from flask import Flask, request
from flask_cors import CORS

import database
import user
import stats
import json


app = Flask(__name__)
CORS(app)
dev_link = "mongodb+srv://tgrogers1221:C5WAvei0gMlYLUuW@cluster0.sp6ibvg.mongodb.net/?retryWrites=true&w=majority"
db = database.cluster_connect(dev_link)



def get_stats_single(time_frame, user_email):
    response = {}
    difficulties = ["beginner", "intermediate", "advanced"]
    for diff in difficulties:
        response[diff] = {"attempted": 0, "correct": 0}

    if time_frame == "day":
        user_stats = stats.get_day_stats(db, user_email)
    elif time_frame == "week":
        user_stats = stats.get_week_stats(db, user_email)
    elif time_frame == "month":
        user_stats = stats.get_month_stats(db, user_email)
    elif time_frame == "3month":
        user_stats = stats.get_3month_stats(db, user_email)
    elif time_frame == "6month":
        user_stats = stats.get_6month_stats(db, user_email)
    else:
        user_stats = stats.get_global_stats(db, user_email)
    
    if user_stats:
        for diff_map in user_stats.values():
            print(diff_map)
            for diff, tup in diff_map.items():
                response[diff]["attempted"] += tup[0]
                response[diff]["correct"] += tup[1]

    data = json.dumps({
        'email': user_email,
        'stats': response,
    })
    return data

def get_stats_export():

    emails = user.get_existing_users(db)
    response = {}

    difficulties = ["beginner", "intermediate", "advanced"]
    for user_email in emails:
        response[user_email] = {}

        for diff in difficulties:
            response[user_email][diff] = {"attempted": 0, "correct": 0}

        user_stats = stats.get_global_stats(db, user_email)
        if user_stats:
            for diff_map in user_stats.values():
                for diff, tup in diff_map.items():
                    response[user_email][diff]["attempted"] += tup[0]
                    response[user_email][diff]["correct"] += tup[1]

    data = json.dumps({
        'stats': response,
    })
    return data

@app.route("/stats", methods=['GET'])
def get_stats():

    export = request.args.get('export', default='false', type=str)
    user_email = request.args.get('email', default='guest', type=str)
    time_frame = request.args.get('timeframe', default='', type=str)

    if export == 'true':
        return get_stats_export()

    return get_stats_single(time_frame, user_email)
    
@app.route("/stats", methods=['POST'])
def update_stat():
    user_email = request.args.get('email', default='guest', type=str)

    data = request.get_json()

    diff = data['difficulty']
    correct = data['correct']
    stats.increment_global_stats(db, user_email, diff, correct)
    return { "status": "success"}

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    if (user.valid_login(db, email, password)):
        return { "status": "success" }

    return { "status": "failure" }

@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if (user.create_user(db, email, password)):
        return { "status": "success" }  
    
    return { "status": "failure" }


if __name__ == "__main__":
    app.run(port=5001)