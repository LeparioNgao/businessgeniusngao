"""
oilrig.py

A teaching-scale oil-rig condition-monitoring system.

This example demonstrates the shape of a production data-analysis service:

    sensor data -> validation -> feature engineering -> anomaly detection
                 -> risk scoring -> maintenance recommendations -> report

The data is simulated so the file can run on a normal Python installation.
A real deployment would replace SimulatedRigSource with an OPC-UA, MQTT,
 historian, or vendor API adapter. This program only recommends actions; it
never controls a valve, pump, well, or other safety-critical equipment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from math import sqrt
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable, Protocol
import json
import logging
import random


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


# These limits are illustrative engineering assumptions, not operating guidance.
# In a real rig they would come from approved process-safety documentation.
@dataclass(frozen=True)
class SensorLimits:
    temperature_c: tuple[float, float] = (0.0, 150.0)
    pressure_bar: tuple[float, float] = (0.0, 250.0)
    vibration_mm_s: tuple[float, float] = (0.0, 45.0)
    flow_m3_h: tuple[float, float] = (0.0, 500.0)


@dataclass(frozen=True)
class SensorReading:
    timestamp: datetime
    asset_id: str
    temperature_c: float
    pressure_bar: float
    vibration_mm_s: float
    flow_m3_h: float


@dataclass(frozen=True)
class QualityIssue:
    asset_id: str
    timestamp: str
    field: str
    message: str


@dataclass(frozen=True)
class AssetFeatures:
    asset_id: str
    sample_count: int
    average_temperature_c: float
    average_pressure_bar: float
    average_vibration_mm_s: float
    average_flow_m3_h: float
    latest_vibration_mm_s: float
    vibration_change_mm_s: float
    pressure_stdev_bar: float
    flow_change_percent: float


@dataclass(frozen=True)
class Alert:
    asset_id: str
    severity: str
    score: int
    reasons: tuple[str, ...]
    recommended_action: str


class RigDataSource(Protocol):
    """Any production or simulated adapter can satisfy this interface."""

    def read(self, start: datetime, end: datetime) -> list[SensorReading]:
        ...


class SimulatedRigSource:
    """Generate realistic-looking readings, including one degrading pump."""

    def __init__(self, seed: int = 42) -> None:
        self.random = random.Random(seed)
        self.assets = ["P-101", "P-102", "SEP-201", "COMP-301"]

    def read(self, start: datetime, end: datetime) -> list[SensorReading]:
        readings: list[SensorReading] = []
        current = start
        sample_number = 0
        while current < end:
            for asset_id in self.assets:
                vibration = 4.0 + self.random.gauss(0, 0.45)
                pressure = 118.0 + self.random.gauss(0, 1.8)
                temperature = 71.0 + self.random.gauss(0, 1.2)
                flow = 205.0 + self.random.gauss(0, 3.0)

                # P-102 develops a bearing problem over the final samples.
                if asset_id == "P-102" and sample_number >= 18:
                    degradation = (sample_number - 17) * 0.9
                    vibration += degradation
                    temperature += degradation * 0.7
                    flow -= degradation * 2.2

                readings.append(SensorReading(
                    timestamp=current,
                    asset_id=asset_id,
                    temperature_c=temperature,
                    pressure_bar=pressure,
                    vibration_mm_s=max(0.0, vibration),
                    flow_m3_h=max(0.0, flow),
                ))
            current += timedelta(minutes=15)
            sample_number += 1
        return readings


def validate_readings(
    readings: Iterable[SensorReading], limits: SensorLimits
) -> tuple[list[SensorReading], list[QualityIssue]]:
    """Reject impossible values while preserving an audit trail of the reason."""
    valid: list[SensorReading] = []
    issues: list[QualityIssue] = []
    numeric_fields = ("temperature_c", "pressure_bar", "vibration_mm_s", "flow_m3_h")

    for reading in readings:
        reading_is_valid = True
        for field in numeric_fields:
            value = getattr(reading, field)
            lower, upper = getattr(limits, field)
            if not lower <= value <= upper:
                issues.append(QualityIssue(
                    reading.asset_id,
                    reading.timestamp.isoformat(),
                    field,
                    f"value {value:.2f} outside [{lower}, {upper}]",
                ))
                reading_is_valid = False
        if reading_is_valid:
            valid.append(reading)
    return valid, issues


def group_by_asset(readings: Iterable[SensorReading]) -> dict[str, list[SensorReading]]:
    grouped: dict[str, list[SensorReading]] = {}
    for reading in readings:
        grouped.setdefault(reading.asset_id, []).append(reading)
    for asset_readings in grouped.values():
        asset_readings.sort(key=lambda reading: reading.timestamp)
    return grouped


def percent_change(old: float, new: float) -> float:
    if old == 0:
        return 0.0
    return ((new - old) / old) * 100


def engineer_features(readings: list[SensorReading]) -> list[AssetFeatures]:
    """Convert raw time-series rows into one explainable record per asset."""
    features: list[AssetFeatures] = []
    for asset_id, asset_readings in group_by_asset(readings).items():
        vibrations = [item.vibration_mm_s for item in asset_readings]
        pressures = [item.pressure_bar for item in asset_readings]
        flows = [item.flow_m3_h for item in asset_readings]
        first_flow = mean(flows[: min(3, len(flows))])
        latest = asset_readings[-1]
        baseline_vibration = mean(vibrations[: min(3, len(vibrations))])
        features.append(AssetFeatures(
            asset_id=asset_id,
            sample_count=len(asset_readings),
            average_temperature_c=mean(item.temperature_c for item in asset_readings),
            average_pressure_bar=mean(pressures),
            average_vibration_mm_s=mean(vibrations),
            average_flow_m3_h=mean(flows),
            latest_vibration_mm_s=latest.vibration_mm_s,
            vibration_change_mm_s=latest.vibration_mm_s - baseline_vibration,
            pressure_stdev_bar=stdev(pressures) if len(pressures) > 1 else 0.0,
            flow_change_percent=percent_change(first_flow, latest.flow_m3_h),
        ))
    return sorted(features, key=lambda item: item.asset_id)


def detect_anomalies(features: Iterable[AssetFeatures]) -> list[Alert]:
    """Use transparent thresholds so an operator can inspect every alert reason."""
    alerts: list[Alert] = []
    for item in features:
        reasons: list[str] = []
        score = 0
        if item.latest_vibration_mm_s > 12:
            reasons.append(f"high latest vibration ({item.latest_vibration_mm_s:.1f} mm/s)")
            score += 45
        if item.vibration_change_mm_s > 5:
            reasons.append(f"vibration rose {item.vibration_change_mm_s:.1f} mm/s")
            score += 25
        if item.flow_change_percent < -8:
            reasons.append(f"flow fell {abs(item.flow_change_percent):.1f}%")
            score += 20
        if item.average_temperature_c > 80:
            reasons.append(f"elevated average temperature ({item.average_temperature_c:.1f} C)")
            score += 15
        if item.pressure_stdev_bar > 4:
            reasons.append(f"unstable pressure (stdev {item.pressure_stdev_bar:.1f} bar)")
            score += 10

        if not reasons:
            continue
        severity = "critical" if score >= 70 else "warning"
        action = (
            "Escalate to the control-room and maintenance teams; follow the approved emergency procedure."
            if severity == "critical"
            else "Inspect the asset, verify the sensor, and schedule maintenance according to site procedure."
        )
        alerts.append(Alert(item.asset_id, severity, min(score, 100), tuple(reasons), action))
    return sorted(alerts, key=lambda alert: (-alert.score, alert.asset_id))


def build_report(
    readings: list[SensorReading],
    issues: list[QualityIssue],
    features: list[AssetFeatures],
    alerts: list[Alert],
    start: datetime,
    end: datetime,
) -> dict:
    """Create a portable report for a dashboard, API, or incident archive."""
    severity_counts = {"critical": 0, "warning": 0}
    for alert in alerts:
        severity_counts[alert.severity] += 1
    return {
        "report_type": "oil_rig_condition_monitoring",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window": {"start": start.isoformat(), "end": end.isoformat()},
        "data_quality": {
            "accepted_readings": len(readings),
            "rejected_readings": len(issues),
            "issues": [asdict(issue) for issue in issues],
        },
        "summary": {
            "assets_monitored": len(features),
            "alerts": len(alerts),
            "critical_alerts": severity_counts["critical"],
            "warning_alerts": severity_counts["warning"],
        },
        "asset_features": [asdict(item) for item in features],
        "alerts": [asdict(alert) for alert in alerts],
    }


def print_operator_summary(report: dict) -> None:
    """Print a compact human-readable view while retaining the full JSON report."""
    summary = report["summary"]
    print("\n" + "=" * 72)
    print("OIL RIG CONDITION MONITORING REPORT")
    print("=" * 72)
    print(f"Assets monitored: {summary['assets_monitored']}")
    print(f"Accepted readings: {report['data_quality']['accepted_readings']}")
    print(f"Data-quality issues: {report['data_quality']['rejected_readings']}")
    print(f"Alerts: {summary['alerts']} ({summary['critical_alerts']} critical, {summary['warning_alerts']} warning)")
    print("\nAlerts requiring review:")
    if not report["alerts"]:
        print("  None")
    for alert in report["alerts"]:
        print(f"  [{alert['severity'].upper():8}] {alert['asset_id']} score={alert['score']}")
        for reason in alert["reasons"]:
            print(f"      - {reason}")
        print(f"      Action: {alert['recommended_action']}")
    print("=" * 72)


def run_monitoring_cycle(output_path: Path = Path("oilrig_report.json")) -> dict:
    """Orchestrate one scheduled monitoring cycle."""
    end = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    start = end - timedelta(hours=8)
    source: RigDataSource = SimulatedRigSource()

    LOGGER.info("Reading sensor data for %s to %s", start.isoformat(), end.isoformat())
    raw_readings = source.read(start, end)
    readings, issues = validate_readings(raw_readings, SensorLimits())
    features = engineer_features(readings)
    alerts = detect_anomalies(features)
    report = build_report(readings, issues, features, alerts, start, end)

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    LOGGER.info("Wrote report to %s", output_path)
    print_operator_summary(report)
    return report


if __name__ == "__main__":
    run_monitoring_cycle()
