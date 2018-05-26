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
        output.append({'unicode':q['unicode'],'nickname':q['nickname']})


#    q = collec.find_one({'unicode':'U+1F600'})
#    output = {'nickname' : q['nickname'],
#    'danceability' : q['danceability'],
#    'energy' : q[energy]}

    # "danceability": 0.6,
    # "energy": 0.5,
    # "liveness": 0.3,
    # "loudness": 0.7,
    # "mode": 1,
    # "nickname": "grinning face",
    # "popularity": 75,
    # "unicode": "U+1F600",
    # "valence": 0.7

    return flask.jsonify(output)

@app.route('/emojicollection/<myunicodes>', methods=['GET'])
def get_an_emoji(myunicodes):
    listofUnicodes = myunicodes.split('_')
    emotionList = []
    danceability=energy=liveness=loudness=valence=popularity = 0.0
    positivemodecount = 0
    myemojicollection = mongo.db.emojicollection

    for singleUnicode in listofUnicodes:
        q = myemojicollection.find_one({'unicode':singleUnicode})
        if q is None:
            return 'nothing found'
        else:
            emotionList.append({'unicode':q['unicode'],
            'nickname':q['nickname'],
            'danceability':q['danceability'],
            'energy':q['energy'],
            'liveness':q['liveness'],
            'loudness':q['loudness'],
            'mode':q['mode'],
            'popularity':q['popularity'],
            'valence':q['valence']});

    for emotion in emotionList:
        danceability += emotion['danceability']
        energy += emotion['energy']
        loudness += emotion['loudness']
        liveness += emotion['liveness']
        valence += emotion['valence']
        popularity += emotion['popularity']
        if emotion['mode'] == 1:
            positivemodecount += 1

#fix loudness
    length = len(emotionList)
    return flask.jsonify(
        {'danceability':danceability/length,
        'energy':energy/length,
        'liveness':liveness/length,
        'loudness':loudness/length,
        'valence':valence/length,
        'popularity':popularity/length}
    )
