"""
logisticsdata.py

A teaching-scale logistics data platform.

A logistics company is not analyzing one thing. It is coordinating a moving
network of orders, vehicles, drivers, warehouses, packages, and customers.
This module demonstrates the main operating loop:

    events -> validation -> shipment state -> ETA/risk features -> decisions
             -> exception queue -> management report

Real-world patterns represented here:

1. UPS ORION optimizes delivery sequences and uses operations data to improve
   routes: https://about.ups.com/us/en/our-company/innovation-and-technology/orion.html
2. DHL publishes work on warehouse automation and robotics. A real system
   combines warehouse events with labor and inventory data:
   https://www.dhl.com/global-en/home/insights-and-innovation/insights/warehouse-automation.html
3. Maersk offers remote container monitoring and cargo visibility, illustrating
   why temperature, location, and condition events matter:
   https://www.maersk.com/digital-services/cargo-visibility
4. Amazon describes robotics used in fulfillment centers. This illustrates a
   warehouse workflow where scans and task events are operational data:
   https://www.aboutamazon.com/news/operations/amazon-robotics-fulfillment-center

These are architecture examples, not claims that this small script reproduces
those companies' proprietary systems. All data below is simulated. In a real
company, source adapters would connect to a transport-management system,
warehouse-management system, GPS/telematics provider, carrier APIs, and
customer notifications. The program recommends actions; it does not drive a
vehicle or independently change a shipment's contractual commitment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Iterable, Protocol
import json
import logging
import random


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


# Business rules should be configuration in production, not magic numbers in
# code. These illustrative limits make the example easy to understand.
@dataclass(frozen=True)
class LogisticsRules:
    late_tolerance_minutes: int = 20
    cold_chain_min_c: float = 2.0
    cold_chain_max_c: float = 8.0
    vehicle_utilization_target: float = 0.85
    max_route_hours: float = 10.0


@dataclass(frozen=True)
class Shipment:
    shipment_id: str
    customer: str
    origin: str
    destination: str
    service_level: str
    promised_delivery: datetime
    weight_kg: float
    temperature_controlled: bool
    assigned_vehicle: str


@dataclass(frozen=True)
class Vehicle:
    vehicle_id: str
    driver: str
    capacity_kg: float
    planned_distance_km: float
    actual_distance_km: float
    planned_route_hours: float
    actual_route_hours: float


@dataclass(frozen=True)
class TrackingEvent:
    timestamp: datetime
    shipment_id: str
    event_type: str
    location: str
    temperature_c: float | None = None
    latitude: float | None = None
    longitude: float | None = None


@dataclass(frozen=True)
class WarehouseEvent:
    timestamp: datetime
    warehouse_id: str
    shipment_id: str
    event_type: str
    operator_or_robot: str


@dataclass(frozen=True)
class DataIssue:
    source: str
    record_id: str
    field: str
    message: str


@dataclass(frozen=True)
class ShipmentFeatures:
    shipment_id: str
    current_status: str
    last_location: str
    event_count: int
    minutes_until_promise: float
    estimated_delay_minutes: float
    temperature_breaches: int
    missing_expected_scan: bool
    risk_score: int


@dataclass(frozen=True)
class ExceptionCase:
    shipment_id: str
    priority: str
    risk_score: int
    reason: str
    owner: str
    recommended_action: str


class LogisticsDataSource(Protocol):
    """Any API, database, message queue, or simulator can implement this."""

    def load(self, start: datetime, end: datetime) -> tuple[list[Shipment], list[Vehicle], list[TrackingEvent], list[WarehouseEvent]]:
        ...


class SimulatedLogisticsSource:
    """Produce a small network with one late and one cold-chain shipment."""

    def __init__(self, seed: int = 7) -> None:
        self.random = random.Random(seed)

    def load(self, start: datetime, end: datetime) -> tuple[list[Shipment], list[Vehicle], list[TrackingEvent], list[WarehouseEvent]]:
        shipments = [
            Shipment("SHP-1001", "Nairobi Market", "Nairobi", "Mombasa", "express", end + timedelta(hours=2), 420, False, "TRK-01"),
            Shipment("SHP-1002", "Coast Hospital", "Nairobi", "Mombasa", "priority", end - timedelta(minutes=10), 180, True, "TRK-02"),
            Shipment("SHP-1003", "Kisumu Grocers", "Nairobi", "Kisumu", "standard", end + timedelta(hours=5), 650, True, "TRK-03"),
            Shipment("SHP-1004", "Eldoret Hardware", "Nairobi", "Eldoret", "standard", end + timedelta(hours=7), 900, False, "TRK-03"),
        ]
        vehicles = [
            Vehicle("TRK-01", "Amina Otieno", 1000, 485, 510, 8.0, 8.4),
            Vehicle("TRK-02", "David Mwangi", 800, 485, 560, 8.0, 10.2),
            Vehicle("TRK-03", "Ruth Kamau", 1800, 650, 635, 9.0, 8.7),
        ]
        tracking: list[TrackingEvent] = []
        warehouse: list[WarehouseEvent] = []
        for shipment in shipments:
            tracking.extend([
                TrackingEvent(start, shipment.shipment_id, "picked_up", shipment.origin),
                TrackingEvent(start + timedelta(hours=2), shipment.shipment_id, "in_transit", "A104 checkpoint"),
            ])
            warehouse.append(WarehouseEvent(start - timedelta(minutes=30), "WH-NBO", shipment.shipment_id, "picked", "worker-17"))
            warehouse.append(WarehouseEvent(start - timedelta(minutes=15), "WH-NBO", shipment.shipment_id, "loaded", "worker-17"))

        # The priority refrigerated shipment has a temperature excursion and
        # an unusually long route. Those are the signals an exception team sees.
        tracking.extend([
            TrackingEvent(end - timedelta(minutes=35), "SHP-1002", "in_transit", "A109 checkpoint", 10.5),
            TrackingEvent(end - timedelta(minutes=5), "SHP-1002", "in_transit", "A109 checkpoint", 11.2),
            TrackingEvent(end - timedelta(minutes=5), "SHP-1001", "in_transit", "A109 checkpoint"),
            TrackingEvent(end - timedelta(minutes=5), "SHP-1003", "in_transit", "A104 checkpoint", 5.0),
            TrackingEvent(end - timedelta(minutes=5), "SHP-1004", "in_transit", "A104 checkpoint"),
        ])
        return shipments, vehicles, tracking, warehouse


def validate_data(
    shipments: Iterable[Shipment],
    vehicles: Iterable[Vehicle],
    tracking: Iterable[TrackingEvent],
    rules: LogisticsRules,
) -> list[DataIssue]:
    """Find invalid or dangerous data before it reaches a decision-maker."""
    issues: list[DataIssue] = []
    vehicle_ids = {vehicle.vehicle_id for vehicle in vehicles}
    for shipment in shipments:
        if shipment.weight_kg <= 0:
            issues.append(DataIssue("shipments", shipment.shipment_id, "weight_kg", "must be positive"))
        if shipment.assigned_vehicle not in vehicle_ids:
            issues.append(DataIssue("shipments", shipment.shipment_id, "assigned_vehicle", "vehicle does not exist"))
    for event in tracking:
        if event.temperature_c is not None and not -80 <= event.temperature_c <= 80:
            issues.append(DataIssue("tracking", event.shipment_id, "temperature_c", "outside plausible sensor range"))
        if event.temperature_c is not None and event.shipment_id == "":
            issues.append(DataIssue("tracking", "unknown", "shipment_id", "missing shipment identifier"))
    for vehicle in vehicles:
        if vehicle.capacity_kg <= 0:
            issues.append(DataIssue("vehicles", vehicle.vehicle_id, "capacity_kg", "must be positive"))
        if vehicle.actual_route_hours > rules.max_route_hours:
            LOGGER.warning("Vehicle %s exceeded the illustrative route-hour limit", vehicle.vehicle_id)
    return issues


def latest_events_by_shipment(events: Iterable[TrackingEvent]) -> dict[str, list[TrackingEvent]]:
    grouped: dict[str, list[TrackingEvent]] = {}
    for event in events:
        grouped.setdefault(event.shipment_id, []).append(event)
    for shipment_events in grouped.values():
        shipment_events.sort(key=lambda event: event.timestamp)
    return grouped


def estimate_delay_minutes(shipment: Shipment, latest_event: TrackingEvent, now: datetime) -> float:
    """A simple explainable ETA proxy; production systems use routing engines."""
    minutes_late = (now - shipment.promised_delivery).total_seconds() / 60
    if minutes_late <= 0:
        return 0.0
    # A recent in-transit event means the shipment is moving, so avoid
    # pretending we know the exact route ETA from this deliberately small model.
    return round(minutes_late if latest_event.event_type == "in_transit" else minutes_late + 30, 1)


def build_shipment_features(
    shipments: Iterable[Shipment],
    tracking: Iterable[TrackingEvent],
    now: datetime,
    rules: LogisticsRules,
) -> list[ShipmentFeatures]:
    """Turn event streams into features that an operations team can act on."""
    events_by_shipment = latest_events_by_shipment(tracking)
    features: list[ShipmentFeatures] = []
    for shipment in shipments:
        events = events_by_shipment.get(shipment.shipment_id, [])
        latest = events[-1] if events else None
        temperatures = [event.temperature_c for event in events if event.temperature_c is not None]
        breaches = sum(not rules.cold_chain_min_c <= temperature <= rules.cold_chain_max_c for temperature in temperatures) if shipment.temperature_controlled else 0
        delay = estimate_delay_minutes(shipment, latest, now) if latest else 60.0
        missing_scan = not any(event.event_type == "in_transit" for event in events)
        score = 0
        if delay > rules.late_tolerance_minutes:
            score += 45
        if breaches:
            score += 50
        if missing_scan:
            score += 20
        if shipment.service_level == "priority":
            score += 10
        features.append(ShipmentFeatures(
            shipment.shipment_id,
            latest.event_type if latest else "unknown",
            latest.location if latest else "unknown",
            len(events),
            round((shipment.promised_delivery - now).total_seconds() / 60, 1),
            delay,
            breaches,
            missing_scan,
            min(score, 100),
        ))
    return sorted(features, key=lambda feature: (-feature.risk_score, feature.shipment_id))


def create_exception_queue(features: Iterable[ShipmentFeatures]) -> list[ExceptionCase]:
    """Prioritize human work instead of sending every event as an alert."""
    cases: list[ExceptionCase] = []
    for feature in features:
        if feature.risk_score == 0:
            continue
        reasons: list[str] = []
        owner = "dispatch"
        action = "Review route and contact the carrier."
        if feature.estimated_delay_minutes > 20:
            reasons.append(f"estimated delay {feature.estimated_delay_minutes:.0f} minutes")
        if feature.temperature_breaches:
            reasons.append(f"{feature.temperature_breaches} cold-chain temperature breach(es)")
            owner = "cold-chain control"
            action = "Quarantine or inspect the shipment and notify the customer under the cold-chain SOP."
        if feature.missing_expected_scan:
            reasons.append("missing in-transit scan")
        priority = "critical" if feature.risk_score >= 70 else "high" if feature.risk_score >= 40 else "medium"
        cases.append(ExceptionCase(feature.shipment_id, priority, feature.risk_score, "; ".join(reasons), owner, action))
    return cases


def calculate_network_kpis(shipments: list[Shipment], vehicles: list[Vehicle], warehouse_events: list[WarehouseEvent]) -> dict:
    """Measure service, fleet, and warehouse performance in one report."""
    total_weight = sum(shipment.weight_kg for shipment in shipments)
    vehicle_capacity = sum(vehicle.capacity_kg for vehicle in vehicles)
    on_time_proxy = sum(shipment.promised_delivery >= datetime.now(timezone.utc) for shipment in shipments) / len(shipments)
    route_efficiency = mean(vehicle.planned_distance_km / vehicle.actual_distance_km for vehicle in vehicles)
    warehouse_completed = sum(event.event_type == "loaded" for event in warehouse_events)
    return {
        "shipments": len(shipments),
        "weight_kg": round(total_weight, 1),
        "on_time_proxy_percent": round(on_time_proxy * 100, 1),
        "fleet_utilization_percent": round(total_weight / vehicle_capacity * 100, 1),
        "route_efficiency_percent": round(route_efficiency * 100, 1),
        "warehouse_load_events": warehouse_completed,
    }


def build_report(
    shipments: list[Shipment],
    vehicles: list[Vehicle],
    tracking: list[TrackingEvent],
    warehouse_events: list[WarehouseEvent],
    issues: list[DataIssue],
    features: list[ShipmentFeatures],
    exceptions: list[ExceptionCase],
    now: datetime,
) -> dict:
    return {
        "report_type": "logistics_control_tower",
        "generated_at": now.isoformat(),
        "kpis": calculate_network_kpis(shipments, vehicles, warehouse_events),
        "data_quality": {"issues": [asdict(issue) for issue in issues], "issue_count": len(issues)},
        "source_counts": {"shipments": len(shipments), "vehicles": len(vehicles), "tracking_events": len(tracking), "warehouse_events": len(warehouse_events)},
        "shipments": [asdict(feature) for feature in features],
        "exception_queue": [asdict(case) for case in exceptions],
    }


def print_operator_summary(report: dict) -> None:
    kpis = report["kpis"]
    print("\n" + "=" * 76)
    print("LOGISTICS CONTROL TOWER REPORT")
    print("=" * 76)
    print(f"Shipments: {kpis['shipments']} | Fleet utilization: {kpis['fleet_utilization_percent']}% | Route efficiency: {kpis['route_efficiency_percent']}%")
    print(f"On-time proxy: {kpis['on_time_proxy_percent']}% | Warehouse load events: {kpis['warehouse_load_events']}")
    print(f"Exceptions requiring human review: {len(report['exception_queue'])}")
    for case in report["exception_queue"]:
        print(f"  [{case['priority'].upper():8}] {case['shipment_id']} score={case['risk_score']} owner={case['owner']}")
        print(f"      {case['reason']}")
        print(f"      Action: {case['recommended_action']}")
    print("=" * 76)


def run_control_tower(output_path: Path = Path("logistics_report.json")) -> dict:
    """Run one scheduled control-tower cycle and archive its output."""
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    start = now - timedelta(hours=10)
    source: LogisticsDataSource = SimulatedLogisticsSource()
    LOGGER.info("Loading logistics events for %s to %s", start.isoformat(), now.isoformat())
    shipments, vehicles, tracking, warehouse_events = source.load(start, now)
    issues = validate_data(shipments, vehicles, tracking, LogisticsRules())
    features = build_shipment_features(shipments, tracking, now, LogisticsRules())
    exceptions = create_exception_queue(features)
    report = build_report(shipments, vehicles, tracking, warehouse_events, issues, features, exceptions, now)
    output_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    LOGGER.info("Wrote report to %s", output_path)
    print_operator_summary(report)
    return report


if __name__ == "__main__":
    run_control_tower()
