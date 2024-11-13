from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms import abp_minimax, minimax, random_move, heuristic
from counter import get_count, reset_count

app = Flask(__name__)
CORS(app)


@app.route('/update_grid', methods=['POST'])
def update_list():
    grid = request.json.get('grid')
    algorithm = request.json.get('algorithm')
    reset_count()
    if algorithm == "random":
        random_move(grid)
    elif algorithm == "heuristic":
        heuristic(grid)
    elif algorithm == "minimax":
        minimax(grid)
    elif algorithm == "abp_minimax":
        abp_minimax(grid)
    print(get_count())
    return jsonify(new_grid=grid)

if __name__ == '__main__':
    app.run(debug=True)
