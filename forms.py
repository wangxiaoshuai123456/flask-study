from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, Form, SelectField

from wtforms import validators, ValidationError


# from email_validator import validate_email


class ContactForm(Form):
    name = StringField("Name Of Student", [validators.DataRequired("Please enter\
                                         your name.")])

    Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('S', 'See')])

    Address = TextAreaField("Address")

    email = StringField("Email", [validators.DataRequired("Please enter your email address."), \
                                  validators.Email("Please enter your email address.")])

    Age = IntegerField("age")
    language = SelectField('Languages', choices=[('cpp', 'C++'), \
                                                 ('py', 'Python'),
                                                 ('jar', 'Java')])
    submit = SubmitField("submit")
