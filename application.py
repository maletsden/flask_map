import main

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("form.html")


@app.route('/nickname', methods=['POST'])
def handle_data():
    nickname = request.form['nickname']
    limit = request.form['limit']
    msg = main.init(nickname, limit)

    # this mean that there is no user with given nickname
    if msg:
        return render_template("unknown.html", nickname=nickname)

    return render_template("Map.html")

if __name__ == '__main__':
    app.run(debug=True)
