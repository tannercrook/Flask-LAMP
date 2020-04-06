# Catalog Blueprint

from flask import Flask, Blueprint, render_template, flash, redirect, abort, url_for, session, Response
from sqlalchemy.orm import sessionmaker, scoped_session, query, session
from sqlalchemy.sql.functions import func 
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, TextAreaField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email


from models.models import School, Catalog, CatalogYear, CreditType, Course
from models.Connection import db_session

# Setup blueprint
catalog = Blueprint('catalog', __name__)


# Routes
# --------------------------

@catalog.route('/catalog/current', methods=['GET','POST'])
def activeCatalogs():
    return '<h1>Catalogs</h1>'

@catalog.route('/catalog/<int:catalog_id>', methods=['GET','POST'])
def viewCatalog(catalog_id):
    catalog = db_session.query(Catalog).filter(Catalog.catalog_id == catalog_id).one()
    school = db_session.query(School).filter(School.school_id == catalog.school_id).one()
    courses = db_session.query(Course).join(Catalog).filter(Catalog.catalog_id==catalog.catalog_id).all()

    return render_template('catalog/viewCatalog.html', catalog=catalog, school=school, courses=courses)


@catalog.route('/catalog/<int:catalog_id>/add-course', methods=['GET','POST'])
def addCourse(catalog_id):
    catalog = db_session.query(Catalog).filter(Catalog.catalog_id == catalog_id).one()
    school = db_session.query(School).filter(School.school_id == catalog.school_id).one()
    courses = db_session.query(Course).join(Catalog).filter(Catalog.catalog_id==catalog.catalog_id).all()

    form = initalizeCourseForm()

    if form.is_submitted() and form.validate_on_submit():
        course = Course()
        course.catalog_id = catalog.catalog_id
        course.number = form.number.data 
        course.name = form.name.data   
        course.description = form.description.data
        course.credit_type_id = form.credit_type_id.data
        course.credits = form.credits.data
        db_session.add(course)
        db_session.commit()
        flash("Saved Successfully.")
        return redirect(url_for('catalog.viewCatalog', catalog_id=catalog.catalog_id))

    return render_template('catalog/addCourse.html', form=form, catalog=catalog, school=school, courses=courses)



# Utility Functions
# -----------------------------

def getCreditTypes():
    credit_types = db_session.query(CreditType.credit_type_id, CreditType.name).all()
    return dict(credit_types)

def initalizeCourseForm():
    form = CourseForm()
    credit_types = db_session.query(CreditType.credit_type_id, CreditType.name).all()
    form.credit_type_id.choices = credit_types

    return form


# Classes
# -----------------------------
class CourseForm(FlaskForm):
    number = StringField('Number: ', validators=[DataRequired()])
    name = StringField('Name: ', validators=[DataRequired()])
    description = TextAreaField('Description: ')
    credit_type_id = SelectField('Credit Type: ', coerce=int)
    credits = DecimalField('Credits: ')

