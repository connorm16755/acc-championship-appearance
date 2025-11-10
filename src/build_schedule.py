import requests
import json

API_KEY = "G7JwRiQN6l2qL9ePSWyc81iT1HhZ28etf8Brq243/O9rn5inJMLjNN8K/+6zD+7c"
YEAR = 2025
CONFERENCE = "ACC"

url = f"https://api.collegefootballdata.com/games?year={YEAR}&conference={CONFERENCE}"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)
games = response.json()

# Filter to only regular season conference games
schedule = []
for g in games:
    if g["seasonType"] == "regular":
        schedule.append({
            "week": g["week"],
            "home": g["homeTeam"],
            "away": g["awayTeam"],
            "conference": g["conferenceGame"],
            "completed": g["completed"]
        })

# Sort by week for readability
schedule.sort(key=lambda x: x["week"])

with open("data/schedule.json", "w") as f:
    json.dump(schedule, f, indent=4)

print(f"Saved {len(schedule)} games to data/schedule.json")
