from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import time
import random
import odds
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


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


@socketio.on('connect')
def test_connect():
    socketio.start_background_task(get_odd)


def get_odd():
    # count = 1
    # while count <= 10:
    #     number = random.randint(1, 10)
    #     print(number)
    #     socketio.emit('send_odd', number)
    #     socketio.sleep(1)

    # odd = [[13.0, 7.18, 7.68, 3.7, 19.61, 17.35, 10.0, 7.76, 7.98, 10.0, 7.88, 8.16, 47.0, 2.04, 2.4, 5.8, 15.5,
    # 14.82, 120.0, 0.87, 1.11, 32.0, 3.51, 4.29, 3.9, 19.39, 17.97, 13.0, 6.2, 6.8, 16.0, 5.78, 6.56, 22.0, 4.27,
    # 4.88], [13.0, 7.18, 7.68, 3.7, 19.61, 17.35, 10.0, 7.76, 7.98, 10.0, 7.88, 8.16, 47.0, 2.04, 2.4, 5.8, 15.5,
    # 14.82, 120.0, 0.87, 1.11, 32.0, 3.51, 4.29, 3.9, 19.39, 17.97, 13.0, 6.2, 6.8, 16.0, 5.78, 6.56, 22.0, 4.27,
    # 4.88]]

    odd = [[]]
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H%M")
        odds.get_start_time()
        # If current time > start time + 3 minutes then stop
        if int(float(current_time)) > int(odds.starttime) + 3:
            break
        else:
            win_list = odds.get_win_odd()
            # print(win_list)
            Q_Ans, P_Ans = odds.get_QP_odd()

            temp = []
            for i in range(len(win_list)):
                temp.append(win_list[i])
                temp.append(Q_Ans[i])
                temp.append(P_Ans[i])
            odd[0] = temp
            if datetime.datetime.now().minute % 1 == 0 and 0 <= datetime.datetime.now().second < 5:
                odd.insert(1, temp)
            socketio.emit('odd_table', odd)
            time.sleep(5)



if __name__ == '__main__':
    socketio.run(app, debug=True, host="192.168.0.132", port="5000")
