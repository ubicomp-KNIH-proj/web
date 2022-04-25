from flask import *
from flask_pymongo import PyMongo
import datetime
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = "2019"
app.config["MONGO_URI"] = "mongodb://localhost:27017/survey"
mongo = PyMongo(app)

@app.route('/register', methods=["GET", "POST"])
def member_register():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        id = request.form.get("id", type=str)
        pwd = request.form.get("pwd", type=str)
        pwd2 = request.form.get("pwd2", type=str)

        if name == "" or id == "" or pwd  == "" or pwd2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("register_test.hmtl")
        
        if pwd != pwd2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("register_test.html")

        members = mongo.db.members
        # cnt = members.find({"id": id}).count()
        # if cnt > 1:
        #     flash("중복된 ID입니다.")
        #     return render_template("register_test.html")

        current_utc_time = round(datetime.datetime.utcnow().timestamp() * 1000)
        post = {
            "name": name,
            "id": id,
            "password": pwd,
            "register_date": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }
        members.insert_one(post)
        flash("회원가입 완료")
        return render_template("login.html")
    else:
        return render_template('register_test.html')

if __name__ == "__main__":
    app.run()
