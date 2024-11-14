import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithms import abp_minimax, minimax, random_move, heuristic
from counter import get_count, reset_count

app = Flask(__name__)
CORS(app)


@app.route('/update_grid', methods=['POST'])
def update_list():
    start_time = time.time()
    
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

    end_time = time.time()
    runtime = end_time - start_time
    runtime = round(runtime * 1000, 2)
    
    return jsonify(new_grid=grid, count=get_count(), runtime=runtime)

if __name__ == '__main__':
    app.run(debug=True)
