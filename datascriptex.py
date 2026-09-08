#Using the four part structure, we can create a Python script that fetches data from an API, processes it, and generates a report. Below is an example of how you might structure such a script with a JSON place holder API:

import json
import os
import argparse
from collections import Counter
from datetime import datetime

import requests

# --- Configuration ---
BASE_API = "https://jsonplaceholder.typicode.com"
ENDPOINT = "/posts"
DATA_DIR = "data"


def ensure_data_dir():
	os.makedirs(DATA_DIR, exist_ok=True)


def fetch_posts(limit: int = 10, timeout: int = 10):
	"""Fetch posts from the JSONPlaceholder API."""
	url = f"{BASE_API}{ENDPOINT}"
	try:
		resp = requests.get(url, params={"_limit": limit}, timeout=timeout)
		resp.raise_for_status()
		return resp.json()
	except requests.RequestException as e:
		raise RuntimeError(f"Failed to fetch posts: {e}")


def process_posts(posts):
	"""Process raw posts into a simple report structure."""
	total = len(posts)
	user_counts = Counter(p.get("userId") for p in posts)
	title_lengths = [len(p.get("title", "")) for p in posts]
	avg_title_len = sum(title_lengths) / total if total else 0

	words = Counter()
	for p in posts:
		words.update(str(p.get("title", "")).lower().split())

	top_words = words.most_common(10)

	return {
		"total_posts": total,
		"posts_per_user": dict(user_counts),
		"avg_title_length": avg_title_len,
		"top_title_words": top_words,
		"generated_at": datetime.utcnow().isoformat() + "Z",
	}


def generate_report(report: dict, out_path: str):
	"""Write the report to JSON and print a short summary."""
	with open(out_path, "w", encoding="utf-8") as fh:
		json.dump(report, fh, indent=2)

	print(f"Report written to: {out_path}")
	print(f"Total posts: {report.get('total_posts')}")
	top_users = sorted(report.get("posts_per_user", {}).items(), key=lambda x: -x[1])[:3]
	print("Top users by post count:")
	for uid, cnt in top_users:
		print(f"  user {uid}: {cnt} posts")


def main():
	parser = argparse.ArgumentParser(description="Fetch posts, process them, and generate a report.")
	parser.add_argument("--limit", type=int, default=20, help="Number of posts to fetch")
	parser.add_argument("--out", type=str, default=os.path.join(DATA_DIR, "report.json"), help="Output report path")
	args = parser.parse_args()

	ensure_data_dir()
	posts = fetch_posts(limit=args.limit)
	report = process_posts(posts)
	generate_report(report, args.out)


if __name__ == "__main__":
	main()