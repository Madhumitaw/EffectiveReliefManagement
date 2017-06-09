"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, url_for ,redirect ,flash,make_response
import pypyodbc
from flask_wtf import Form
from wtforms import  BooleanField, TextField, PasswordField, validators ,SubmitField
import reg
import json
from urllib.request import urlopen
import requests
from reportlab.pdfgen import canvas
import pdfkit
import sys
from operator import add
from pyspark import SparkContext,SQLContext
import csv
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import plotly
from plotly.graph_objs import Figure,Scatter,Layout
import plotly.graph_objs as go
from matplotlib import style
from io import BytesIO
import base64
from io import StringIO


from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
import tempfile

#routes = Blueprint('routes', __name__)


app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

connection = pypyodbc.connect('Driver={SQL Server};' 'Server=tcp:madhuw.database.windows.net,1433;'
'Database=dbtest;'
'Uid=madhu123@madhuw;'
'Pwd=Madhu@123;')
cursor = connection.cursor()



@app.route('/')
def Homepage():
    """Renders a sample page."""
    style.use('ggplot')
    a=5
    
    '''
    Spark details:
    data was cleaned using spark -pandas library
    thh csv was converted to Dataframe using SQL context and then registered as a table which was accesses using SQL
    '''
    sc = SparkContext(appName="DemoCount")
    sqlct=SQLContext(sc)
    #pandas_df = pd.read_csv('C:/Users/madhumita/Downloads/Test_final.csv') 
    pandas_df = pd.read_csv('Demo_data.csv') 
    s_df1 = sqlct.createDataFrame(pandas_df)
    sqlct.registerDataFrameAsTable(s_df1,"Demo_2")
    df0_3=sqlct.sql("Select * from Demo_2")
    df_0_3=df0_3.groupby('CTYNAME').sum()


 
    df0_3=sqlct.sql("Select CTYNAME,TOT_POP,TOT_MALE,TOT_FEMALE from Demo_2 where YEAR=8 and AGEGRP >0 and AGEGRP <=3")
    df_0_3=df0_3.groupby('CTYNAME').sum()
    a0_3=df_0_3.select('CTYNAME','sum(TOT_POP)','sum(TOT_MALE)','sum(TOT_FEMALE)').collect()
    
    for row in a0_3:
       
        CityName=str(row[0]);
        Tot_pop=str(row[1])
        Tot_Male=str(row[2])
        Tot_Female=str(row[3])
        AGEGRP='0:3'
        print(CityName+"-TP-"+Tot_pop+"-TM-"+Tot_Male+"-TF-"+Tot_Female)
        SQLCommand = ("SELECT * FROM loc_tet where CTYNAME= ? and AGEGRP='0:3'")
        Values=[CityName]
        cursor.execute(SQLCommand,Values)
        if  cursor.rowcount==0 :
           SQLCommand = ("INSERT INTO loc_tet "
           "(CTYNAME, AGEGRP,TOT_POP,TOT_MALE,TOT_FEMALE) "
            "VALUES (?,?,?,?,?)")
           Values = [CityName,AGEGRP,Tot_pop,Tot_Male,Tot_Female]
           cursor.execute(SQLCommand,Values)
           connection.commit()
        else:
          
            cursor.execute("""Update loc_tet Set TOT_POP=(?) ,TOT_MALE=(?),TOT_FEMALE=(?) where CTYNAME=(?) and  AGEGRP='0:3'""" ,(Tot_pop,Tot_Male,Tot_Female,CityName))
            connection.commit()

      
    df4_9=sqlct.sql("Select CTYNAME,TOT_POP,TOT_MALE,TOT_FEMALE from Demo_2 where YEAR=8 and AGEGRP >4 and AGEGRP <=9")
    df_4_9=df4_9.groupby('CTYNAME').sum()
   
    b4_9=df_4_9.select('CTYNAME','sum(TOT_POP)','sum(TOT_MALE)','sum(TOT_FEMALE)').collect()

    for row in b4_9:
        
        CityName=str(row[0]);
        Tot_pop=str(row[1])
        Tot_Male=str(row[2])
        Tot_Female=str(row[3])
        AGEGRP='4:9'
        print(CityName+"-TP-"+Tot_pop+"-TM-"+Tot_Male+"-TF-"+Tot_Female)
        SQLCommand = ("SELECT * FROM loc_tet where CTYNAME= ? and AGEGRP='4:9'")
        Values=[CityName]
        cursor.execute(SQLCommand,Values)
        if  cursor.rowcount==0 :
           SQLCommand = ("INSERT INTO loc_tet "
           "(CTYNAME, AGEGRP,TOT_POP,TOT_MALE,TOT_FEMALE) "
            "VALUES (?,?,?,?,?)")
           Values = [CityName,AGEGRP,Tot_pop,Tot_Male,Tot_Female]
           cursor.execute(SQLCommand,Values)
           connection.commit()
        else:
          
            cursor.execute("""Update loc_tet Set TOT_POP=(?) ,TOT_MALE=(?),TOT_FEMALE=(?) where CTYNAME=(?) and  AGEGRP='4:9'""" ,(Tot_pop,Tot_Male,Tot_Female,CityName))
            connection.commit()
      

        

    df10_13=sqlct.sql("Select CTYNAME,TOT_POP,TOT_MALE,TOT_FEMALE from Demo_2 where YEAR=8 and AGEGRP >9 and AGEGRP <=13")
    df_10_13=df10_13.groupby('CTYNAME').sum()
    c10_13=df_10_13.select('CTYNAME','sum(TOT_POP)','sum(TOT_MALE)','sum(TOT_FEMALE)').collect()

    for row in c10_13:
       
        CityName=str(row[0]);
        Tot_pop=str(row[1])
        Tot_Male=str(row[2])
        Tot_Female=str(row[3])
        AGEGRP='10:13'
        print(CityName+"-TP-"+Tot_pop+"-TM-"+Tot_Male+"-TF-"+Tot_Female)
        SQLCommand = ("SELECT * FROM loc_tet where CTYNAME= ? and AGEGRP='10:13'")
        Values=[CityName]
        cursor.execute(SQLCommand,Values)
        if  cursor.rowcount==0 :
           SQLCommand = ("INSERT INTO loc_tet "
           "(CTYNAME, AGEGRP,TOT_POP,TOT_MALE,TOT_FEMALE) "
            "VALUES (?,?,?,?,?)")
           Values = [CityName,AGEGRP,Tot_pop,Tot_Male,Tot_Female]
           cursor.execute(SQLCommand,Values)
           connection.commit()
        else:
          
            cursor.execute("""Update loc_tet Set TOT_POP=(?) ,TOT_MALE=(?),TOT_FEMALE=(?) where CTYNAME=(?) and  AGEGRP='10:13'""" ,(Tot_pop,Tot_Male,Tot_Female,CityName))
            connection.commit()
      
    df13=sqlct.sql("Select CTYNAME,TOT_POP,TOT_MALE,TOT_FEMALE from Demo_2 where YEAR=8 and AGEGRP >13 ")
    df_13=df13.groupby('CTYNAME').sum()
    d_13=df_13.select('CTYNAME','sum(TOT_POP)','sum(TOT_MALE)','sum(TOT_FEMALE)').collect()
    for row in d_13:
     
        CityName=str(row[0]);
        Tot_pop=str(row[1])
        Tot_Male=str(row[2])
        Tot_Female=str(row[3])
        AGEGRP='14:18'
        print(CityName+"-TP-"+Tot_pop+"-TM-"+Tot_Male+"-TF-"+Tot_Female)
        SQLCommand = ("SELECT * FROM loc_tet where CTYNAME= ? and AGEGRP='14:18'")
        Values=[CityName]
        cursor.execute(SQLCommand,Values)
        if  cursor.rowcount==0 :
           SQLCommand = ("INSERT INTO loc_tet "
           "(CTYNAME, AGEGRP,TOT_POP,TOT_MALE,TOT_FEMALE) "
            "VALUES (?,?,?,?,?)")
           Values = [CityName,AGEGRP,Tot_pop,Tot_Male,Tot_Female]
           cursor.execute(SQLCommand,Values)
           connection.commit()
        else:
          
            cursor.execute("""Update loc_tet Set TOT_POP=(?) ,TOT_MALE=(?),TOT_FEMALE=(?) where CTYNAME=(?) and  AGEGRP='14:18'""" ,(Tot_pop,Tot_Male,Tot_Female,CityName))
            connection.commit()
       
    return render_template("main.html",Data0_3=a0_3,Data4_9=b4_9,Data10_13=c10_13,Data13=d_13)
    #return render_template("main.html")

 

        
def __init__(self, *args, **kwargs):
    kwargs['csrf_enabled'] = False
    super(ProfileInfoForm, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    import os
  
    # set as part of the config
    SECRET_KEY = 'many random bytes'

# or set directly on the app
    app.secret_key = 'many random bytes'   
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
  
  