from flask import Flask, request
from executor import Executor
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

@app.route("/")
def get_problem():

    difficulty_map = {
        'beginner': 'easy',
        'intermediate': 'medium',
        'advanced': 'hard',
    }

    difficulty = request.args.get('difficulty', default='beginner', type=str)
    difficulty = difficulty_map[difficulty]
    executor = Executor()
    data = json.dumps(executor.generate(difficulty))
    return data

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()