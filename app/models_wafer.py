from app import db
from datetime import datetime


class WaferType(db.Model):
    __tablename__ = 'wafer_types'

    wafer_type_id = db.Column(db.Integer, primary_key=True)
    wafer_device = db.Column(db.String(100))
    wafer_charge = db.Column(db.String(100))

    wafer_description = db.relationship("WaferDescription", cascade="all, delete-orphan")

    def __init__(self, wafer_device, wafer_charge):
        self.wafer_device = wafer_device
        self.wafer_charge = wafer_charge


# factors to classify the wafer
class WaferDescription(db.Model):
    __tablename__ = 'wafer_descriptions'

    wafer_description_id = db.Column(db.Integer, primary_key=True)
    storage_location = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    project_leader = db.Column(db.String(100))
    incoming_qty = db.Column(db.String(100))
    slice_no = db.Column(db.String(100))
    withdraw_date = db.Column(db.String(100))
    withdraw_by = db.Column(db.String(100))
    withdraw_purpose = db.Column(db.String(100))
    balance = db.Column(db.String(100))
    trans_type = db.Column(db.String(100))
    release_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    wafer_type_id = db.Column(db.Integer, db.ForeignKey('wafer_types.wafer_type_id'))

    wafer_type = db.relationship("WaferType", backref='wafer_type')

    def __init__(self, storage_location, received_date, project_leader, incoming_qty, slice_no, withdraw_date,
                 withdraw_by, withdraw_purpose, balance, trans_type, release_status, created_time, wafer_type_id):
        self.storage_location = storage_location
        self.received_date = received_date
        self.project_leader = project_leader
        self.incoming_qty = incoming_qty
        self.slice_no = slice_no
        self.withdraw_date = withdraw_date
        self.withdraw_by = withdraw_by
        self.withdraw_purpose = withdraw_purpose
        self.balance = balance
        self.trans_type = trans_type
        self.release_status = release_status
        self.created_time = created_time
        self.wafer_type_id = wafer_type_id


db.create_all()
db.session.commit()
