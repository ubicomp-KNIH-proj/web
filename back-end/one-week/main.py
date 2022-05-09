from flask import *
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

# Mongo DB
client = MongoClient('localhost', 27017)
members = mongo.db.members

@app.route('/')
def home():
    return render_template('one_week.html')
    # return render_template('test.html')
    # return render_template('survey.html') #main html
    # return render_template('research.html')

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