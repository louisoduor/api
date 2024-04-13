from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
from models import Asset, Employee, AssignedAsset, RequestedAsset

from flask_migrate import Migrate
import uuid
import os
from faker import Faker

from models import  db

fake = Faker()


app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(base_dir, 'data')
os.makedirs(db_dir, exist_ok=True)

db_path_assets = os.path.join(db_dir, 'assets.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path_assets}'

migrate = Migrate(app, db)
db.init_app(app)



@app.route('/assets', methods=['GET'])
def get_all_assets():
    assets = Asset.query.all()
    asset_list = []
    for asset in assets:
        asset_data = {
            'id': asset.id,
            'name': asset.name,
            'serial_no': asset.serial_no,
            'model': asset.model,
            'brand': asset.brand,
            'status': asset.status
        }
        asset_list.append(asset_data)
    return jsonify(asset_list)

@app.route('/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Asset not found'}), 404
    asset_data = {
        'id': asset.id,
        'name': asset.name,
        'serial_no': asset.serial_no,
        'model': asset.model,
        'brand': asset.brand,
        'status': asset.status
    }
    return jsonify(asset_data)

@app.route('/assets', methods=['POST'])
def create_asset():
    data = request.get_json()
    asset = Asset(
        name=data['name'],
        serial_no=data['serial_no'],
        model=data['model'],
        brand=data['brand'],
        status=data['status']
    )
    db.session.add(asset)
    db.session.commit()
    return jsonify({'message': 'Asset created successfully'}), 201

@app.route('/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Asset not found'}), 404
    data = request.get_json()
    asset.name = data['name']
    asset.serial_no = data['serial_no']
    asset.model = data['model']
    asset.brand = data['brand']
    asset.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Asset updated successfully'})

@app.route('/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Asset not found'}), 404
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted successfully'})

@app.route('/assigned_assets', methods=['GET'])
def get_all_assigned_assets():
    assigned_assets = AssignedAsset.query.all()
    assigned_assets_list = []
    for asset in assigned_assets:
        asset_data = {
            'id': asset.id,
            'name': asset.name,
            'serial_no': asset.serial_no,
            'model': asset.model,
            'asset_id': asset.asset_id,
            'status': asset.status,
            'assigned_to': asset.assigned_to,
            'assigned_date': asset.assigned_date.strftime('%Y-%m-%d') if asset.assigned_date else None
        }
        assigned_assets_list.append(asset_data)
    return jsonify(assigned_assets_list)

@app.route('/assigned_assets/<int:asset_id>', methods=['GET'])
def get_assigned_asset(asset_id):
    asset = AssignedAsset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Assigned Asset not found'}), 404
    asset_data = {
        'id': asset.id,
        'name': asset.name,
        'serial_no': asset.serial_no,
        'model': asset.model,
        'asset_id': asset.asset_id,
        'status': asset.status,
        'assigned_to': asset.assigned_to,
        'assigned_date': asset.assigned_date.strftime('%Y-%m-%d') if asset.assigned_date else None
    }
    return jsonify(asset_data)


@app.route('/assigned_assets', methods=['POST'])
def create_assigned_asset():
    data = request.get_json()
    assigned_asset = AssignedAsset(
        name=data['name'],
        serial_no=data['serial_no'],
        model=data['model'],
        asset_id=data['asset_id'],
        status=data['status'],
        assigned_to=data['assigned_to'],
        assigned_date=data['assigned_date']
    )
    db.session.add(assigned_asset)
    db.session.commit()
    return jsonify({'message': 'Assigned Asset created successfully'}), 201

@app.route('/assigned_assets/<int:asset_id>', methods=['PUT'])
def update_assigned_asset(asset_id):
    asset = AssignedAsset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Assigned Asset not found'}), 404
    data = request.get_json()
    asset.name = data['name']
    asset.serial_no = data['serial_no']
    asset.model = data['model']
    asset.asset_id = data['asset_id']
    asset.status = data['status']
    asset.assigned_to = data['assigned_to']
    asset.assigned_date = data['assigned_date']
    db.session.commit()
    return jsonify({'message': 'Assigned Asset updated successfully'})

