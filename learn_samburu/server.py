#!/usr/bin/env python3
"""Run the local Learn Samburu word and recording catalog."""

import json
import mimetypes
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


PROJECT_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = PROJECT_DIRECTORY / "data"
DATABASE_PATH = DATA_DIRECTORY / "learn_samburu.sqlite3"
AUDIO_DIRECTORY = DATA_DIRECTORY / "audio"
MAX_AUDIO_BYTES = 15 * 1024 * 1024
MAX_JSON_BYTES = 32 * 1024
AUDIO_TYPES = {
    "audio/webm": "webm",
    "audio/ogg": "ogg",
    "audio/mp4": "m4a",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/mpeg": "mp3",
    "audio/aac": "aac",
}


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def database():
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with database() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase TEXT NOT NULL,
                meaning TEXT NOT NULL,
                pronunciation TEXT NOT NULL DEFAULT '',
                context TEXT NOT NULL DEFAULT '',
                example TEXT NOT NULL DEFAULT '',
                speaker TEXT NOT NULL DEFAULT '',
                audio_file TEXT,
                consent_confirmed_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )


def entry_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Entry data must be an object.")

    fields = ("phrase", "meaning", "pronunciation", "context", "example", "speaker")
    values = {field: str(payload.get(field, "")).strip() for field in fields}
    if not values["phrase"] or not values["meaning"]:
        raise ValueError("Add both the Samburu word or phrase and its meaning.")
    limits = {
        "phrase": 500,
        "meaning": 1000,
        "pronunciation": 1000,
        "context": 2000,
        "example": 2000,
        "speaker": 120,
    }
    for field, limit in limits.items():
        if len(values[field]) > limit:
            raise ValueError(f"{field.capitalize()} must be {limit} characters or fewer.")
    return values


def serialize_entry(row):
    entry = dict(row)
    entry["audio_url"] = f"/audio/{entry['audio_file']}" if entry["audio_file"] else None
    entry["review_status"] = "Needs review"
    return entry


class LearnSamburuHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/entries":
            self.list_entries(parsed)
            return
        if parsed.path.startswith("/audio/"):
            self.serve_audio(parsed.path.removeprefix("/audio/"))
            return
        static_files = {
            "/": "index.html",
            "/index.html": "index.html",
            "/styles.css": "styles.css",
            "/app.js": "app.js",
        }
        filename = static_files.get(parsed.path)
        if filename:
            self.serve_file(PROJECT_DIRECTORY / filename)
            return
        self.send_json(404, {"error": "Page or asset not found."})

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/entries":
                self.create_entry()
                return
            match = re.fullmatch(r"/api/entries/(\d+)/audio", parsed.path)
            if match:
                self.save_audio(int(match.group(1)))
                return
            self.send_json(404, {"error": "Endpoint not found."})
        except ValueError as error:
            self.send_json(400, {"error": str(error)})

    def do_PUT(self):
        match = re.fullmatch(r"/api/entries/(\d+)", urlparse(self.path).path)
        if not match:
            self.send_json(404, {"error": "Entry not found."})
            return
        try:
            self.update_entry(int(match.group(1)))
        except ValueError as error:
            self.send_json(400, {"error": str(error)})

    def do_DELETE(self):
        match = re.fullmatch(r"/api/entries/(\d+)", urlparse(self.path).path)
        if not match:
            self.send_json(404, {"error": "Entry not found."})
            return
        self.delete_entry(int(match.group(1)))

    def read_json(self):
        if self.headers.get_content_type() != "application/json":
            raise ValueError("Send entry details as JSON.")
        length = self.content_length(MAX_JSON_BYTES)
        try:
            payload = json.loads(self.rfile.read(length))
        except json.JSONDecodeError as error:
            raise ValueError("Entry data is not valid JSON.") from error
        return entry_payload(payload)

    def content_length(self, maximum):
        raw_length = self.headers.get("Content-Length", "")
        if not raw_length.isdigit():
            raise ValueError("A valid content length is required.")
        length = int(raw_length)
        if length <= 0 or length > maximum:
            raise ValueError("The submitted file or data is empty or too large.")
        return length

    def list_entries(self, parsed):
        query = parse_qs(parsed.query).get("q", [""])[0].strip()
        with database() as connection:
            rows = connection.execute(
                """SELECT * FROM entries
                   WHERE phrase LIKE ? OR meaning LIKE ? OR context LIKE ?
                   ORDER BY updated_at DESC, id DESC""",
                (f"%{query}%", f"%{query}%", f"%{query}%"),
            ).fetchall()
        self.send_json(200, {"entries": [serialize_entry(row) for row in rows]})

    def create_entry(self):
        values = self.read_json()
        created_at = now_utc()
        with database() as connection:
            cursor = connection.execute(
                """INSERT INTO entries
                   (phrase, meaning, pronunciation, context, example, speaker, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (*values.values(), created_at, created_at),
            )
            row = connection.execute(
                "SELECT * FROM entries WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        self.send_json(201, {"entry": serialize_entry(row)})

    def update_entry(self, entry_id):
        values = self.read_json()
        with database() as connection:
            cursor = connection.execute(
                """UPDATE entries SET phrase = ?, meaning = ?, pronunciation = ?, context = ?,
                   example = ?, speaker = ?, updated_at = ? WHERE id = ?""",
                (*values.values(), now_utc(), entry_id),
            )
            if cursor.rowcount == 0:
                self.send_json(404, {"error": "Entry not found."})
                return
            row = connection.execute(
                "SELECT * FROM entries WHERE id = ?", (entry_id,)
            ).fetchone()
        self.send_json(200, {"entry": serialize_entry(row)})

    def save_audio(self, entry_id):
        if self.headers.get("X-Recording-Consent") != "confirmed":
            raise ValueError("Confirm you have permission to save this speaker's recording.")
        content_type = self.headers.get_content_type().lower()
        extension = AUDIO_TYPES.get(content_type)
        if not extension:
            raise ValueError("Use a supported audio file: WebM, Ogg, MP4, WAV, MP3, or AAC.")
        length = self.content_length(MAX_AUDIO_BYTES)
        audio_bytes = self.rfile.read(length)
        if len(audio_bytes) != length:
            raise ValueError("The audio upload was incomplete. Please try again.")

        AUDIO_DIRECTORY.mkdir(parents=True, exist_ok=True)
        filename = f"{entry_id}.{extension}"
        destination = AUDIO_DIRECTORY / filename
        with database() as connection:
            row = connection.execute(
                "SELECT audio_file FROM entries WHERE id = ?", (entry_id,)
            ).fetchone()
            if row is None:
                self.send_json(404, {"error": "Entry not found."})
                return
            destination.write_bytes(audio_bytes)
            connection.execute(
                """UPDATE entries SET audio_file = ?, consent_confirmed_at = ?, updated_at = ?
                   WHERE id = ?""",
                (filename, now_utc(), now_utc(), entry_id),
            )
            if row["audio_file"] and row["audio_file"] != filename:
                (AUDIO_DIRECTORY / row["audio_file"]).unlink(missing_ok=True)
            updated = connection.execute(
                "SELECT * FROM entries WHERE id = ?", (entry_id,)
            ).fetchone()
        self.send_json(200, {"entry": serialize_entry(updated)})

    def delete_entry(self, entry_id):
        with database() as connection:
            row = connection.execute(
                "SELECT audio_file FROM entries WHERE id = ?", (entry_id,)
            ).fetchone()
            if row is None:
                self.send_json(404, {"error": "Entry not found."})
                return
            connection.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        if row["audio_file"]:
            (AUDIO_DIRECTORY / row["audio_file"]).unlink(missing_ok=True)
        self.send_json(200, {"deleted": True})

    def serve_audio(self, filename):
        if not re.fullmatch(r"\d+\.(webm|ogg|m4a|wav|mp3|aac)", filename):
            self.send_json(404, {"error": "Recording not found."})
            return
        self.serve_file(AUDIO_DIRECTORY / filename)

    def serve_file(self, file_path):
        if not file_path.is_file():
            self.send_json(404, {"error": "File not found."})
            return
        content = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    initialize_database()
    server = ThreadingHTTPServer(("127.0.0.1", 8001), LearnSamburuHandler)
    print("Learn Samburu is ready at http://127.0.0.1:8001")
    print(f"Entries and recordings are stored in {DATA_DIRECTORY}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nLearn Samburu stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()