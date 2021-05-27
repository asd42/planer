from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, Faddorganization, Faddtypemashinery, Faddmodel
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Organization, Typemachinery, Modelsmachinery
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Домашняя страница')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_organization', methods=['GET', 'POST'])
def add_org():
    form = Faddorganization()
    flash('Cjj,otybt')
    if form.validate_on_submit():
        org = Organization(fullname=form.fullname.data,
                           name=form.name.data,
                           inn=form.inn.data,
                           kpp=form.kpp.data,
                           okpo=form.okpo.data,
                           off_address=form.off_address.data,
                           post_address=form.post_address.data,
                           head_position=form.head_position.data,
                           last_name=form.last_name.data,
                           first_name=form.first_name.data,
                           patronymic=form.patronymic.data,
                           email=form.email.data)
        db.session.add(org)
        db.session.commit()
        flash('Контрагент добавлен')
        return redirect(url_for('l_org'))
    elif request.method == 'GET':
        flash('Контрагент не добавлен')
    return render_template('add_organizations.html', title='Новый контрагент', form=form)


@app.route('/add_typemashinery', methods=['GET', 'POST'])
def add_typemashinery():
    form1 = Faddtypemashinery()
    if form1.validate_on_submit():
        typem = Typemachinery(typename=form1.typename.data)
        db.session.add(typem)
        db.session.commit()
        flash('Тип добавлен')
        return redirect(url_for('cl'))
    else:
        flash('Контрагент не добавлен')
    return render_template('lists/add_typemashinery.html', title='Новый тип', form=form1)


@app.route('/lists/organizations', methods=['GET', 'POST'])
def l_org():
    org = Organization.query.all()
    return render_template('lists/organizations.html', title='Контрагенты', org=org)


@app.route('/lists/common_list', methods=['GET', 'POST'])
def cl():
    c_list = Typemachinery.query.all()
    return render_template('lists/common_list.html', title='Список', list=c_list)


@app.route('/lists/common_list/delete_row', methods=['POST'])
def delete_row():
    row = request.form['del_id']
    print('hello')
    print(row)
    drow = Typemachinery.query.get(row)
 #   Work.query.filter_by(id=row).delete()
 #   print(stype)

    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('cl'))


@app.route('/lists/models', methods=['GET', 'POST'])
def mod():
    c_list = Modelsmachinery.query.all()
    return render_template('lists/models.html', title='Модели техники', list=c_list)


@app.route('/lists/models/add_model', methods=['GET', 'POST'])
def add_model():
    form1 = Faddmodel()
    if form1.validate_on_submit():
        typem = Modelsmachinery(name=form1.name.data)
        db.session.add(typem)
        db.session.commit()
        flash('Тип добавлен')
        return redirect(url_for('mod'))
    else:
        flash('Контрагент не добавлен')
    return render_template('lists/add_model.html', title='Новый тип', form=form1, type=Typemachinery.query.all())


@app.route('/lists/models/delete_row', methods=['POST'])
def delete_mod():
    row = request.form['del_id']
    print('hello')
    print(row)
    drow = Modelsmachinery.query.get(row)
 #   Work.query.filter_by(id=row).delete()
 #   print(stype)

    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('mod'))
