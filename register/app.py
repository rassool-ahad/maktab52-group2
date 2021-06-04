from flask import Flask, render_template, request


class User:
    user_list = []

    def __init__(self, username, fname, lname, password):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password
        User.user_list.append(self)

    def info(self) -> str:
        return f"id={User.user_list.index(self)}\t{self.fname=}\t{self.lname=}\t{self.username=}"


app = Flask(__name__)


@app.route('/', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/', methods=['POST'])
def creat_user():
    form = request.form
    print(form)
    User(**form)
    return "new user created"


@app.route('/<int:id>', methods=['GET'])
def show_user(id):
    u = User.user_list[id]
    return u.info()


@app.route('/list', methods=['GET'])
def show_all_user():
    return render_template("show_all_users.html", users=User.user_list)


if __name__ == '__main__':
    app.run()
