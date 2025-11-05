# src/display_standings_tied_conf_only.py
import json
from collections import Counter

# Load team data
with open("data/teams.json") as f:
    teams = json.load(f)

# Sort by conference record first, then overall record for display
teams_sorted = sorted(
    teams,
    key=lambda t: (
        -t["conferenceWins"],
        t["conferenceLosses"],
        -t["wins"],
        t["losses"]
    )
)

# Count how many teams share each conference record
conf_records = [(t["conferenceWins"], t["conferenceLosses"]) for t in teams_sorted]
record_counts = Counter(conf_records)

# Assign ranks
ranked_teams = []
prev_conf_key = None
rank = 0

for idx, t in enumerate(teams_sorted):
    conf_key = (t["conferenceWins"], t["conferenceLosses"])
    if conf_key != prev_conf_key:
        rank = idx + 1  # new rank
    # If more than one team shares this conference record → tie
    if record_counts[conf_key] > 1:
        display_rank = f"t-{rank}"
    else:
        display_rank = str(rank)
    ranked_teams.append((display_rank, t))
    prev_conf_key = conf_key

# Display standings
print(f"{'Rank':<6} {'Team':<25} {'Conf W-L':<10} {'Overall W-L':<10}")
print("-" * 55)
for r, t in ranked_teams:
    conf_record = f"{t['conferenceWins']}-{t['conferenceLosses']}"
    overall_record = f"{t['wins']}-{t['losses']}"
    print(f"{r:<6} {t['team']:<25} {conf_record:<10} {overall_record:<10}")
