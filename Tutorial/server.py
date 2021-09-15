from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


# Run test_connect() when client connected to server
# Show "User has connected" in server terminal
@socketio.on('connect')
def test_connect():
    # print("User has connected")
    pass


# Run test_disconnect() when client disconnected to server
# Show "Client disconnected" in server terminal
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

@socketio.on("client-disconnecting")
def client_disconnecting(id):
    print("\nUser: " + str(id) + " is disconnected \n\n")
    index = connected.index(id)
    connected.pop(index)
    print("Current Users: " + str(connected))
    print()


# Listen for client. When msg is sent from client, run handle_message
@socketio.on("message")
def handle_message(message):
    print("Recevied message: " + message)
    # Send the message to all the client (broadcast = True)
    send(message, broadcast=True)


connected = []


@socketio.on("id")
def handle_id(id):
    print("\nUser has connected. ID: " + str(id) + "\n\n")
    connected.append(id)
    print("Current Users: " + str(connected))
    print()


if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, debug=True, host="192.168.0.132", port="5000")
