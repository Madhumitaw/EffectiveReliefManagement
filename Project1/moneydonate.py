from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField,RadioField,SelectField,DateField,IntegerField
import pypyodbc
connection = pypyodbc.connect('Driver={SQL Server};' 'Server=tcp:madhuw.database.windows.net,1433;'
'Database=dbtest;'
'Uid=madhu123@madhuw;'
'Pwd=Madhu@123;')

cursor = connection.cursor()

class Donatemoney(Form):
   card_number=TextField('',[validators.Required()], render_kw={"placeholder": "Card Number"})
   cvc=TextField('',[validators.Length(min=3, max=3),validators.required()], render_kw={"placeholder": "CVC"})
   amount = RadioField('', choices = [('10','10 USD'),('50','50 USD'),('100','100 USD')])
   #date=DateField('MM/YY', format='%Y-%m-%d')
   date=TextField('',[validators.Required()], render_kw={"placeholder": "EXP Date"})
   SQLCommand = ("Select Disaster_desc from Disaster")
   cursor.execute(SQLCommand)
   entries = cursor.fetchone()
   item=''
   i=0
   alist=[]
   while entries :
        
         item='(\''+str(entries[i])+"','"+str(entries[i])+'\')'
         a=(entries[i],entries[i])
         alist.append(a)
         entries = cursor.fetchone()
        #crit = SelectField('Select County',default=alist[0],
         #           choices =alist)
   cause=SelectField('',default=alist[0],
                    choices =alist)
   #cause= SelectField('', choices = [('Nepal Earthquake', 'Nepal Earthquake'),('Tsunami','Tsunami'),('Other','Other')])
  