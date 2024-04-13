from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    serial_no = db.Column(db.String(50))
    model = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    status = db.Column(db.String(50))

    def __repr__(self):
        return f"Asset(id={self.id}, name={self.name}, serial_no={self.serial_no}, model={self.model}, brand={self.brand}, status={self.status})"

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    department = db.Column(db.String(100))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"Employee(id={self.id}, public_id={self.public_id}, name={self.name}, department={self.department}, admin={self.admin})"

class AssignedAsset(db.Model):
    __tablename__ = 'assigned_assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    serial_no = db.Column(db.Integer)
    model = db.Column(db.String(50))
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    status = db.Column(db.Boolean)
    assigned_to = db.Column(db.String(100))
    assigned_date = db.Column(db.Date)

    def __repr__(self):
        return f"AssignedAsset(id={self.id}, name={self.name}, serial_no={self.serial_no}, model={self.model}, asset_id={self.asset_id}, status={self.status}, assigned_to={self.assigned_to}, assigned_date={self.assigned_date})"


class RequestedAsset(db.Model):
    __tablename__ = 'requested_assets'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    employee_id = db.Column(db.Integer)
    status = db.Column(db.String(50))
    name = db.Column(db.String(100))

    def __repr__(self):
        return f"RequestedAsset(id={self.id}, asset_id={self.asset_id}, employee_id={self.employee_id}, status={self.status})"
