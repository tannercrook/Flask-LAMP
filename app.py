from flask import Flask 
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

# Database
from models.models import Base, CreditType
from models.Connection import db_session

# Views 
from views.catalog import catalog
from views.school import school



app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd2\x04S4\xbc\xce\xe2\x17\xfb\xff\x19C@\xa6e\xc2\xf4\x18\xad\xe8\xc4\xcb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalog_app:schoolrocks@localhost/course_catalog'
db = SQLAlchemy(app)

# Blueprints
app.register_blueprint(catalog)
app.register_blueprint(school)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return 'Hello, CIT225! This is a demo!'

@app.route('/testdb')
def testDB():
    try:
        credit_types = db_session.query(CreditType)
        return '<h2>You are set!</h2>'
    except:
        return "Something isn't quite right."
