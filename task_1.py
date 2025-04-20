from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class RegistrationForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            InputRequired(message="Email обязателен"),
            Email(message="Неверный формат email")
        ]
    )
    phone = IntegerField(
        'Phone',
        validators=[
            InputRequired(message="Телефон обязателен"),
            # Кастомные валидаторы добавим далее
        ]
    )
    name = StringField(
        'Name',
        validators=[InputRequired(message="Имя обязательно")]
    )
    address = StringField(
        'Address',
        validators=[InputRequired(message="Адрес обязателен")]
    )
    index = IntegerField(
        'Index',
        validators=[InputRequired(message="Индекс обязателен")]
    )
    comment = StringField(
        'Comment',
        validators=[Optional()]
    )

@app.route('/registration', methods=['POST'])
def registration():
    form = RegistrationForm(data=request.form)
    if form.validate():
        return jsonify({'message': 'Регистрация прошла успешно!'})
    else:
        return jsonify(form.errors), 400

if __name__ == "__main__":
    app.run(debug=True)
