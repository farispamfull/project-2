from flask import Flask, render_template, json, request
from random import sample

app = Flask(__name__)


@app.route('/')
def index():
    with open('data.json', 'r', encoding='utf-8') as f:
        teachers = json.load(f)["teachers"]
    random = sample(teachers, k=6)

    return render_template('index.html', teacher=random)

@app.route("/all/")
def all():
    with open("data.json","r",encoding="utf-8") as f:
        teachers = json.load(f)["teachers"]
    return render_template('all.html',teacher=teachers)




@app.route('/profiles/<int:id>/')
def profile(id):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        teachers = data["teachers"]
        goals = data["goals"]
    teacher = list(filter(lambda x: x['id'] == id, teachers))[0]

    return render_template('profile.html', teacher=teacher, goals=goals)


@app.route('/goals/<goal>/')
def goals(goal):
    goal = goal
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        teachers = data["teachers"]
        goals = data["goals"]
        teachers = list(filter(lambda x: goal in x['goals'], teachers))

    return render_template('goal.html', teacher=teachers, goal=goal, goals=goals)


@app.route('/booking/<int:id>/', methods=['post'])
def booking(id):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        teachers = data["teachers"]
    teacher = list(filter(lambda x: x['id'] == id, teachers))[0]
    week = {"mon": "Понедельник", "tue": "Вторник", "wed": "Среда", "thu": "Четверг", "fri": "Пятница",
            "sat": "Суббота", "sun": "Воскресенье"}
    times = request.form.get("time").split()
    day = week[times[1]]
    time = times[0]

    return render_template('booking.html', day=day, time=time, teacher=teacher)


@app.route('/booking_done/', methods=['post'])
def booking_done():
    teacher = request.form.get('teacher')
    time = request.form.get('time')
    day = request.form.get('day')
    number = request.form.get("clientPhone")
    name = request.form.get('clientName')
    to_json = {'teacher': teacher, "name": name, "day": day, "time": time, "phone": number}
    with open('booking.json', "r", encoding='utf-8') as f:
        a = json.load(f)
        a += [to_json]
    with open('booking.json', "w", encoding='utf-8') as f:
        json.dump(a, f, indent=4, ensure_ascii=False)

    return render_template("booking_done.html", time=time, day=day, number=number, name=name)


@app.route('/request/', methods=["post", "get"])
def requested():
    if request.method == 'GET':
        return render_template('request.html')
    time = request.form.get('time')
    goal = request.form.get('goal')
    phone = request.form.get('phone')
    name = request.form.get('name')
    to_json = {'name': name, 'phone': phone, 'goal': goal, "time": time}
    with open('request.json', "r", encoding='utf-8') as f:
        a = json.load(f)
        a += [to_json]
    with open('request.json', "w", encoding='utf-8') as f:
        json.dump(a, f, indent=4, ensure_ascii=False)

    return render_template('request_done.html', goal=goal, time=time, phone=phone, name=name)


if __name__ == '__main__':
    app.run()
