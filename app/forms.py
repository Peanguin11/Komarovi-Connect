from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


# class AdminLogin(FlaskForm): ###  dakomentarebuli rac maqvs egeni agar aris sawiro mara mainc ar wavshale gadaxede
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Log In')


class NewEvent(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=500)])
    description = StringField('Description', validators=[DataRequired()], widget=TextArea())
    registration_link = StringField("Registration Link", validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired(), Length(min=1, max=500)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    event_date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Upload')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")




class Addnewsform(FlaskForm):
    name = StringField('name')
    img = FileField('image')
    description = StringField('description')
    submit = SubmitField('add news')

class NewProject(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description',)
    funding_goal = IntegerField('Funding Goal', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Add Project')

class NewAlumni(FlaskForm):
    name = StringField('name')
    photo_path = FileField('image')
    title = StringField('title')
    class_year = StringField('class year')  
    position = StringField('position') 
    submit = SubmitField('add alumni')