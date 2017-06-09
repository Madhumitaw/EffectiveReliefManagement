"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.

Project: Using BigData and IOT for Effective diaster Management
During any natural calamity users can make donation considering the demographic distribution of the impacted area instead of just donating items.
This will also prevent huge waste of resources.

This project is built using follwoing technologies:

Android: IOT Simulator
python with visual Studio IDE
(Pthon with all required libraries)
Azure cloud database
HTML5, CSS.
SPARK-pyspark


"""

from flask import Flask, render_template, request, url_for ,redirect ,flash , session
import pypyodbc
import cgitb ,cgi
from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField,RadioField
from datetime import datetime
import loginreg,moneydonate,fooddonate,clothesdonate,admin_view ,otherdonate
import base64
from io import BytesIO
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
# imports for matplotlib plotting
import tempfile
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
##Azure connection
connection = pypyodbc.connect('Driver={SQL Server};' 'Server=tcp:madhuw.database.windows.net,1433;'
'Database=dbtest;'
'Uid=madhu123@madhuw;'
'Pwd=Madhu@123;')

cursor = connection.cursor()


@app.route('/')
def home():
    return render_template("index.html")
@app.route('/blog/')
def blog():
   return render_template("blog.html")
@app.route('/staff/')
def staff():
    return render_template("staff.html")

@app.route('/events/')
def events():
    return render_template("events.html")
@app.route('/contact/')
def contact():
    return render_template("page-contact.html")
@app.route('/statistics/')

#Retieve latest data for graphical represntation of all donations based on Country
def stat():
    SQLCommand = ("Select count(*) from User_Donation,User_Info where  User_Donation.Donor=User_Info.Username and User_Info.Country='US' ")
    cursor.execute(SQLCommand)
    US=cursor.fetchone()[0]
    #return("MONEY"+str(money)+str(cursor))
    SQLCommand = ("Select count(*) from User_Donation,User_Info where  User_Donation.Donor=User_Info.Username and User_Info.Country='CHINA' ")
    cursor.execute(SQLCommand)
    CHINA=cursor.fetchone()[0]
    SQLCommand = ("Select count(*) from User_Donation,User_Info where  User_Donation.Donor=User_Info.Username and User_Info.Country='UK' ")
    cursor.execute(SQLCommand)
    UK=cursor.fetchone()[0]
    SQLCommand = ("Select count(*) from User_Donation,User_Info where  User_Donation.Donor=User_Info.Username and User_Info.Country='INDIA' ")
    cursor.execute(SQLCommand)
    INDIA=cursor.fetchone()[0]
    SQLCommand = ("Select count(*) from User_Donation,User_Info where  User_Donation.Donor=User_Info.Username and User_Info.Country='GERMANY' ")
    cursor.execute(SQLCommand)
    GERMANY=cursor.fetchone()[0]


    data = [('GERMANY', GERMANY), ('INDIA', INDIA), ('CHINA', CHINA),('US', US),('UK', UK)]
    return render_template("statistics.html",data_1=data)

#User Valid/Invalid Login Check
@app.route('/admin/', methods=["GET","POST"])
def admin():
    try:
        
        admin_login = loginreg.AdminLogin(request.form)
        
        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Admin Login' and admin_login.validate_on_submit():
                uname=str(admin_login.adminu.data)
                pwd=str(admin_login.adminp.data)
                #return(uname+pwd)
 
                if  uname=='adminl'and pwd=='adminp' :
                    return redirect(url_for('onadminlogin'))
                   
                else:
                    errmsg="Invalid credentials"
                    return render_template("admin.html",errmsg = errmsg,form5 = admin_login)
                    
                  
        return render_template("admin.html",form5 = admin_login)
    except Exception as e:
        return("Error:"+str(e))


  
 #Signup Registeration page and insert into database  
@app.route('/pagedonate/', methods=["GET","POST"])
def don():
    try:
        register_form= loginreg.RegistrationForm(request.form)
        login_form = loginreg.LoginForm(request.form)
        
        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Login' and login_form.validate_on_submit():
                #print ("Login form is submitted")
                #return render_template("main.html")
                uname=str(login_form.username1.data)
                pwd=str(login_form.password1.data)
                SQLCommand = ("SELECT * FROM User_Info where Username= ? and Password= ?")
                Values=[uname,pwd]
                cursor.execute(SQLCommand,Values)
                
                #session['my_var'] = uname
                x=cursor.fetchone()
      
                session['my_var'] = uname
                if  cursor.rowcount==0 :
                   
                    errmsg="Invalid credentials"
                    return render_template("page-donate.html",errmsg = errmsg,form1=login_form,form=register_form)
                else:
                      return redirect(url_for('onlogin'))
                      
                  
            if attempted_button=='Sign-Up' and register_form.validate_on_submit():
                runame=str(register_form.username.data)
                rpwd=str(register_form.password.data)
                rfname=str(register_form.firstname.data)
                rlname=str(register_form.lastname.data)
                remail=str(register_form.email.data)
                rphone=str(register_form.phoneno.data)
                radd=str(register_form.Address.data)
                rcountry=str(register_form.Country.data)
                SQLCommand = ("SELECT * FROM User_Info where Username= ?")
                Values=[runame]
                cursor.execute(SQLCommand,Values)
            
                #session['my_var'] = uname
                x=cursor.fetchone()
                if  cursor.rowcount==0 :
                   SQLCommand = ("INSERT INTO User_Info "
                             "(Username, Password,Fname,Lname,Phone,Email,Addr,Country) "
                            "VALUES (?,?,?,?,?,?,?,?)")
                   Values = [runame,rpwd,rfname,rlname,rphone,remail,radd,rcountry]
                   cursor.execute(SQLCommand,Values)
                   connection.commit()
                   loginmsg="Please log-in to Continue.."
                   return render_template("page-donate.html",form1 = login_form,form=register_form,loginmsg=loginmsg)
                else:
                   loginmsg="This is already registered user"
                   return render_template("page-donate.html",form1 = login_form,form=register_form,loginmsg=loginmsg)


              
                    
        return render_template("page-donate.html",form1 = login_form,form=register_form)
    except Exception as e:
        return("Error:"+str(e))
   #all transaction on user money donation page
@app.route('/donatemoney/', methods=["GET","POST"])
def ondonateMoney():#      
    uname = session.get('user', None)
    try:
        #Retrieve all previous donations to show the distribution done till date
        donatemoney= moneydonate.Donatemoney(request.form)
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? and Details='50 USD'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        money50=(cursor.fetchone()[0])*50
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? and Details='10 USD'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        money10=(cursor.fetchone()[0])*10
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? and Details='100 USD'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        money100=(cursor.fetchone()[0])*100
        data = [('10 USD', money10), ('50 USD', money50), ('100 USD', money100)]
        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Donate Money' and donatemoney.validate_on_submit(): #and donatemoney.validate_on_submit():
               
                cardnumber=str(donatemoney.card_number.data)
                typeofdonation="MONEY"
                cvc=str(donatemoney.cvc.data)
                amount=str(donatemoney.amount.data)
                expdate=str(donatemoney.date.data)
                cause=str(donatemoney.cause.data)
                donor=uname
                na='NA'
                status='Approved'
             


                year=str(datetime.now().date())
                comments='NA'
                SQLCommand = ("INSERT INTO User_Donation "
                             "(Cause,Donor,Donation_Type,Details,Qty,CVC_Number,Card_Number,Exp_date,Suitable_for,Size,Comments,Date,Status) "
                            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)")
                Values=[cause,donor,typeofdonation,amount,amount,cvc,cardnumber,expdate,na,na,na,year,status]
                cursor.execute(SQLCommand,Values)
                
                connection.commit()
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? and Details='50 USD'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                money50=(cursor.fetchone()[0])*50
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? and Details='10 USD'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                money10=(cursor.fetchone()[0])*10
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? and Details='100 USD'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                money100=(cursor.fetchone()[0])*100
                data = [('10 USD', money10), ('50 USD', money50), ('100 USD', money100)]
                
                
                
                don_msg=donor+" Thanks for your generous donation"  
                return render_template("donatemoney.html",form2 =donatemoney,uname=uname,don_msg=don_msg,data=data)  
        return render_template("donatemoney.html",form2 =donatemoney,uname=uname,data=data)
    except Exception as e:
        return("Error:"+str(e))
def __init__(self, *args, **kwargs):
    kwargs['csrf_enabled'] = False
    super(ProfileInfoForm, self).__init__(*args, **kwargs)                   
##end Login
#Food donation page with all queries related to donations made to non-perishable food items
@app.route('/fooddonation/', methods=["GET","POST"])
def ondonateFood():#      
    uname = session.get('user', None)
    try:
        donatefood= fooddonate.Donatefood(request.form)
        SQLCommand = ("Select ItemInfo,cast(Capacity as Int)-cast(ItemQty as int) from Inventory where Item='FOOD'")
        cursor.execute(SQLCommand)
        results = cursor.fetchall()
        '''
        '''
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'Cookies'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        cookies=(cursor.fetchone()[0])
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'Rice'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        rice=(cursor.fetchone()[0])
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'Water'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        Water=(cursor.fetchone()[0])
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'ProtBar'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        ProtBar=(cursor.fetchone()[0])

        data = [('Cookies', cookies), ('Rice', rice), ('Water', Water),('Protein Bars',ProtBar)] 
        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Donate Food' and donatefood.validate_on_submit():
                
                typeofdonation="FOOD"
                foodtype=str(donatefood.Foodtype.data)
                suit_for=str(donatefood.suit_for.data)
                comment=''+str(donatefood.comments.data)
                cause=str(donatefood.cause.data)
                donor=uname
                dondetails=comment
                na='NA'
                status='Pending'
                year=str(datetime.now().date())
                cursor.execute("""Update Inventory Set ItemDonated=cast(ItemDonated as int)+cast(? as int) where Item='Food' and ItemInfo=(?)""" ,(suit_for,foodtype))
                connection.commit()
                SQLCommand = ("INSERT INTO User_Donation "
                             "(Cause,Donor,Donation_Type,Details,Qty,CVC_Number,Card_Number,Exp_date,Suitable_for,Size,Comments,Date,Status) "
                            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)")
                Values=[cause,donor,typeofdonation,foodtype,suit_for,na,na,na,na,na,comment,year,status]
                cursor.execute(SQLCommand,Values)
                connection.commit()
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'Cookies'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                cookies=(cursor.fetchone()[0])
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'Rice'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                rice=(cursor.fetchone()[0])
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'Water'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                Water=(cursor.fetchone()[0])
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? and Details like 'ProtBar'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                ProtBar=(cursor.fetchone()[0])

                data = [('Cookies', cookies), ('Rice', rice), ('Water', Water),('Protein Bars',ProtBar)] 


                #return ("test"+year)
                don_msg=donor+" Thanks for your generous donation.Once the donations are recieved the above table will reflect the changes"  
                return render_template("fooddonation.html",form3 =donatefood,uname=uname,don_msg=don_msg,result=results,data=data)  
                #return ("test"+uname+foodtype)
                    
        return render_template("fooddonation.html",form3 =donatefood,uname=uname,result=results,data=data)
    except Exception as e:
        return("Error:"+str(e))
#CLothes Donation page which covers all clothes donation considering gender and age the clother will be suitlable for
@app.route('/donateclothes/', methods=["GET","POST"])
def clothesdonation():      
    uname = session.get('user', None)
    try:
        donateclothes= clothesdonate.DonateClothes(request.form)
        
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? and Details like 'Kid%'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        kids=(cursor.fetchone()[0])
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? and Details like 'Women%'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        women=(cursor.fetchone()[0])
        SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? and Details like 'Men%'")
        Values=[uname]
        cursor.execute(SQLCommand,Values)
        men=(cursor.fetchone()[0])
        data = [('Kids', kids), ('Women', women), ('Men', men)]   
        SQLCommand = ("Select ItemInfo,cast(Capacity as Int)-cast(ItemQty as int) from Inventory where Item='CLOTHES'")
        cursor.execute(SQLCommand)
        results = cursor.fetchall()
        
           
        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Donate Clothes' and donateclothes.validate_on_submit():
                
                typeofdonation="CLOTHES"
                Clothes=str(donateclothes.Clothes.data)
                size=str(donateclothes.size.data)
                comment=str(donateclothes.comments.data)
                cause=str(donateclothes.cause.data)
                qty=str(donateclothes.qty.data)
                details=Clothes+" "+size
                donor=uname
                na='NA'
                status='Pending'
                year=str(datetime.now().date())
                SQLCommand = ("INSERT INTO User_Donation "
                             "(Cause,Donor,Donation_Type,Details,Qty,CVC_Number,Card_Number,Exp_date,Suitable_for,Size,Comments,Date,Status) "
                            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)")
                Values=[cause,donor,typeofdonation,details,qty,na,na,na,Clothes,size,comment,year,status]
                cursor.execute(SQLCommand,Values)
                connection.commit()
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? and Details='kids'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                kids=(cursor.fetchone()[0])
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? and Details='women'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                women=(cursor.fetchone()[0])
                SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? and Details='men'")
                Values=[uname]
                cursor.execute(SQLCommand,Values)
                men=(cursor.fetchone()[0])
                data = [('Kids', kids), ('Women', women), ('Men', men)]   
                #return ("test"+year)
                don_msg=donor+" Thanks for your generous donation.Once the donations are recieved the above table will reflect the changes"  
                return render_template("clothesdonation.html",form4 =donateclothes,uname=uname,don_msg=don_msg,data=data,result=results)  
                    
        return render_template("clothesdonation.html",form4 =donateclothes,uname=uname,data=data,result=results)
    except Exception as e:
        return("Error:"+str(e))

@app.route('/otherdonations/',methods=["GET","POST"])
def others():
       uname = session.get('user', None)
       try:
        donateother= otherdonate.DonateOthers(request.form)
        SQLCommand = ("Select ItemInfo,cast(Capacity as Int)-cast(ItemQty as int) from Inventory where Item='OTHERS'")
        cursor.execute(SQLCommand)
        results = cursor.fetchall()
              
        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Donate Other' and donateother.validate_on_submit():
                
                typeofdonation="OTHERS"
                items=str(donateother.Items.data)
                qty=str(donateother.Qty.data)
                cause=str(donateother.cause.data)
                comment=str(donateother.comments.data)
                donor=uname
                na='NA'
                status='Pending'
                year=str(datetime.now().date())
                SQLCommand = ("INSERT INTO User_Donation "
                             "(Cause,Donor,Donation_Type,Details,Qty,CVC_Number,Card_Number,Exp_date,Suitable_for,Size,Comments,Date,Status) "
                            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)")
                Values=[cause,donor,typeofdonation,items,qty,na,na,na,na,na,comment,year,status]
                cursor.execute(SQLCommand,Values)
                connection.commit()
 
                #return ("test"+year)
                don_msg=donor+" Thanks for your generous donation.Once the donations are recieved the above table will reflect the changes"  
                return render_template("donateother.html",form_don =donateother,uname=uname,don_msg=don_msg,result=results)  
                
        return render_template("donateother.html",form_don =donateother,uname=uname,result=results)
       except Exception as e:
        return("Error:"+str(e))



@app.route('/onlogin/')
def onlogin():
    """Renders a sample page."""
    #return "Hello World!"
    uname = session.get('my_var')
    session['user'] = uname
    
    
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' and Donor=? ")
    Values=[uname]
    cursor.execute(SQLCommand,Values)
    money=cursor.fetchone()[0]
    #return("MONEY"+str(money)+str(cursor))
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' and Donor=? ")
    Values=[uname]
    cursor.execute(SQLCommand,Values)
    food=cursor.fetchone()[0]
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES' and Donor=? ")
    Values=[uname]
    cursor.execute(SQLCommand,Values)
    clothes=cursor.fetchone()[0]
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='OTHERS' and Donor=? ")
    Values=[uname]
    cursor.execute(SQLCommand,Values)
    others=cursor.fetchone()[0]
    data = [('CLOTHES', clothes), ('MONEY', money), ('Food', food),('Others',others)]
    SQLCommand = ("SELECT Transaction_id,Donation_Type,Details,date FROM User_Donation where Donor=?")
    Values=[uname]
    cursor.execute(SQLCommand,Values)
    results = cursor.fetchall()
    #return("test"+str(results))
    
    #return my_var
    return render_template("OnLogin.html",uname = uname,data=data,result=results)


@app.route('/addCalamity/', methods=["GET","POST"])
def addCalamity():
    try:
        addcalamity=admin_view.addcal(request.form)

        if request.method == "POST":
            attempted_button = request.form['but']
          
            if  attempted_button=='Add Calamity' :#and donatefood.validate_on_submit():
              
                calname=str(addcalamity.calname.data)
                loc=str(addcalamity.calaloc.data)
                year=str(datetime.now().date())  
                desc=calname+":"+loc 
                SQLCommand = ("INSERT INTO Disaster "
                             "(Disaster_name,Location,Date,Disaster_desc) "
                            "VALUES (?,?,?,?)")
                Values=[calname,loc,year,desc]
                cursor.execute(SQLCommand,Values)
                connection.commit()
                a='hola'
                return render_template("add.html",formcal =addcalamity) 
                #return ("test"+uname+foodtype)
                    
        return render_template("add.html",formcal =addcalamity)
    except Exception as e:
        return("Error:"+str(e))
    

@app.route('/onadminlogin/')
def onadminlogin():
    """Renders a sample page."""
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='MONEY' ")
    
    cursor.execute(SQLCommand)
    money=cursor.fetchone()[0]
    #return("MONEY"+str(money)+str(cursor))
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='FOOD' ")
    
    cursor.execute(SQLCommand)
    food=cursor.fetchone()[0]
    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='CLOTHES'")
    cursor.execute(SQLCommand)
    clothes=cursor.fetchone()[0]

    SQLCommand = ("Select count(*) from User_Donation where Donation_Type='OTHERS' ")
    
    cursor.execute(SQLCommand)
    other=cursor.fetchone()[0]
    SQLCommand = ("SELECT Transaction_id,Donor,Donation_Type,date FROM User_Donation ")

    cursor.execute(SQLCommand)
    results = cursor.fetchall()

    data = [('CLOTHES', clothes), ('MONEY', money), ('FOOD', food), ('OTHERS', other)]
    return render_template("adminLogin.html",data=data,result=results)

@app.route('/viewstatus/', methods=["GET","POST"])
def viewstat():
   
    
    try:
        adm_view = admin_view.filter_Criteria(request.form)

        if request.method == "POST" :
            selected_opt=str(adm_view.crit.data)
            res=selected_opt
            SQLCommand = ("select sum(cast (TOT_MALE as int)) from loc_tet where CTYNAME=?")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            m=cursor.fetchone()[0]
            SQLCommand = ("select  sum(cast (TOT_FEMALE as int)) from loc_tet where CTYNAME=?")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            f=cursor.fetchone()[0]

            x=[5,7]
            y=[m,f]
            labels=['Female','Male']
          
            #plt.xticks[x,x_xticks]
            my_colors = 'mb'
            plt.clf()
            plt.cla()
            plt.close()
            plt.bar(x, y,color=my_colors, align='center')
           # plt.bar(x2, y2, color=my_colors, align='center')
            plt.xticks(x,labels)
            #plt.margin(0.2)
            plt.title('Demo')
            plt.ylabel('Population')
            plt.xlabel('distribution')
            plt.savefig('test')
            figfile = BytesIO()
            plt.savefig(figfile, format='png')
            figfile.seek(0)
            figdata_png = base64.b64encode(figfile.getvalue())
            result = figdata_png
            result = str(figdata_png)[2:-1]
            
            SQLCommand = ("select cast (TOT_MALE as int) from loc_tet where CTYNAME=? and AGEGRP='0:3'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_0_3=cursor.fetchone()[0]
            SQLCommand = ("select cast (TOT_MALE as int) from loc_tet where CTYNAME=? and AGEGRP='4:9'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_4_9=cursor.fetchone()[0]
            
            SQLCommand = ("select cast (TOT_MALE as int) from loc_tet where CTYNAME=? and AGEGRP='10:13'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_10_13=cursor.fetchone()[0]
            SQLCommand = ("select cast (TOT_MALE as int) from loc_tet where CTYNAME=? and AGEGRP='14:18'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_14_18=cursor.fetchone()[0]
            label = ['A', 'B','C', 'D']
            sizes=[age_0_3,age_4_9,age_10_13,age_14_18]
            plt1.clf()
            plt1.cla()
            plt1.close()
            #sizes = [215, 130, 245, 210]
            colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
            #explode = (0.1, 0, 0, 0)  # explode 1st slice
            plt1.pie(sizes,  labels=label, colors=colors,explode = (0, 0.05, 0, 0),
             autopct='%1.1f%%', shadow=True, startangle=90)

            figfile1  = BytesIO()
            plt1.title('Male-Data Distribution')
            plt1.savefig('test1')
            plt1.ylabel('')
            plt1.xlabel('')
            plt1.savefig(figfile1, format='png')
            figfile.seek(0)
            figdata_png1 = base64.b64encode(figfile1.getvalue())
            result11=''
            result11 = figdata_png1
            result11 = str(figdata_png1)[2:-1]
 
            plt1.axis('equal')
 ######
            SQLCommand = ("select cast (TOT_FEMALE as int) from loc_tet where CTYNAME=? and AGEGRP='0:3'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_0_3F=cursor.fetchone()[0]
            SQLCommand = ("select cast (TOT_FEMALE as int) from loc_tet where CTYNAME=? and AGEGRP='4:9'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_4_9F=cursor.fetchone()[0]
            
            SQLCommand = ("select cast (TOT_FEMALE as int) from loc_tet where CTYNAME=? and AGEGRP='10:13'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_10_13F=cursor.fetchone()[0]
            SQLCommand = ("select cast (TOT_FEMALE as int) from loc_tet where CTYNAME=? and AGEGRP='14:18'")
            Values=[res]
            cursor.execute(SQLCommand,Values)
            age_14_18F=cursor.fetchone()[0]
            label = ['A', 'B','C', 'D']
            sizes=[age_0_3F,age_4_9F,age_10_13F,age_14_18F]
            plt2.clf()
            plt2.cla()
            plt2.close()
            #sizes = [215, 130, 245, 210]
            colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
            #explode = (0.1, 0, 0, 0)  # explode 1st slice
            plt2.pie(sizes,  labels=label, colors=colors,explode = (0, 0.05, 0, 0),
             autopct='%1.1f%%', shadow=True, startangle=140)

            figfile2  = BytesIO()
            plt2.title('Female-Data Distribution')
            plt2.savefig('test1')
            plt2.ylabel('')
            plt2.xlabel('')
            plt2.savefig(figfile2, format='png')
            figfile2.seek(0)
            figdata_png2 = base64.b64encode(figfile2.getvalue())
            result12=''
            result12 = figdata_png2
            result12 = str(figdata_png2)[2:-1]
 
            plt1.axis('equal')
            SQLCommand = ("Select Age, Def from agedef;")
            cursor.execute(SQLCommand)
            fetchres = cursor.fetchall()	          
            return render_template("adminViewStatus.html",form_ad=adm_view,result=result,result11=result11,result12=result12,fetchres=fetchres)
        load_msg='Please select County and click on \'Go\' to load the image'
         
        return render_template("adminViewStatus.html",form_ad=adm_view,load_msg=load_msg)
    except Exception as e:
        return("Error:"+str(e))
@app.route('/inventory/', methods=["GET","POST"])
def viewinvent():
    
        SQLCommand = ("SELECT Transaction_id,Donor,Donation_Type,date FROM User_Donation where Status='Pending' ")
        cursor.execute(SQLCommand)
        results = cursor.fetchall()
        return render_template("adminViewInventory.html",result=results)
@app.route('/approve/<int:row_id><string:type>', methods=["GET","POST"])
def appro(row_id,type):
        Status='Approved'
        nos=row_id
        type=type
        cursor.execute("""Update User_Donation Set Status=(?)  where Transaction_id=(?)""" ,(Status,nos))
        connection.commit()

        SQLCommand = ("SELECT Transaction_id,Donation_Type,Details,Qty FROM User_Donation where Transaction_id=? ")
        Values=[row_id]
        cursor.execute(SQLCommand,Values)
        row = cursor.fetchone()  
        type_don=str(row[1]) 
        details= str(row[2]) 
        qty=str(row[3]) 
        
        
        cursor.execute("""Update Inventory Set ItemDonated=cast(ItemDonated as int)-cast(? as int) ,ItemQty=cast (ItemQty as int)+cast(? as int) where Item=(?) and ItemInfo=(?)""" ,(qty,qty,type_don,details))
        connection.commit()
        SQLCommand = ("SELECT Transaction_id,Donor,Donation_Type,date FROM User_Donation where Status='Pending' ")
        cursor.execute(SQLCommand)
        results = cursor.fetchall()
        
        return render_template("adminViewInventory.html",result=results)
   
if __name__ == '__main__':
    import os
     # set as part of the config
    SECRET_KEY = 'many random bytes'

# or set directly on the app
    app.secret_key = 'many random bytes'   
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
