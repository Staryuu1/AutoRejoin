from flask import Flask, request, jsonify
import json
from datetime import datetime, timedelta
import os
import threading
import time

app = Flask(__name__)

user_data = {}
def launch_roblox_with_private_server(private_server_link, username):
    packagename = user_data.get(username, {}).get('packagename')
    if packagename:
        cmd = f"am start -a android.intent.action.VIEW -d '{private_server_link}' {packagename}"
        os.system(cmd)
        print(f"Launched Roblox game with ps: {private_server_link} for user: {username}")
    else:
        print(f"Package name not found for user: {username}")

def launch_roblox(game_id, username):
    packagename = user_data.get(username, {}).get('packagename')
    if packagename:
        url = f"roblox://placeID={game_id}"
        cmd = f"am start -a android.intent.action.VIEW -d '{url}' {packagename}"
        os.system(cmd)
        print(f"Launched Roblox game with ID: {game_id} for user: {username}")
    else:
        print(f"Package name not found for user: {username}")

@app.route('/updatetime', methods=['POST'])
def update_time():
    username = request.json.get('username')
    print(f"Received update_time request for user: {username}")
    if username in user_data:
        user_data[username]['last_update'] = str(datetime.now())
        print(f"Time updated for user: {username} with time {user_data[username]['last_update']}")
        return jsonify({"message": f"Time updated for user: {username}"}), 200
    else:
        print(f"User '{username}' not found")
        return jsonify({"error": f"User '{username}' not found"}), 404

@app.route('/adduser', methods=['POST'])
def add_user():
    username = request.json.get('username')
    packagename = request.json.get('packagename')
    game_id = request.json.get('game_id')
    is_ps = request.json.get('is_ps')
    ps = request.json.get("private_link")
    
    if not username or not packagename or not game_id:
        print("Missing required fields: username, packagename, and game_id are required")
        return jsonify({"error": "Username, packagename, and game_id are required"}), 400
    
    if username in user_data:
        print(f"User '{username}' already exists")
        return jsonify({"error": f"User '{username}' already exists"}), 409
    
    user_data[username] = {
        'packagename': packagename,
        'game_id': game_id,
        'ps_link': ps,
        'is_ps': is_ps,
        'last_update': str(datetime.now())
    }
    print(f"User added: {username}")
    return jsonify({"message": f"User '{username}' added successfully"}), 201

def check_inactive_users():
    print("Starting check_inactive_users thread...")
    while True:
        time.sleep(60)  
        now = datetime.now()
        inactive_users = []
        for username, data in user_data.items():
            last_update = datetime.strptime(data['last_update'], '%Y-%m-%d %H:%M:%S.%f')
            if now - last_update > timedelta(minutes=1):
                print(f"User Inactive: '{username}'")
                inactive_users.append(username)
        
        for user in inactive_users:
            print(f"User {user} has been inactive for more than 5 minutes")
            if user_data[user]['is_ps'] == True :
                launch_roblox_with_private_server(user_data[user]['ps_link'], user)
            else:
                launch_roblox(user_data[user]['game_id'], user)

            user_data[user]['last_update'] = str(datetime.now())
        print("Inactive users checked.")



thread = threading.Thread(target=check_inactive_users, daemon=True)
thread.start()
print("Background thread started.")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6969)
