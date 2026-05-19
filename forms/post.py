from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    content = TextAreaField("Текст", validators=[DataRequired()])
    author = StringField("Автор", validators=[DataRequired()])
