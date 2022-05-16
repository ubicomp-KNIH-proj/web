from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash
from bson.json_util import dumps
from sqlalchemy import JSON

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

# Mongo DB
client = MongoClient('localhost', 27017)
members = mongo.db.members
result = mongo.db.survey_result

@app.route('/')
def home():
    return render_template('one_week.html')
    # return render_template('yaho.html')
    # return render_template('test.html')
    # return render_template('survey.html') #main html
    # return render_template('research.html')

@app.route('/ajax', methods=['GET', 'POST'])
def ajax():
    data = request.get_json()
    # print(data)
    keyList = data.keys()
    # print(data.keys())
    # print(data.items())
    # print(data.values())
    #생활습관 설문조사 결과 {'name':~, 'value':} 형태
    q1 = list(data.values())[0][0:2]
    print('q1',q1)
    q2 = list(data.values())[0][2]
    print('q2',q2)
    q3 = list(data.values())[0][3]
    print('q3',q3)
    q4 = list(data.values())[0][4]
    print('q4',q4)
    q5 = list(data.values())[0][5]
    print('q5',q5)
    q6 = list(data.values())[0][6:15]
    print('q6',q6)
    q7 = list(data.values())[0][16]
    print('q7',q7)
    q8 = list(data.values())[0][17]
    print('q8',q8)
    q9 = list(data.values())[0][18]
    print('q9',q9)
    #정신건강 설문조사 결과 {'name':~, 'value':} 형태
    mq1 = list(data.values())[1][0]
    print('mental-q1',mq1)
    mq2 = list(data.values())[1][1]
    print('mental-q2',mq2)
    mq3 = list(data.values())[1][2]
    print('mental-q3',mq3)
    mq4 = list(data.values())[1][3]
    print('mental-q4',mq4)
    # for item in keyList:
    #     print('Key:',item, 'Value:',data[item])
    # members.insert_one(data)
    #request.get_json()를 통해 받아 data에 넣기
    members.insert_one(q2)
    return jsonify(result = "success", result2= data)

#회원가입
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        # return render_template("register_test.html")
        return render_template("register.html")
    else:
        name = request.form.get("name", type=str)
        id = request.form.get("id", type=str)
        pwd = request.form.get("pwd", type=str)
        pwd2 = request.form.get("pwd2", type=str)
        
        current_utc_time = round(datetime.datetime.utcnow().timestamp() * 1000)
        post = {
            "name": name,
            "id": id,
            "password": pwd,
            "register_date": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }

        if not (id and pwd and pwd2):
            return "모두 입력해주세요"
        elif pwd != pwd2:
            return "비밀번호를 확인해주세요."
        else:
            members.insert_one(post)
            # return "회원가입 완료"
            # flash("회원가입 완료")
            # return render_template("login_test.html")
            return render_template("login.html")

#로그인
@app.route('/user/login', methods = ['POST'])
def login():
    id = request.form['id']
    pwd = request.form['pwd']
    print(id)
    print(pwd)

    user = members.find_one({'id':id}, {'pwd':pwd})
    if user is None:
        return jsonify({'login':False})
    else:
        # flash("로그인 완료") #flash 안 뜸
        resp = jsonify({'login':True})
        return resp

@app.route('/survey/day', methods=['POST'])
def post_survey():
    # s1 = request.form["s1"]
    s2 = request.json()
    # print(s1)
    print(s2)
    return render_template("survey.html")
