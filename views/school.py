# School Blueprint

from flask import Flask, Blueprint, render_template, flash, redirect, abort, url_for, session, Response
from sqlalchemy.orm import sessionmaker, scoped_session, query, session
from sqlalchemy.sql.functions import func 

from models.models import School, Catalog
from models.Connection import db_session

# Setup blueprint
school = Blueprint('school', __name__)

@school.route('/school/all', methods=['GET','POST'])
def listSchools():
    schools = db_session.query(School)
    
    return render_template('school/allSchools.html', schools=schools)

@school.route('/school/<int:school_id>', methods=['GET','POST'])
def schoolCatalogs(school_id):
    school = db_session.query(School).filter(School.school_id==school_id).one()
    catalogs = db_session.query(Catalog).join(School).filter(School.school_id==school_id).all()
    return render_template('school/catalogs.html', school=school ,catalogs=catalogs)