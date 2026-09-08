#This is your Week 4 project. You will build a grade tracker that reads student data from a simulated CSV, processes it with functions, handles bad data using error handling, computes averages and letter grades, then outputs a clean report. Every skill from this week appears in this project.

import csv
import io
import json

student_data = """name,score1,score2,score3
Leuyan Lepario,90, 78, 85
John Kamano, 78, 66
June Wambui, 88, 75, 90
Leo Wangai, 98, bad data, 67"""


def parse_score(data):
    try:
        return int(data)
    except (ValueError, TypeError):
        return None

def calculate_average(scores):
    valid_scores = [r for r in scores if r is not None]
    if not valid_scores:
        return None
    return round(sum(valid_scores) / len(valid_scores), 1)

def letter_grade(avg):
    if avg is None:
        return "N/A"
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

f = io.StringIO(student_data)
reader = csv.DictReader(f)
results = []

print("=" * 50)
print(f"{'NAME':<20} {'AVG':>5}  {'GRADE':>5}  NOTES")
print("=" * 50)

for row in reader:
    scores = [
        parse_score(row["score1"]),
        parse_score(row["score2"]),
        parse_score(row["score3"])
    ]
    invalid_count = scores.count(None)
    avg = calculate_average(scores)
    grade = letter_grade(avg)
    notes = f"{invalid_count} invalid score(s)" if invalid_count else "All scores valid"

    print(f"{row['name']:<20} {str(avg):>5}  {grade:>5}  {notes}")

    results.append({
        "name": row["name"],
        "scores": [row["score1"], row["score2"], row["score3"]],
        "average": avg,
        "grade": grade
    })

print("=" * 50)

#Class Averages
valid_avgs = [r["average"] for r in results if r["average"] is not None]
class_avg = round(sum(valid_avgs) / len(valid_avgs), 1)
print(f"\nClass average: {class_avg}")
print(f"Students: {len(results)}")

#Export results to JSON
with open("student_results.json", "w") as json_file:
    json.dump(results, json_file, indent=4)


#Export as JSON
print("\nJSON Results:")
print(json.dumps(results, indent=2))
