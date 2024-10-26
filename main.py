from tournament import run_tournament
from chess_model import ChessModel
from models import models

model_instances = []
for model_info in models:
    model = ChessModel(model_info['name'], model_info['provider'], model_info['model_id'])
    model.rating = model_info['rating']
    model_instances.append(model)

n_games = 3  # Number of games to play between each pair of models
run_tournament(model_instances, n_games)
