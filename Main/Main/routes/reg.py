from . import Main
from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
   # email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
    #register = SubmitField('Register')
  
class LoginForm(Form):
    username1 = TextField('Username', [validators.Length(min=4, max=20)])
    password1 = TextField('Password', [validators.Length(min=4, max=10)])
   # email = TextField('Email Address', [validators.Length(min=6, max=50)])
    #password1 = PasswordField('New Password', [
     #   validators.Required()
    #])
   # login = SubmitField('Login')
@routes.route('/register/', methods=["GET","POST"])
def register_page():
    try:
        register_form= reg.RegistrationForm(request.form)
        login_form = reg.LoginForm(request.form)
        if request.method == "POST":
            attempted_button = request.form['but']
    
            #if(attempted_button=='Login'and login_form.validate()):
            
            if  attempted_button=='Login' and login_form.validate_on_submit():
                #print ("Login form is submitted")
                #return render_template("main.html")
                return("Trurr"+str(login_form.validate_on_submit()))
            if(attempted_button=='Register'):
                if(register_form.validate()):
                    return("Trr")
        return render_template("register.html",form = register_form,form1=login_form)
    except Exception as e:
        return("EEE"+str(e))



        

