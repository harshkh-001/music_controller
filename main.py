from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import random
import secrets
import os
import string

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
app.config["SQLALCHEMY_ECHO"] = True
socketio = SocketIO(app)
db = SQLAlchemy(app)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False)
    votes_to_skip = db.Column(db.Integer, nullable=False)
    current_song = db.Column(db.String(100), nullable=True)
    host = db.Column(db.String(50), nullable=False)

def generate_room_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=6))
        exist_room = Room.query.filter_by(code=code).first()
        if not (exist_room):
            return code

@app.route("/")
def home():
    # return "hello"
    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("createroom.html")


@app.route("/create-room", methods=["POST"])
def create_room():
    vote_to_skip = request.json.get('vote_to_skip')
    session["host"] = request.remote_addr  # Track host IP
    room_code = generate_room_code()
    new_room = Room(code=room_code, votes_to_skip=int(vote_to_skip), host=session["host"])
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"room_code": room_code})

@app.route("/room/<roomcode>")
def room(roomcode):
    room = Room.query.filter_by(code=roomcode).first()
    if(room):
        print(room.votes_to_skip)
        roomdata = {
            "room_code":room.code,
            "Vote_to_skip":room.votes_to_skip,
            "current_song":room.current_song ,
            "host":room.host
        }
        return render_template("room.html",room=roomdata)
     
    return "error in finding room pls enter correct room code"

@app.route("/join-room", methods=["POST"])
def join_room():
    data = request.json
    room = Room.query.filter_by(code=data["code"]).first()
    if room:
        return jsonify({"message": "Joined successfully", "room": room.code})
    return jsonify({"error": "Invalid room code"}), 400

if __name__ == "__main__":
    print("hello")
    with app.app_context():  # Ensure Flask knows which app to use
        db.create_all()  # Create missing tables
    socketio.run(app, debug=True)

