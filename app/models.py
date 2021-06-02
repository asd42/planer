from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
#    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    staff = db.relationship('Staff', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    inn = db.Column(db.String(12), index=True, unique=True)
    kpp = db.Column(db.String(9))
    okpo = db.Column(db.String(10))
    off_address = db.Column(db.String, index=True)
    post_address = db.Column(db.String, index=True)
    head_position = db.Column(db.String(30))
    last_name = db.Column(db.String(32), index=True)
    first_name = db.Column(db.String(32), index=True)
    patronymic = db.Column(db.String(32), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    accounting = db.Column(db.Boolean, index=True)
    staff = db.relationship('Staff', backref='organization', lazy='dynamic')
    divisions = db.relationship('Divisions', backref='organization', lazy='dynamic')

    def __repr__(self):
        return '<Organization {}>'.format(self.fullname)


class Divisions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    abbreviation = db.Column(db.String(8), index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    staff = db.relationship('Staff', backref='division', lazy='dynamic')

    def __repr__(self):
        return '<Division {}>'.format(self.name)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    users = db.relationship('Staff', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(32), index=True)
    first_name = db.Column(db.String(32), index=True)
    patronymic = db.Column(db.String(32), index=True)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))

    def __repr__(self):
        return '<Staff {}>'.format(self.last_name)


class Typecontract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(64), index=True, unique=True)
    we_sell = db.Column(db.Boolean, index=True)
    protected = db.Column(db.Boolean)

    def __repr__(self):
        return '<TypeContract {}>'.format(self.typename)


class Typefulfillment(db.Model):  # тип выполнения
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(64), index=True, unique=True)
    protected = db.Column(db.Boolean)

    def __repr__(self):
        return '<TypeFulfillment {}>'.format(self.typename)


class Typemachinery(db.Model):  # тип техники
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(64), index=True, unique=True)
    models = db.relationship('Modelsmachinery', backref='model_type', lazy='dynamic')
    def __repr__(self):
        return '<TypeMachinery {}>'.format(self.typename)


class Modelsmachinery(db.Model):  # модель техники
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('typemachinery.id'))

    def __repr__(self):
        return '<ModelsMachinery {}>'.format(self.name)


class Machinery(db.Model):  # конкретная единица техники
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    model_id = db.Column(db.Integer, db.ForeignKey('modelsmachinery.id'), index=True)
    type_id = db.Column(db.Integer, db.ForeignKey('typemachinery.id'), index=True)
    division = db.Column(db.Integer, db.ForeignKey('divisions.id'), index=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('staff.id'), index=True)
    number = db.Column(db.String(15), index=True, unique=True)

    def __repr__(self):
        return '<ModelsMachinery {}>'.format(self.name)


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('typecontract.id'))
    typefulfillment_id = db.Column(db.Integer, db.ForeignKey('typefulfillment.id'))
    accounting_method = db.Column(db.Integer)  # 1-по ед. расценкам, 2-по смете, 3-акт за машиночасы, 4-накладная
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    price = db.Column(db.Float, index=True)
    organization = db.Column(db.Integer, db.ForeignKey('organization.id'))
    contractor = db.Column(db.Integer, db.ForeignKey('organization.id'))
    number = db.Column(db.String(32), index=True)
    date = db.Column(db.Date, index=True)
    name = db.Column(db.String(128), index=True)
    full_name = db.Column(db.String, index=True)


class Divisionscontract(db.Model):  # привязка договора к участку
    id = db.Column(db.Integer, primary_key=True)
    division = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'))


class Typesownership(db.Model):  # тип собственности
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, unique=True)
    protected = db.Column(db.Boolean)


class Roads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    abbreviation = db.Column(db.String(16), index=True)
    length = db.Column(db.Integer)
    start_address = db.Column(db.Integer)
    type_of_ownership = db.Column(db.Integer, db.ForeignKey('typesownership.id'))
    owner = db.Column(db.Integer, db.ForeignKey('organization.id'))

    def __repr__(self):
        return '<Roads {}>'.format(self.abbreviation)


class Roadstructure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.SmallInteger, index=True)  # 1-мост, 2-труба, 3-лед. переправа
    road = db.Column(db.Integer, db.ForeignKey('roads.id'))
    address = db.Column(db.Integer, index=True)  # метры от км 0+000
    barrier = db.Column(db.String(32), index=True)
    length = db.Column(db.Integer)  # для мостов и переправ
    roadway_area = db.Column(db.Integer)  # для мостов
    sidewalk_area = db.Column(db.Integer)  # для мостов
    material = db.Column(db.Integer, db.ForeignKey('materials.id'), index=True)  # заменить на список
    diameter = db.Column(db.Integer)  # в мм для труб
    width = db.Column(db.Integer)  # для переправ
    lifting_capacity = db.Column(db.Integer, index=True)  # грузоподъемность


class Roadsincontract(db.Model):  # привязка дороги к контракту
    id = db.Column(db.Integer, primary_key=True)
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'))
    road = db.Column(db.Integer, db.ForeignKey('roads.id'))
    start_address = db.Column(db.Integer, index=True)  # метры от км 0+000
    end_address = db.Column(db.Integer, index=True)  # метры от км 0+000


class Unitrates(db.Model):  # единичные расценки
    id = db.Column(db.Integer, primary_key=True)
    contract = db.Column(db.Integer, db.ForeignKey('contract.id'))
    job_title = db.Column(db.String(256), index=True)
    price = db.Column(db.Float)
    zone = db.Column(db.SmallInteger, index=True)  # зона 1 или 2
    season_winter = db.Column(db.Boolean, index=True)  # зимняя работа
    tag = db.Column(db.String(32), index=True)  # группа работ (знаки, мосты, и т.д.)


class Planeprice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date, index=True)
    model = db.Column(db.Integer, db.ForeignKey('modelsmachinery.id'))
    price = db.Column(db.Float)


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), index=True)
    date = db.Column(db.Date, index=True)
    unit_rate_id = db.Column(db.Integer, db.ForeignKey('unitrates.id'), index=True)
    road_id = db.Column(db.Integer, db.ForeignKey('roads.id'), index=True)
    address = db.Column(db.Integer)
    address2 = db.Column(db.Integer)  # если требуется
    volume = db.Column(db.Float)


class Usedmashines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), index=True)
    mashinery_id = db.Column(db.Integer, db.ForeignKey('machinery.id'), index=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('staff.id'), index=True)
    volume = db.Column(db.Float)


class Usedmaterials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), index=True)
    material = db.Column(db.Integer, db.ForeignKey('materials.id'), index=True)
    source = db.Column(db.Integer, db.ForeignKey('heaps.id'), index=True)
    volume = db.Column(db.Float)


class Materials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, db.ForeignKey('units.id'), index=True)  # ед. измерения
    full_name = db.Column(db.String(128), index=True)


class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True)
    full_name = db.Column(db.String(128), index=True)
    OKEI = db.Column(db.Integer, index=True)


class Heaps(db.Model):  # отвалы
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True)  # если есть (карьер)
    road = db.Column(db.Integer, db.ForeignKey('roads.id'), index=True)
    address = db.Column(db.Integer, index=True)
    distance_from_road = db.Column(db.Integer)
