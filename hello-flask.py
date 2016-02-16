from flask import Flask, render_template, url_for, json, request, Response
import datetime, os, subprocess
from take_picture import takePicture
from flask_httpauth import HTTPBasicAuth
from list_files import listFiles

app = Flask(__name__, static_url_path='/static')
auth = HTTPBasicAuth()

users = {
    "user1": "pass1",
    "user2": "pass2",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

def run_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return p

@app.route("/")
def hello():
    now = datetime.datetime.now()
    rootDir = os.path.dirname(os.path.abspath(__file__))
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'rootdir': rootDir,
        }
    return render_template('main.html', **templateData)

@app.route("/takepic")
@auth.login_required
def takePic():
    templateData = {
        'title' : 'Take A Pic',
        'urlTakePicApi': url_for('takePicApi'),
        'urlList': url_for('list'),
        }
    return render_template('takepic.html', **templateData)


@app.route('/takepicapi', methods = ['POST'])
def takePicApi():

    if request.headers['Content-Type'] == 'application/json':
        try:
            request.json['picQuality']
        except:
            return "json message not accepted"

        rootDir = os.path.dirname(os.path.abspath(__file__))
        fileName = 'picam_ondemand_'+ datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
        fileName = os.path.join(rootDir, 'static/', fileName)
        
        if request.json['picQuality'] == 'low':
            takePicture(fileName, 'low')
        else:
            takePicture(fileName, 'high')

        urlImg = url_for('static', filename=os.path.basename(fileName))
        js = json.dumps({'urlImg':urlImg})
        
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://luisrei.com'
        return resp
    else:
        return "415 Unsupported Media Type ;)"

@app.route('/messages', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'application/json':
        js = json.dumps(request.json)
        print js, type(js), len(js), type(request.json), len(request.json)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://luisrei.com'
        return resp
    else:
        return "415 Unsupported Media Type ;)"

@app.route("/load")
@auth.login_required
def load():
    rootDir = os.path.dirname(os.path.abspath(__file__))
    fileName = 'picam_ondemand_'+ datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
    fileName = os.path.join(rootDir, 'static/', fileName)

    takePicture(fileName, 'low')

    urlImg = url_for('static', filename=os.path.basename(fileName))

    response =  'Take shots for the monitoring environment.'
    templateData = {
        'title' : 'Pi monitoring',
        'response': response,
        'urlImg': urlImg,
        'urlList': url_for('list'),
        }
    return render_template('load.html', **templateData)

@app.route("/list")
@auth.login_required
def list():
    rootDir = os.path.dirname(os.path.abspath(__file__))
    staticDir = os.path.join(rootDir, 'static/')
    listFileNames = listFiles(staticDir)
    
    response = []
    for fn in listFileNames:
        data = {'filename': fn, 'url': url_for('static', filename=fn)}
        response.append(data)

    templateData = {
        'title' : 'Pics We Have',
        'response': response,
        'urlTakePic': url_for('takePic')
        }
    return render_template('list.html', **templateData)


if __name__ == "__main__":
    #load, err = run_command('cat /proc/loadavg')
    #print load
    app.run(host='0.0.0.0', port=8080, debug=True)
