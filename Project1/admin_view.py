from flask_wtf import Form
import pypyodbc
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField,RadioField,SelectField,DateField,IntegerField
connection = pypyodbc.connect('Driver={SQL Server};' 'Server=tcp:madhuw.database.windows.net,1433;'
'Database=dbtest;'
'Uid=madhu123@madhuw;'
'Pwd=Madhu@123;')

cursor = connection.cursor()
class filter_Criteria(Form):
        SQLCommand = ("select distinct CTYNAME from loc_tet")
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
        crit = SelectField('Select County',default=alist[0],
                    choices =alist)
    
class addcal(Form):
        calname = SelectField('', choices = [('Earthquake', 'Earthquake'),('Tsunami','Tsunami'),('Forest Fire','Forest Fire'),('Hurricane','Hurricane')])
        SQLCommand = ("select distinct CTYNAME from loc_tet")
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
        calaloc =SelectField('Select County',default=alist[0],
                    choices =alist)
    