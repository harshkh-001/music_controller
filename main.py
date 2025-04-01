from flask import Flask, render_template, request, jsonify, session, redirect , url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import random
from spotify_data import sp
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
# current_playback = sp.current_playback()
# if current_playback and current_playback['item']:
#     current_track = current_playback['item']
#     song_name = current_track['name']
#     singer_name = ','.join(artist['name'] for artist in current_track['artists'])
#     print(song_name,singer_name)
# else:
#     print("no song is playing")

class Votes(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    code = db.Column(db.String(6), unique=True, nullable=False)
    # user_id = db.Column(db.String , unique=True, nullable=False)
    current_votes = db.Column(db.Integer , default=0)
    
    
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
    # if not sp_oauth.validate_token(cache_handler.get_cached_token()):
    #     auth_url = sp_oauth.get_authorize_url()
    #     return redirect(auth_url)
    # return redirect(url_for('get_playlists'))
    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("createroom.html")

# @app.route('/callback')
# def callback():
#     sp_oauth.get_access_token(request.args['code'])
#     return redirect(url_for('get_playlists'))

# @app.route('/get_playlists')
# def get_playlists():
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
    
#     playlists = sp.current_user_playlists()
#     playlists_info = [(pl['name'], pl['external_urls']['spotify'], pl['uri']) for pl in playlists['items']]
#     playlists_html = '<br>'.join([f"{name}: {url} : {uri}" for name,url,uri in playlists_info])
#     print("start\n")
#     song_uri = random.choice(playlists_info)[2]
#     sp.start_playback(song_uri)
#     print("\n end")
#     # sp.start_playback()
#     return playlists_html


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for('home'))
    
@app.route("/create-room", methods=["POST"])
def create_room():
    vote_to_skip = request.json.get('vote_to_skip')
    session["host"] = request.remote_addr  # Track host IP
    current_song = song_name
    room_code = generate_room_code()
    new_room = Room(code=room_code, votes_to_skip=int(vote_to_skip), host=session["host"])
    new_room_votes = Votes(code=room_code)
    db.session.add(new_room)
    db.session.add(new_room_votes)
    db.session.commit()
    return jsonify({"room_code": room_code})

@app.route("/room/<roomcode>")
def room(roomcode):
    room = Room.query.filter_by(code=roomcode).first()
    if(room):
        current_playback = sp.current_playback()
        if current_playback and current_playback['item']:
            current_track = current_playback['item']
            song_name = current_track['name']+' by '
            singer_name = ','.join(artist['name'] for artist in current_track['artists'])
            print(song_name,singer_name)
        else:
            # print("no song is playing")
            song_name = "None"
            singer_name = ""
        room_vote = Votes.query.filter_by(code=room.code).first()
        print(room.votes_to_skip)
        roomdata = {
            "room_code":room.code,
            "Vote_to_skip":room.votes_to_skip,
            "current_song":song_name+singer_name ,
            "host":room.host,
            "current_votes":room_vote.current_votes
        }
        return render_template("room.html",room=roomdata)
     
    return "error in finding room pls enter correct room code"

@app.route("/inc-vote" , methods=["POST"])
def inc_vote():
    print("hello")
    data = request.get_json()  
    room_code = data.get('room_Code') 
    # user_id = data.get('user_id')
    # vote_to_change = data.get('vote_to_change') 
    # print(vote_to_change)

    # if vote_to_change is True:
    room_vote = Votes.query.filter_by(code=room_code).first()
    if room_vote: 
        room_vote.current_votes += 1  
        db.session.commit() 

        return jsonify({"current_votes":room_vote.current_votes})
    else:
        return jsonify({"error": "Room not found"}), 404  


@app.route("/join-room", methods=["POST"])
def join_room():
    data = request.json
    room = Room.query.filter_by(code=data["code"]).first()
    if room:
        return jsonify({"message": "Joined successfully", "room": room.code})
    return jsonify({"error": "Invalid room code"}), 400

if __name__ == "__main__":
    # print("hello")
    with app.app_context():  # Ensure Flask knows which app to use
        db.create_all()  # Create missing tables
    socketio.run(app, debug=True)

