from itertools import product
import copy
import json
from tqdm import tqdm
from collections import Counter

CHECKPOINT = 1_000_000  # save every 1 million scenarios
OUTPUT_FILE = "data/scenarios/unique_scenario_breakdowns.json"

# Load current standings
with open("data/teams.json") as f:
    teams = json.load(f)

# Load remaining games
with open("data/schedule.json") as f:
    schedule = json.load(f)

# Filter remaining games to only those not yet played
remaining_games = [g for g in schedule if not g.get("completed", False)]

num_remaining_games = len(remaining_games)
total_scenarios = 2 ** num_remaining_games

print(f"Remaining Games: {len(remaining_games)}")
print(f"Total scenarios: {total_scenarios}")

# Counter to store unique scenario breakdowns
unique_breakdowns = Counter()

# Each game has 2 outcomes: 0 = home team wins, 1 = away team wins
scenarios = product([0, 1], repeat=num_remaining_games)

for i, scenario in enumerate(tqdm(scenarios, total=total_scenarios, desc="Simulating scenarios"), start=1):
    # Deep copy teams to simulate this scenario
    sim_teams = copy.deepcopy(teams)
    team_lookup = {t['team']: t for t in sim_teams}

    # Apply game results
    for outcome, game in zip(scenario, remaining_games):
        home = game['home']
        away = game['away']
        if outcome == 0:
            winner, loser = home, away
        else:
            winner, loser = away, home

        if winner in team_lookup:
            team_lookup[winner]['wins'] += 1
        if loser in team_lookup:
            team_lookup[loser]['losses'] += 1

        if game.get('conference', False):
            if winner in team_lookup:
                team_lookup[winner]['conferenceWins'] += 1
            if loser in team_lookup:
                team_lookup[loser]['conferenceLosses'] += 1

    # Determine final conference standings
    final_standings = sorted(
        sim_teams,
        key=lambda t: (-t['conferenceWins'], t['conferenceLosses'], -t['wins'], t['losses'])
    )

    # Top and second place teams
    top_conf_record = (final_standings[0]['conferenceWins'], final_standings[0]['conferenceLosses'])
    top_teams = tuple(sorted(t['team'] for t in final_standings if (t['conferenceWins'], t['conferenceLosses']) == top_conf_record))
    top_count = len(top_teams)

    if top_count == 1:
        second_conf_record = (final_standings[top_count]['conferenceWins'], final_standings[top_count]['conferenceLosses'])
        second_teams = tuple(sorted(t['team'] for t in final_standings[top_count:] if (t['conferenceWins'], t['conferenceLosses']) == second_conf_record))
    else:
        second_teams = ()

    # Create a **hashable key** representing this scenario breakdown
    breakdown_key = (top_teams, second_teams)
    unique_breakdowns[breakdown_key] += 1  # increment counter for this unique outcome

    # ----------------------
    # CHECKPOINT SAVE
    # ----------------------
    if i % CHECKPOINT == 0:
        checkpoint_file = f"data/scenarios/checkpoint_scenario_breakdowns_{i}.json"
        # Sort the breakdowns by count descending before saving
        sorted_checkpoint = sorted(
            unique_breakdowns.items(),
            key=lambda x: x[1],
            reverse=True
        )
        with open(checkpoint_file, "w") as f:
            json.dump(
                [{"top_teams": k[0], "second_teams": k[1], "count": v} for k, v in sorted_checkpoint],
                f,
                indent=2
            )
        print(f"Saved checkpoint after {i} scenarios to {checkpoint_file}")

# ----------------------
# FINAL SAVE (sorted by count descending)
# ----------------------
sorted_breakdowns = sorted(
    unique_breakdowns.items(),
    key=lambda x: x[1],  # sort by count
    reverse=True
)

with open(OUTPUT_FILE, "w") as f:
    json.dump(
        [{"top_teams": k[0], "second_teams": k[1], "count": v} for k, v in sorted_breakdowns],
        f,
        indent=2
    )

print(f"Simulation complete. Unique breakdowns saved to {OUTPUT_FILE}")
print(f"Total unique breakdowns: {len(unique_breakdowns)}")