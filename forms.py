from flask_wtf import FlaskForm # pentru a transforma registerul in flask form
from wtforms import StringField, PasswordField, FileField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileAllowed
from flask_uploads import IMAGES


#pentru formul de register
class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired('Numele este camp obligatoriu! '), Length(max=100, message='Numele nu poate avea mai mult de 100 de caractere')])
    username = StringField('Username', validators=[InputRequired('Username-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    image    = FileField(validators=[FileAllowed(IMAGES, 'Doar imaginile sunt acceptate!')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('Username-ul este camp obligatioriu!'), Length(max=100, message='Username-ul nu poate avea mai mult de 100 de caractere!')])
    password = PasswordField('Password', validators=[InputRequired('Parola este camp obligatoriu!')])
    remember = BooleanField('Remember Me')

class TweetForm(FlaskForm):
    text = TextAreaField('Message',validators=[InputRequired('Message is required.')])
