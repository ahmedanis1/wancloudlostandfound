from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/lostandfound'
dataBase=SQLAlchemy(app)
# engine = sqlalchemy.create_engine('mysql://root:''@db:3306/apnaschoolmysqldb')

if __name__== '__main__':
    from api.User import *
    from api.Item import *

    app.run(host="127.0.0.1",port="5000",debug=True)
