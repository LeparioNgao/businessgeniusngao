#!/usr/bin/env python3
"""Serve the crypto market webpage and a small JSON API."""

import json
import mimetypes
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import load_dotenv

from crypto_market_tool import fetch_market_snapshot

PROJECT_DIRECTORY = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIRECTORY / ".env")
load_dotenv(PROJECT_DIRECTORY.parent / ".env")


def json_response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


class CryptoMarketHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/snapshot":
            self.serve_snapshot(parsed)
            return

        if parsed.path in ("/", "/index.html"):
            self.serve_file(PROJECT_DIRECTORY / "index.html")
            return

        file_path = PROJECT_DIRECTORY / parsed.path.lstrip("/")
        if parsed.path in ("/styles.css", "/app.js") and file_path.is_file():
            self.serve_file(file_path)
            return

        json_response(self, 404, {"error": "Page or asset not found."})

    def serve_snapshot(self, parsed):
        query = parse_qs(parsed.query)
        coin_id = query.get("coin", [""])[0].strip().lower()
        currency = query.get("currency", ["usd"])[0].strip().lower() or "usd"

        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", coin_id):
            json_response(self, 400, {"error": "Enter a valid CoinGecko coin ID, such as bitcoin or ethereum."})
            return

        if not re.fullmatch(r"[a-z]{3,5}", currency):
            json_response(self, 400, {"error": "Enter a valid currency code, such as usd or kes."})
            return

        api_key = os.getenv("COINGECKO_API_KEY")
        if not api_key:
            json_response(self, 500, {"error": "CoinGecko API key is not configured on the server."})
            return

        try:
            snapshot = fetch_market_snapshot(coin_id, currency, api_key)
            json_response(self, 200, snapshot)
        except requests.HTTPError as error:
            status = error.response.status_code if error.response is not None else 502
            if status == 401:
                message = "CoinGecko rejected the API key. Check the server configuration."
            elif status == 429:
                message = "CoinGecko request limit reached. Please try again later."
            else:
                message = f"CoinGecko returned an error (HTTP {status})."
            json_response(self, 502 if status not in (400, 404, 429) else status, {"error": message})
        except requests.RequestException:
            json_response(self, 502, {"error": "Could not connect to CoinGecko. Check your internet connection."})
        except ValueError as error:
            json_response(self, 400, {"error": str(error)})

    def serve_file(self, file_path):
        if not file_path.is_file():
            json_response(self, 404, {"error": "File not found."})
            return

        content = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    port = 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), CryptoMarketHandler)
    print(f"Crypto market webpage: http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
