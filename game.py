from flask import flask
app = Flask(__name__)

def spcall(qry, param, commit=False):
    try:
        dbo = DBconn()
        cursor = dbo.getcursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            dbo.dbcommit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
    return res


@auth.route('/newplayer/<string:name>/<int:numTri>/<int:numFail>/<int:conTime>', methods=['POST'])
def insertPl(name, tries, fail, time):
    res = spcall("newtopPl", (name, tries, fail, time), True)
    if 'Error' in res[0][0]:
        return jsonify({'status': 'error', 'message': res[0][0]})
    return jsonify({'status': 'ok', 'message': res[0][0]})

@auth.route('/newplayer/<string:name>/<int:numTri>/<int:numFail>/<int:conTime>', methods=['POST'])
def updatePl(name, tries, fail, time):
    res = spcall("updateTopPl", (name, tries, fail, time), True)
    if 'Error' in res[0][0]:
        return jsonify({'status': 'error', 'message': res[0][0]})
    return jsonify({'status': 'ok', 'message': res[0][0]})

@auth.route('/newplayer', methods=['GET'])
def presPl():
    res = spcall('getDetails', ())
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})
    recs = []
    for r in res:
        recs.append({"PlName": r[0], "PlNumTries": r[1], "PlNumFail": str(r[2]), "PlConTime": str(r[3])})
    return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})

@auth.route('/report/<text:name>', methods=['GET'])
def presPl1(name):
    res = spcall('getSpecDetails', (year))
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})
    recs = []
    for r in res:
        recs.append({"PlName": r[0], "PlNumTries": r[1], "PlNumFail": str(r[2]), "PlConTime": str(r[3])})
    return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})

if __name__ == '__main__':
    app.run(debug=True)
