from random import choice as rc
from faker import Faker
from app import app, db
from models import Asset, Employee, AssignedAsset, RequestedAsset

fake = Faker()

def generate_fake_data():
    with app.app_context():
        try:
            asset_types = ['Laptop', 'Monitor', 'Printer', 'Scanner', 'Vehicle']
            for _ in range(10):
                asset_type = rc(asset_types)
                asset_name = fake.word() + f" {asset_type}"
                asset = Asset(
                    name=asset_name,
                    serial_no=fake.random_int(min=1000, max=9999),
                    model=fake.word() + " Series",
                    brand=fake.company(),
                    status=rc(('Available', 'In Use', 'Maintenance'))
                )
                db.session.add(asset)

            for _ in range(5):
                employee = Employee(
                    public_id=str(fake.uuid4()),
                    name=fake.name(),
                    department=fake.job(),
                    admin=fake.boolean()
                )
                db.session.add(employee)

            for _ in range(8):
                assigned_asset_name = fake.word() + f" {rc(asset_types)}"
                assigned_asset = AssignedAsset(
                    name=assigned_asset_name,
                    serial_no=fake.random_int(min=1000, max=9999),
                    model=fake.word() + " Series",
                    asset_id=fake.random_int(min=1, max=10),
                    status=fake.boolean(),
                    assigned_to=fake.name(),
                    assigned_date=fake.date_this_year()
                )
                db.session.add(assigned_asset)

            for _ in range(5): 
                requested_asset_name = fake.word() + f" {rc(asset_types)}"
                requested_asset = RequestedAsset(
                    asset_id=fake.random_int(min=1, max=10),  
                    employee_id=fake.random_int(min=1, max=5), 
                    status=rc(('Pending', 'Approved', 'Rejected')),
                    name=requested_asset_name  
                )
                db.session.add(requested_asset)

            db.session.commit()
            print("Fake data generated and added to the database.")
        except Exception as e:
            print(f"Error generating fake data: {e}")


generate_fake_data()
