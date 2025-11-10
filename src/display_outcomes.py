import json

TEAM = "Georgia Tech"
FILE = "data/scenarios/unique_scenario_breakdowns.json"

with open(FILE) as f:
    data = json.load(f)

total_count = sum(entry["count"] for entry in data)

# Initialize counters
counts = {
    "3-way tie for first": 0,
    "2-way tie for second": 0,
    "GT outright first": 0
}

for entry in data:
    top = entry["top_teams"]
    second = entry["second_teams"]
    c = entry["count"]

    if len(top) == 3 and TEAM in top:
        counts["3-way tie for first"] += c
    elif len(top) == 1 and len(second) == 2 and TEAM in second:
        counts["2-way tie for second"] += c
    elif len(top) == 1 and TEAM in top:
        counts["GT outright first"] += c

# Print results
for outcome, c in counts.items():
    pct = c / total_count * 100
    print(f"{outcome}: {c:,} ({pct:.2f}% of all outcomes)")

# Final combined total
total_gt = sum(counts.values())
print(f"\nGeorgia Tech appears in {total_gt:,} scenarios "
      f"({total_gt / total_count * 100:.2f}% of all outcomes)")