from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, Faddorganization, Faddtypemashinery, Faddmodel, Fadddivision, Faddcontract, Feditmodel
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Organization, Typemachinery, Modelsmachinery, Divisions, Contract
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
    else:
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


@app.route('/lists/divisions', methods=['GET', 'POST'])
def l_dns():
    dns = Divisions.query.all()
    return render_template('lists/divisions.html', title='Участки', dns=dns)


@app.route('/lists/common_list', methods=['GET', 'POST'])
def cl():
    c_list = Typemachinery.query.all()
    return render_template('lists/common_list.html', title='Список', list=c_list)


@app.route('/lists/common_list/delete_row', methods=['POST'])
def delete_row():
    row = request.form['del_id']
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
    types = db.session.query(Typemachinery).all()
    #    types = Typemachinery.query.all()
    type_list = [(i.id, i.typename) for i in types]
    form1 = Faddmodel()
    form1.type.choices = type_list
    if form1.validate_on_submit():
        typem = Modelsmachinery(name=form1.name.data, type_id=form1.type.data)
        db.session.add(typem)
        db.session.commit()
        flash('Модель добавлена')
        return redirect(url_for('mod'))
    else:
        flash('Модель не добавлена')
    return render_template('lists/add_row.html', title='Новая модель', form=form1, type=Typemachinery.query.all())


@app.route('/lists/models/<int:e_id>/edit_row', methods=['GET', 'POST'])
def edit_mod(e_id):
    # row = request.form[e_id]
    erow = Modelsmachinery.query.get(e_id)
    types = db.session.query(Typemachinery).all()
    type_list = [(i.id, i.typename) for i in types]
    form1 = Feditmodel()
    form1.type.choices = type_list
    if form1.name.data is None:
        form1.name.data = erow.name
    if form1.type.data is None:
        form1.type.data = erow.type_id
    if form1.validate_on_submit():
        erow.name = form1.name.data
        erow.type_id = form1.type.data
        # erow = Modelsmachinery(name=form1.name.data, type_id=form1.type.data)
        # db.session.add(erow)
        db.session.commit()
        flash('Модель изменена')
        print(erow.name)
        return redirect(url_for('mod'))
    else:
        flash('Модель не изменена')

    return render_template('lists/add_row.html', title='Изменить модель', form=form1, type=Typemachinery.query.all())


@app.route('/lists/divisions/add_division', methods=['GET', 'POST'])
def add_dns():
    form1 = Fadddivision()
    if form1.validate_on_submit():
        dns = Divisions(name=form1.name.data,
                        abbreviation=form1.abbreviation.data,
                        email=form1.email.data)
        db.session.add(dns)
        db.session.commit()
        flash('Участок добавлен')
        return redirect(url_for('l_dns'))
    else:
        flash('Участок не добавлен')
    return render_template('lists/add_row.html', title='Новый участок', form=form1, dns=Divisions.query.all())


@app.route('/lists/models/delete_row', methods=['POST'])
def delete_mod():
    row = request.form['del_id']
    print(row)
    drow = Modelsmachinery.query.get(row)
    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('mod'))


@app.route('/lists/divisions/delete_row', methods=['GET', 'POST'])
def delete_dns():
    row = request.form['del_id']
    print(row)
    drow = Divisions.query.get(row)
    db.session.delete(drow)
    db.session.commit()
    return redirect(url_for('l_dns'))


@app.route('/lists/contracts', methods=['GET', 'POST'])
def contracts():
    c_list = Contract.query.all()
    org_list = Organization.query.all()
    return render_template('lists/contracts.html', title='Контракты', list=c_list, org_list=org_list)


@app.route('/lists/contracts/add_contract', methods=['GET', 'POST'])
def add_contract():
    contractors = db.session.query(Organization).all()
    #    types = Typemachinery.query.all()
    cont_list = [(i.id, i.name) for i in contractors]
    addform = Faddcontract()
    addform.contractor.choices = cont_list
    if addform.validate_on_submit():
        contract = Contract(date=addform.date.data,
                            number=addform.number.data,
                            contractor=addform.contractor.data,
                            name=addform.name.data,
                            price=addform.price.data,
                            end_date=addform.end_date.data)
        db.session.add(contract)
        db.session.commit()
        flash('Контракт добавлен')
        return redirect(url_for('contracts'))
    else:
        flash('Контракт не добавлен')
    return render_template('lists/add_row.html', title='Новый контракт', form=addform)
