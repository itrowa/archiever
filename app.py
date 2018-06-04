# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, session, send_file
from flask_wtf import Form
from wtforms import IntegerField, SubmitField, StringField, DateField, SelectField, RadioField
from wtforms.validators import Required, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db') # 数据库文件存储于本网站目录中.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)        # init SQLAlchemy obj

# Routes Handle

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/plan/<int:id>')
def plan_id(id):
    plan = Plan.query.get_or_404(id)
    return render_template('plan.html', id=plan.id)

@app.route('/plan/<int:id>/graph')
def graph_image(id):
    graph = Plan.query.get_or_404(id).graph
    return send_file(graph, mimetype='image/svg+xml')

@app.route('/create-plan', methods=['GET', 'POST'])
def create_plan():
    form = CreatePlanForm()
    if form.validate_on_submit():
        # perform database operation, and some calculations
        pln = Plan(name=form.name.data, 
                 desc=form.desc.data, 
                 body=form.body.data, 
                 graph=form.svg.data)
        db.session.add(pln)
        db.session.commit()
        return redirect (url_for('plan_id', id=pln.id))  # jump to plan view page
    return render_template('create_plan.html', form=form)

@app.route('/find', methods=['GET', 'POST'])
def find_plan():
    form = FindPlanForm()
    if form.validate_on_submit():
        pass
    return render_template('find.html', form=form)

@app.route('/loungenode', methods=['GET', 'POST'])
def loungenode():
    return render_template('lounge_node.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/find-result', methods=['GET'])
def find_result():
    return render_template('find_result.html')

# Form Definition
class CreatePlanForm(Form):
    name = StringField('The Name of This Layout: ', validators=[Required()])
    desc = StringField('The Short Description of This Layout: ', validators=[Required()])
    body = StringField('Article: ')
    svg = StringField('Filename of SVG: ', validators=[Required()])
    submit = SubmitField('Submit')

class FindPlanForm(Form):
    # group 1
    # layout_type = RadioField('居室数量: ', choices=[(1, 'Straight'), (2, 'PolyLine')] )
    br_num = IntegerField(u'卧室数量: ')
    lr_num = IntegerField(u'客厅数量: ')
    tol_num = IntegerField(u'厕所数量: ')

    # group 2
    br_width_min = IntegerField(u'从: ')
    br_width_max = IntegerField(u'到: ')

    lr_width_min = IntegerField(u'从: ')
    lr_width_max = IntegerField(u'到: ')

    corridor_length_min = IntegerField(u'从：')
    corridor_length_max = IntegerField(u'到：')

    # choices=[('1', 1),('2',2),('3',3)]
    # choices=[('1', 1),('2',2),('3',3)]
    # choices=[('1', 1),('2',2),('3',3)]
    # room_num = SelectField(u'居室数量：', choices=choices, coerce=int)

    # group 3
    tags = StringField(u'标签: ' )

    # group for test 
    start = DateField('Start Date', format='%m/%d/%y')

    submit = SubmitField('Submit')

# SQL Model

class Plan(db.Model):
    ''' for one house layout or a part of it
    '''
    __tabname__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.Text)
    body = db.Column(db.Text)
    designtime = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    data = db.Column(db.PickleType, default=None)
    graph = db.Column(db.String(128)) # svg file name
    square = db.Column(db.Float, default=0.0)
    brnum = db.Column(db.Integer, default=0)

# class FloorPlan(db.Model):
    # publicsquare = db.Column(db.Float, default=0.0)

# class Project(db.Model):
#     __tabname__ = 'project'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     timeStamp = db.Column(db.DateTime)
#     designer = db.Column(db.String(64))


if __name__ == '__main__':

    app.run()
