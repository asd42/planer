from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import Organization, Typemachinery, Modelsmachinery, Divisions


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Вход')


class Faddorganization(FlaskForm):
    fullname = StringField('Полное наименование', validators=[DataRequired()])
    name = StringField('Наименование')
    inn = IntegerField('ИНН', validators=[DataRequired()])
    kpp = IntegerField('КПП')
    okpo = IntegerField('ОКПО')
    off_address = StringField('Юридический адрес')
    post_address = StringField('Почтовый адрес')
    head_position = StringField('Должность руководителя')
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    patronymic = StringField('Отчество')
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Записать')

    def validate_fullname(self, fullname):
        org = Organization.query.filter_by(fullname=fullname.data).first()
        if org is not None:
            raise ValidationError('Please use a different fullname.')

    def validate_inn(self, inn):
        inn = Organization.query.filter_by(inn=inn.data).first()
        if inn is not None:
            raise ValidationError('Please use a different inn.')


class Faddtypemashinery(FlaskForm):
    typename = StringField('Наименование', validators=[DataRequired()])
    submit = SubmitField('Записать')

    def validate_typename(self, typename):
        typename = Typemachinery.query.filter_by(typename=typename.data).first()
        if typename is not None:
            raise ValidationError('Please use a different typename.')


class Faddmodel(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
#    type = SelectField('Типы техники', choices=[('1','один'),('2','два')])
    type = SelectField('Типы техники', coerce=int)
    submit = SubmitField('Записать')

    def validate_name(self, name):
        name = Modelsmachinery.query.filter_by(name=name.data).first()
        if name is not None:
            raise ValidationError('Please use a different name.')


class Feditmodel(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
#    type = SelectField('Типы техники', choices=[('1','один'),('2','два')])
    type = SelectField('Типы техники', coerce=int)
    submit = SubmitField('Записать')

#   def validate_name(self, name):
#       name = Modelsmachinery.query.filter_by(name=name.data).first()
#       if name is not None:
#           raise ValidationError('Please use a different name.')


class Fadddivision(FlaskForm):
    name = StringField('Наименование')
    abbreviation = StringField('Аббревиатура', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Записать')

    def validate_name(self, name):
        name = Divisions.query.filter_by(name=name.data).first()
        if name is not None:
            raise ValidationError('Please use a different name.')

    def validate_abbreviation(self, abbreviation):
        abbreviation = Divisions.query.filter_by(abbreviation=abbreviation.data).first()
        if abbreviation is not None:
            raise ValidationError('Please use a different abbreviation.')


class Faddcontract(FlaskForm):
    date = DateField('Дата')
    number = StringField('Номер')
    contractor = SelectField('Контрагент', coerce=int)
    name = StringField('Предмет контракта')
    price = FloatField('Цена контракта')
    end_date = DateField('Срок выполнения работ')
    submit = SubmitField('Записать')
