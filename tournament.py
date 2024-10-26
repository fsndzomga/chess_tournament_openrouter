from play_game import play_game
import random
import csv


def run_tournament(model_instances, n_games=5):
    results = {}
    games_played = []  # To track the games played

    # Initialize results for each model
    for model in model_instances:
        results[model.name] = {
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'rating': model.rating
        }

    # Create all possible matchups with alternating colors
    matchups = []
    for i in range(len(model_instances)):
        for j in range(i + 1, len(model_instances)):
            agent1 = model_instances[i]
            agent2 = model_instances[j]
            for game_num in range(n_games):
                if game_num % 2 == 0:
                    matchups.append((agent1, agent2))
                else:
                    matchups.append((agent2, agent1))

    # Shuffle the matchups to randomize the order
    random.shuffle(matchups)

    # Schedule games to prevent models from playing consecutive games
    scheduled_games = []
    while matchups:
        for i, (agent_white, agent_black) in enumerate(matchups):
            if not scheduled_games:
                # Schedule the first game
                scheduled_games.append((agent_white, agent_black))
                matchups.pop(i)
                break
            else:
                last_agents = scheduled_games[-1]
                last_agents_set = {last_agents[0].name, last_agents[1].name}
                current_agents_set = {agent_white.name, agent_black.name}
                # Check if neither agent played in the last game
                if not last_agents_set.intersection(current_agents_set):
                    scheduled_games.append((agent_white, agent_black))
                    matchups.pop(i)
                    break
        else:
            # If no suitable game is found, force the next one
            scheduled_games.append(matchups.pop(0))

    # Play the scheduled games
    for idx, (agent_white, agent_black) in enumerate(scheduled_games):
        print(f"Game {idx + 1} between {agent_white.name} (White) and {agent_black.name} (Black)")
        winner = play_game(agent_white, agent_black)

        # Record the game details
        game_record = {
            'game_number': idx + 1,
            'white': agent_white.name,
            'black': agent_black.name,
            'winner': winner,
            'white_rating': agent_white.rating,
            'black_rating': agent_black.rating
        }
        games_played.append(game_record)
        print(game_record)

        # Update results
        if winner == agent_white.name:
            results[agent_white.name]['wins'] += 1
            results[agent_black.name]['losses'] += 1
        elif winner == agent_black.name:
            results[agent_black.name]['wins'] += 1
            results[agent_white.name]['losses'] += 1
        else:
            results[agent_white.name]['draws'] += 1
            results[agent_black.name]['draws'] += 1

        # Update ratings in the results
        results[agent_white.name]['rating'] = agent_white.rating
        results[agent_black.name]['rating'] = agent_black.rating

    print("\nFinal Results:")
    for model_name, stats in results.items():
        print(f"{model_name}: Wins={stats['wins']}, Losses={stats['losses']}, "
              f"Draws={stats['draws']}, Rating={stats['rating']:.2f}")

    # Save final results to a CSV file
    with open('tournament_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Model Name', 'Wins', 'Losses', 'Draws', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for model_name, stats in results.items():
            writer.writerow({
                'Model Name': model_name,
                'Wins': stats['wins'],
                'Losses': stats['losses'],
                'Draws': stats['draws'],
                'Rating': f"{stats['rating']:.2f}"
            })

    # Optionally return the list of games played
    return games_played
