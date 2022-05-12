from app import db
from datetime import datetime


class MoldType(db.Model):
    __tablename__ = 'mold_types'

    mold_type_id = db.Column(db.Integer, primary_key=True)
    mold_name = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    pellet_size = db.Column(db.String(100))
    part_no = db.Column(db.String(100))

    mold_description = db.relationship("MoldDescription", cascade="all, delete-orphan")

    def __init__(self, mold_name, supplier, pellet_size, part_no):
        self.mold_name = mold_name
        self.supplier = supplier
        self.pellet_size = pellet_size
        self.part_no = part_no


class MoldDescription(db.Model):
    __tablename__ = 'mold_descriptions'

    mold_description_id = db.Column(db.Integer, primary_key=True)
    lot_no = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    manufacturing_date = db.Column(db.String(100))
    expiry_date = db.Column(db.String(100))
    project_leader = db.Column(db.String(100))
    incoming_qty = db.Column(db.String(100))
    withdraw_date = db.Column(db.String(100))
    withdraw_qty = db.Column(db.String(100))
    withdraw_by = db.Column(db.String(100))
    withdraw_purpose = db.Column(db.String(100))
    balance = db.Column(db.String(100))
    trans_type = db.Column(db.String(100))
    release_status = db.Column(db.String(100))
    expiry_status = db.Column(db.String(100))
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    mold_type_id = db.Column(db.Integer, db.ForeignKey('mold_types.mold_type_id'))

    mold_type = db.relationship("MoldType", backref='mold_type')

    def __init__(self, lot_no, received_date, manufacturing_date, expiry_date, project_leader, incoming_qty,
                 withdraw_date, withdraw_qty, withdraw_by, withdraw_purpose, balance, trans_type, release_status,
                 expiry_status, created_time, mold_type_id):
        self.lot_no = lot_no
        self.received_date = received_date
        self.manufacturing_date = manufacturing_date
        self.expiry_date = expiry_date
        self.project_leader = project_leader
        self.incoming_qty = incoming_qty
        self.withdraw_date = withdraw_date
        self.withdraw_qty = withdraw_qty
        self.withdraw_by = withdraw_by
        self.withdraw_purpose = withdraw_purpose
        self.balance = balance
        self.trans_type = trans_type
        self.release_status = release_status
        self.expiry_status = expiry_status
        self.created_time = created_time
        self.mold_type_id = mold_type_id


db.create_all()
db.session.commit()
