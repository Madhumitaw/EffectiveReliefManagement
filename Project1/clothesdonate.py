from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField,RadioField,SelectField,DateField,IntegerField
import pypyodbc
connection = pypyodbc.connect('Driver={SQL Server};' 'Server=tcp:madhuw.database.windows.net,1433;'
'Database=dbtest;'
'Uid=madhu123@madhuw;'
'Pwd=Madhu@123;')

cursor = connection.cursor()
class DonateClothes(Form):
    Clothes = RadioField('', choices = [('Women','Women'),('Men','Men'),('Kids','Kids')])
    size= RadioField('', choices = [('S','Small'),('M','Medium'),('L','Large')])
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
    comments=TextField('', render_kw={"placeholder": "Comments"})
    qty= SelectField('', choices = [('2', 'Pack of 2'),('4','Pack of 4'),('6','Pack of 6'),('12','Pack of 12')])