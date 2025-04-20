#1. Функциональный валидатор
from wtforms import ValidationError

def number_length(min: int, max: int, message=None):
    def _number_length(form, field):
        value = str(field.data)
        if field.data is None or not value.isdigit():
            raise ValidationError(message or "Телефон должен содержать только цифры")
        if not (min <= len(value) <= max):
            raise ValidationError(message or f"Длина телефона должна быть от {min} до {max}")
        if int(field.data) < 0:
            raise ValidationError(message or "Телефон не может быть отрицательным")
    return _number_length


#2. Классовый валидатор
class NumberLength:
    def __init__(self, min, max, message=None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        value = str(field.data)
        if field.data is None or not value.isdigit():
            raise ValidationError(self.message or "Телефон должен содержать только цифры")
        if not (self.min <= len(value) <= self.max):
            raise ValidationError(self.message or f"Длина телефона должна быть от {self.min} до {self.max}")
        if int(field.data) < 0:
            raise ValidationError(self.message or "Телефон не может быть отрицательным")


#3. Применяем кастомные валидаторы
class RegistrationForm(FlaskForm):
    # ...
    phone = IntegerField(
        'Phone',
        validators=[
            InputRequired(message="Телефон обязателен"),
            number_length(10, 10, message="Телефон должен содержать 10 цифр")  # Функциональный вариант
            # или NumberLength(10, 10, message="Телефон должен содержать 10 цифр")
        ]
    )
    # ...
