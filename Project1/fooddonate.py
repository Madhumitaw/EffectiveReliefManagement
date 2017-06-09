from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField,RadioField,SelectField,DateField,IntegerField
import pypyodbc
connection = pypyodbc.connect('Driver={SQL Server};' 'Server=tcp:madhuw.database.windows.net,1433;'
'Database=dbtest;'
'Uid=madhu123@madhuw;'
'Pwd=Madhu@123;')

cursor = connection.cursor()
class Donatefood(Form):
   comments=TextField('', render_kw={"placeholder": "Comments"})
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
   Foodtype= SelectField('', choices = [('Rice', 'Rice'),('Water','Water'),('Cookies','Cookies'),('ProtBar','Protein Bars')])
   suit_for= SelectField('', choices = [('1', '1'),('2','2'),('3','3'),('4','4')])
   
  