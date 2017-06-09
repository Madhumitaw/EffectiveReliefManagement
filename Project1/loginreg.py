from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField,SelectField
class RegistrationForm(Form):
    firstname=TextField('',[validators.Required()], render_kw={"placeholder": "First Name"})
    lastname=TextField('',[validators.Required()], render_kw={"placeholder": "Last Name"})
    username = TextField('', [validators.Length(min=3, max=20)], render_kw={"placeholder": "User Name"})
    phoneno = TextField('', [validators.required()], render_kw={"placeholder": "Phone"})
    email = TextField('', [validators.email()], render_kw={"placeholder": "Email"})
    Address = TextField('', [validators.Required()], render_kw={"placeholder": "Residential Address"})
    Country= SelectField('', choices = [('US', 'US'),('CHINA','CHINA'),('INDIA','INDIA'),('UK','UK'),('GERMANY','GERMANY')])
    password = PasswordField('', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Enter Password"})
    confirm = PasswordField('',render_kw={"placeholder": "Re-Enter Password"})
    
class LoginForm(Form):
    username1 = TextField('', [validators.Length(min=3, max=10)],render_kw={"placeholder": "Registered User Name"})
   
    password1 = PasswordField('',[validators.Required()],render_kw={"placeholder": "Password"})

class AdminLogin(Form):
    adminu = TextField('', [validators.Length(min=3, max=10)],render_kw={"placeholder": "Admin User Name"})
   
    adminp = PasswordField('',[validators.Required()],render_kw={"placeholder": "Admin Password"})