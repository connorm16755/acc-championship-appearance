import requests
import json

API_KEY = "G7JwRiQN6l2qL9ePSWyc81iT1HhZ28etf8Brq243/O9rn5inJMLjNN8K/+6zD+7c"
url = "https://api.collegefootballdata.com/records"
params = {
    "year": 2025,
    "conference": "ACC"
}
headers = { "Authorization": f"Bearer {API_KEY}" }

resp = requests.get(url, headers=headers, params=params)
records = resp.json()

# Example output structure:
# [
#   {
#     "team": "Georgia Tech",
#     "conference": "ACC",
#     "confWins": 5,
#     "confLosses": 1,
#     "wins": 7,
#     "losses": 3
#   },
#   ...
# ]

# transform into your schema
teams = []
for r in records:
    teams.append({
        "team": r["team"],
        "wins": r["regularSeason"]["wins"],
        "losses": r["regularSeason"]["losses"],
        "conferenceWins": r["conferenceGames"]["wins"],
        "conferenceLosses": r["conferenceGames"]["losses"]
    })

with open("data/teams.json", "w") as f:
    json.dump(teams, f, indent=4)

print("Updated teams.json with current records")
