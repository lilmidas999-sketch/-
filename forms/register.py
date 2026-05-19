from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повтор пароля",
        validators=[DataRequired(), EqualTo('password')]
    )
