from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.choices import SelectField, RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import validators

class NewNewsArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    content = TextAreaField('Content', [validators.DataRequired(), Length(1, 6000)])
    image = RadioField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class Login(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Length(1, 60),
        Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
               message="Please enter a valid email address")
    ])
    submit = SubmitField('Submit')

class ImageForm(FlaskForm):
    image = FileField("photo", validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Submit')