@app.route('/assigned_assets/<int:asset_id>', methods=['DELETE'])
def delete_assigned_asset(asset_id):
    asset = AssignedAsset.query.get(asset_id)
    if not asset:
        return jsonify({'message': 'Assigned Asset not found'}), 404
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Assigned Asset deleted successfully'})


@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    employee_list = []
    for employee in employees:
        employee_data = {
            'id': employee.id,
            'public_id': employee.public_id,
            'name': employee.name,
            'department': employee.department,
            'admin': employee.admin
        }
        employee_list.append(employee_data)
    return jsonify(employee_list)

@app.route('/employees/<public_id>', methods=['GET'])
def get_employee(public_id):
    employee = Employee.query.filter_by(public_id=public_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    employee_data = {
        'id': employee.id,
        'public_id': employee.public_id,
        'name': employee.name,
        'department': employee.department,
        'admin': employee.admin
    }
    return jsonify(employee_data)

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_employee = Employee(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        department=data['department'],
        admin=data['admin'],
        password=hashed_password
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully'}), 201

@app.route('/employees/<public_id>', methods=['PUT'])
def update_employee(public_id):
    employee = Employee.query.filter_by(public_id=public_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    data = request.get_json()
    employee.name = data['name']
    employee.department = data['department']
    employee.admin = data['admin']
    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/employees/<public_id>', methods=['DELETE'])
def delete_employee(public_id):
    employee = Employee.query.filter_by(public_id=public_id).first()
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

@app.route('/requested_assets', methods=['GET'])
def get_all_requested_assets():
    requested_assets = RequestedAsset.query.all()
    requested_assets_list = []
    for asset in requested_assets:
        asset_data = {
            'id': asset.id,
            'asset_id': asset.asset_id,
            'employee_id': asset.employee_id,
            'status': asset.status
        }
        requested_assets_list.append(asset_data)
    return jsonify(requested_assets_list)

@app.route('/requested_assets/<int:requested_asset_id>', methods=['GET'])
def get_requested_asset(requested_asset_id):
    requested_asset = RequestedAsset.query.get(requested_asset_id)
    if not requested_asset:
        return jsonify({'message': 'Requested Asset not found'}), 404
    asset_data = {
        'id': requested_asset.id,
        'asset_id': requested_asset.asset_id,
        'employee_id': requested_asset.employee_id,
        'status': requested_asset.status
    }
    return jsonify(asset_data)

@app.route('/requested_assets', methods=['POST'])
def create_requested_asset():
    data = request.get_json()
    requested_asset = RequestedAsset(
        asset_id=data['asset_id'],
        employee_id=data['employee_id'],
        status=data['status']
    )
    db.session.add(requested_asset)
    db.session.commit()
    return jsonify({'message': 'Requested Asset created successfully'}), 201

@app.route('/requested_assets/<int:requested_asset_id>', methods=['PUT'])
def update_requested_asset(requested_asset_id):
    requested_asset = RequestedAsset.query.get(requested_asset_id)
    if not requested_asset:
        return jsonify({'message': 'Requested Asset not found'}), 404
    data = request.get_json()
    requested_asset.asset_id = data['asset_id']
    requested_asset.employee_id = data['employee_id']
    requested_asset.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Requested Asset updated successfully'})

@app.route('/requested_assets/<int:requested_asset_id>', methods=['DELETE'])
def delete_requested_asset(requested_asset_id):
    requested_asset = RequestedAsset.query.get(requested_asset_id)
    if not requested_asset:
        return jsonify({'message': 'Requested Asset not found'}), 404
    db.session.delete(requested_asset)
    db.session.commit()
    return jsonify({'message': 'Requested Asset deleted successfully'})

def init_db():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)