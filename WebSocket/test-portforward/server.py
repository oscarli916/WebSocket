import eventlet

eventlet.monkey_patch()
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send, emit
import time
import random
import odds
import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @socketio.on('connect')
# def test_connect():
#     print


connected = []


@socketio.on('connect_id')
def connect_id(id):
    print("\nClient connected. ID: " + str(id) + "\n")
    connected.append(id)
    print("Current Client: " + str(connected) + "\n")


@socketio.on('client-disconnect')
def disconnect_id(id):
    print("\nClient disconnected. ID: " + str(id) + "\n")
    index = connected.index(id)
    connected.pop(index)
    print("Current Client: " + str(connected) + "\n")


start = 0


@socketio.on('connect')
def test_connect():
    global start
    if start == 0:
        socketio.start_background_task(get_odd)
        start = 1


def recommend():
    socketio.emit('recommend', [["1"], ["推薦:6>3,4,13"], ["留意:1,5,7,14"]])


def get_odd():
    # odd = [[13.0, 7.18, 7.68, 3.7, 19.61, 17.35, 10.0, 7.76, 7.98, 10.0, 7.88, 8.16, 47.0, 2.04, 2.4, 5.8, 15.5,
    # 14.82, 120.0, 0.87, 1.11, 32.0, 3.51, 4.29, 3.9, 19.39, 17.97, 13.0, 6.2, 6.8, 16.0, 5.78, 6.56, 22.0, 4.27,
    # 4.88], [13.0, 7.18, 7.68, 3.7, 19.61, 17.35, 10.0, 7.76, 7.98, 10.0, 7.88, 8.16, 47.0, 2.04, 2.4, 5.8, 15.5,
    # 14.82, 120.0, 0.87, 1.11, 32.0, 3.51, 4.29, 3.9, 19.39, 17.97, 13.0, 6.2, 6.8, 16.0, 5.78, 6.56, 22.0, 4.27,
    # 4.88]]

    odd = [[], [], [], [], [], [], [], [], [], [], []]
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H%M")
        odds.get_start_time()
        # If current time > start time + 3 minutes then stop
        if int(float(current_time)) > int(odds.starttime) + 3:
            break
        else:
            try:
                win_list = odds.get_win_odd()
                # print(win_list)
                Q_Ans, P_Ans = odds.get_QP_odd()
            except:
                pass

            temp = []
            for i in range(len(win_list)):
                temp.append(win_list[i])
                temp.append(Q_Ans[i])
                temp.append(P_Ans[i])
            odd[1] = temp  # Update odd[1] in every time
            if len(odd[0]) == 0:
                noh = int(len(temp) / 3)
                for i in range(noh):
                    odd[0].append(str(i + 1) + ".")
                    odd[0].append('入Q%')
                    odd[0].append('入P%')
            # print(odds.starttime)  # 1845
            # print(current_time)  # 0056
            # print(int(odds.starttime) - int(current_time))
            if int(odds.starttime) - int(current_time) >= 41:
                current_time = int(current_time) + 40
            if int(odds.starttime) - int(current_time) == 40 and 0 <= datetime.datetime.now().second < 9:
                odd[9] = temp
            elif int(odds.starttime) - int(current_time) == 30 and 0 <= datetime.datetime.now().second < 9:
                odd[8] = temp
            elif int(odds.starttime) - int(current_time) == 25 and 0 <= datetime.datetime.now().second < 9:
                odd[7] = temp
            elif int(odds.starttime) - int(current_time) == 20 and 0 <= datetime.datetime.now().second < 9:
                odd[6] = temp
            elif int(odds.starttime) - int(current_time) == 15 and 0 <= datetime.datetime.now().second < 9:
                odd[5] = temp
            elif int(odds.starttime) - int(current_time) == 10 and 0 <= datetime.datetime.now().second < 9:
                odd[4] = temp
            elif int(odds.starttime) - int(current_time) == 5 and 0 <= datetime.datetime.now().second < 9:
                odd[3] = temp
            elif int(odds.starttime) - int(current_time) == 3 and 0 <= datetime.datetime.now().second < 9:
                odd[2] = temp
            socketio.emit('odd_table', odd)
            print(odd, current_time, odds.starttime)  # Print emit msg in server For debug
            print()
            time.sleep(3)
            # If no result check if condition < > and render template


if __name__ == '__main__':
    socketio.run(app, debug=True, host="192.168.0.132", port="5050")
