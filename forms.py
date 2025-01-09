from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField, FileField
from flask_wtf.file import FileField, FileAllowed

from wtforms.validators import DataRequired, Length
from wtforms import validators
import secrets

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo
Bootstrap5(app)
csrf = CSRFProtect(app)


class NewNewsArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    content = TextAreaField('Content', [validators.DataRequired(), Length(1, 6000)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 60)])
    submit = SubmitField('Submit')
