import flask
from flask import Flask
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from twilio.rest import Client
import random
from time import sleep

app = Flask(__name__)

# Substitute your Twilio AccountSid and ApiKey details
# AC0237d34614765b296305be28392600fb
ACCOUNT_SID = 'AC0237d34614765b296305be28392600fb' # ???
AUTH_TOKEN = '1098fc0165aee1baced956ccd82dc3fd'
API_KEY_SID = 'SKf4235e61e171a4bfb2e098b2a708cb21'
API_KEY_SECRET = 'i46QxVuJKZ38LuewwpTDzkn5nbeMwXPH'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/createRoom/<name>/')
def createRoom(name):
    room = client.video.rooms.create(
                                type='peer-to-peer',
                                unique_name=name
                            )
    print(room.sid) # cannot make a room with the same name
    return room.sid

@app.route('/joinRoom/<name>/')
def joinRoom(name):
    room = client.video.rooms(name).fetch()
    return room.unique_name

@app.route('/completeRoom/<name>/')
def completeRoom(name):
    room = client.video.rooms(name).update(status='completed')
    return room.unique_name

@app.route('/workflow/<name>/')
def workflow(name):
    createRoom(name)
    joinRoom(name)
    sleep(5)
    return completeRoom(name)
    

@app.route('/getToken/<room>/')
def getToken(room):

    # Create an Access Token
    token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET)

    username = 'foobar' + str(random.randint(0, 100))
    # Set the Identity of this token
    token.identity = username

    # Grant access to Video
    grant = VideoGrant(room=room)
    token.add_grant(grant)

    # Serialize the token as a JWT
    jwt = token.to_jwt()
    print(jwt)
    return jwt

if __name__ == "__main__":
    app.run(debug=True)