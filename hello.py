import flask
from flask_pymongo import PyMongo

app = flask.Flask(__name__)

app.config['MONGO_DBNAME'] = 'emojistoemotionsdatabase'
app.config['MONGO_URI'] = 'mongodb://seto:123@ds235860.mlab.com:35860/emojistoemotionsdatabase'
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Insert query!'

@app.route('/emojicollection', methods=['GET'])
def get_all_emoji():

    myemojicollection = mongo.db.emojicollection
    output = []

    for q in myemojicollection.find():
        output.append({'unicode':q['unicode'],'nickname':q['nickname'], 'danceability':q['danceability']})


#    q = collec.find_one({'unicode':'U+1F600'})
#    output = {'nickname' : q['nickname'],
#    'danceability' : q['danceability'],
#    'energy' : q[energy]}

    return flask.jsonify({'result':output})

@app.route('/emojicollection/<myunicode>', methods=['GET'])
def get_an_emoji(myunicode):

    myemojicollection = mongo.db.emojicollection
    q = myemojicollection.find_one({'unicode':myunicode})
    output = {
    'unicode':q['unicode'],
    'nickname':q['nickname'],
    'danceability':q['danceability']}

    return flask.jsonify(output)
