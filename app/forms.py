from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class AdminLogin(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class NewEvent(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=500)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max = 2000)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Upload')
