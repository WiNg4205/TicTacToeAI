from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/update_grid', methods=['POST'])
def update_list():
    grid = request.json.get('grid')
    empty_cells = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == " "]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = "X"
    return jsonify(new_grid=grid)

if __name__ == '__main__':
    app.run(debug=True)
