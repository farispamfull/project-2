from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def ru_phone(form,field):
    phone=form.phone.data
    if not(phone.startswith('+79') or phone.startswith('89') or phone.startswith('79')) or len(phone)!=12 and len(phone)!=11:
        raise ValidationError('неправильно введен номер')
    elif not phone.startswith('+79'):
        form.phone.data='+7'+phone[1:]

class BookingForm(FlaskForm):
    name = StringField('Вас зовут', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired(), ru_phone])
    submit = SubmitField('Записаться на пробный урок')


class RequestForm(FlaskForm):
    goals = RadioField(
        '',
        choices=[
            ('travel', 'Для путешествий'),
            ('study', 'Для школы'),
            ('work', 'Для работы'),
            ('relocate', 'Для переезда'),
        ],
        default='travel',
    )
    times = RadioField(
        '',
        choices=[
            ('1-2', '1-2 часа в неделю'),
            ('3-5', '3-5 часа в неделю'),
            ('5-7', '5-7 часа в неделю'),
            ('7-10', '7-10 часа в неделю'),
        ],
        default='1-2',
    )
    name = StringField('Вас зовут', validators=[DataRequired()])
    phone = StringField('Ваш телефон', validators=[DataRequired(), ru_phone])
    submit = SubmitField('Найдите мне преподавателя')