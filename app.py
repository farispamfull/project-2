from flask import Flask, render_template, json, request,redirect, url_for,flash,session
from random import sample
from flask.json import jsonify
from flask_wtf import FlaskForm
from form import BookingForm,RequestForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate






app = Flask(__name__)

app.config.update({
    'SECRET_KEY': 'asdasdasd',
    'DEBUG': True,

})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
migrate = Migrate(app, db)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    about=db.Column(db.Text,nullable=False)
    rating=db.Column(db.Float,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    picture=db.Column(db.String,nullable=False)
    free=db.Column(db.Text,nullable=False)



teacher_goal=db.Table('teacher_goal',
        db.Column('teacher_id',db.Integer,db.ForeignKey('teachers.id')),
        db.Column('goal_id',db.Integer,db.ForeignKey('goals.id'))
        )

class Goal(db.Model):
    __tablename__='goals'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    teachers=db.relationship('Teacher',secondary=teacher_goal,backref='goals')


class Booking(db.Model):
    __tablename__='bookings '
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    phone=db.Column(db.String,nullable=False)
    teacher_id=db.Column(db.Integer,db.ForeignKey('teachers.id'),nullable=False)
    teacher=db.relationship('Teacher',backref='bookings')


class Application(db.Model):
    __tablename__='applications'
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.String,nullable=False)
    name=db.Column(db.String,nullable=False)
    phone=db.Column(db.String,nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)
    goal = db.relationship('Goal', backref='applications')


@app.route('/')
def index():
    print(request.path.endswith('/'))
    print(request.path)
    raw_teachers=Teacher.query.all()
    teachers=sorted(sample(raw_teachers,k=6),
                    key=lambda teacher:teacher.rating,
                    reverse=True)

    return render_template('index.html', teachers=teachers)

@app.route("/all/")
def all():
    teachers=Teacher.query.order_by(Teacher.rating.desc())

    return render_template('all.html',teachers=teachers)




@app.route('/profiles/<int:id>/')
def profile(id):
    teacher=Teacher.query.get_or_404(id)
    calendar = json.loads(teacher.free)
    return render_template('profile.html', teacher=teacher,goals=teacher.goals,calendar=calendar)


@app.route('/goals/<goal>/')
def goals(goal):
    self_goal = Goal.query.filter(Goal.name==goal).first_or_404()
    print(request.path.endswith('/'))
    print(request.path.endswith(url_for('goals',goal=goal)))
    print(request.referrer)
    print(request.base_url)
    teachers=sorted(self_goal.teachers,
                    key=lambda teacher:teacher.rating,
                    reverse=True)

    return render_template('goal.html',teacher=teachers,goal=goal)


# class BookingForm(FlaskForm):
#     name = StringField('Вас зовут', validators=[DataRequired()])
#     phone = StringField('Ваш телефон', validators=[DataRequired(), ru_phone])
#     submit = SubmitField('Записаться на пробный урок')


@app.route('/booking/<int:teacher_id>/',methods=['POST','GET'])
def booking(teacher_id):
    form=BookingForm()
    week = {"mon": "Понедельник",
            "tue": "Вторник",
            "wed": "Среда",
            "thu": "Четверг",
            "fri": "Пятница",
            "sat": "Суббота",
            "sun": "Воскресенье"}

    raw_day=request.args.get('day')
    day=week[raw_day]
    time=request.args.get('time')
    teacher=Teacher.query.get_or_404(teacher_id)

    if request.method == "POST" and form.validate_on_submit():
        session['booking'] = {'teacher':teacher.id,
                              "day":day,
                              "time":time,
                              "name":form.name.data,
                              "phone":form.phone.data}

        return redirect(url_for('booking_done'))

    return render_template('booking.html',day=day,time=time,teacher=teacher,form=form,days=raw_day)


@app.route('/booking_done/', methods=['POST',"GET"])
def booking_done():
    if session.get('booking') is None:
        return redirect('/')
    booking=session.pop('booking')

    booking_done=Booking(name=booking['name'],
                    phone=booking['phone'],
                    teacher_id=booking['teacher'])
    db.session.add(booking_done)
    db.session.commit()

    return render_template("booking_done.html",
                           time=booking['time'],
                           day=booking['day'],
                           phone=booking['phone'],
                           name=booking['name'])


@app.route('/request/', methods=["POST", "GET"])
def requested():
    form=RequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        session['requested']={'name':form.name.data,
                              'phone':form.phone.data,
                              'goal':form.goals.data,
                              'time':form.times.data}
        return redirect(url_for('request_done'))

    return render_template('request.html',form=form)

@app.route('/request_done/',methods=["POST","GET"])

def request_done():
    if session.get('requested') is None:
        return redirect('/')
    requested=session.pop('requested')

    name=requested['name']
    phone=requested['phone']
    goall=requested['goal']
    time=requested['time']

    goal=Goal.query.filter(Goal.name==goall).first_or_404()
    application=Application(name=name,
                            phone=phone,
                            time=time,
                            goal=goal)
    db.session.add(application)
    db.session.commit()

    return render_template('request_done.html',goal=goall,time=time,name=name,phone=phone)





if __name__ == '__main__':
    app.run()
