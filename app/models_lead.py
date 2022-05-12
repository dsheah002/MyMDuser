from app import db
from datetime import datetime


class LeadType(db.Model):
    __tablename__ = 'lead_types'

    lead_type_id = db.Column(db.Integer, primary_key=True)
    lead_no = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    package_no = db.Column(db.String(100))
    title = db.Column(db.String(100))

    lead_description = db.relationship("LeadDescription", cascade="all, delete-orphan")

    def __init__(self, lead_no, supplier, package_no, title):
        self.lead_no = lead_no
        self.supplier = supplier
        self.package_no = package_no
        self.title = title


# factors to classify the lead
class LeadDescription(db.Model):
    __tablename__ = 'lead_descriptions'

    lead_description_id = db.Column(db.Integer, primary_key=True)
    lot_no = db.Column(db.String(100))
    row_location = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    manufacturing_date = db.Column(db.String(100))
    expiry_date = db.Column(db.String(100))
    project_leader = db.Column(db.String(100))
    record_reff = db.Column(db.String(100))
    invoice_no = db.Column(db.String(100))
    purchasing_order = db.Column(db.String(100))
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
    lead_type_id = db.Column(db.Integer, db.ForeignKey('lead_types.lead_type_id'))

    lead_type = db.relationship("LeadType", backref='lead_type')

    def __init__(self, lot_no, row_location, received_date, manufacturing_date, expiry_date, project_leader,
                 record_reff, invoice_no, purchasing_order, incoming_qty, withdraw_date, withdraw_qty,
                 withdraw_by, withdraw_purpose, balance, trans_type, release_status, expiry_status, created_time,
                 lead_type_id):
        self.lot_no = lot_no
        self.row_location = row_location
        self.received_date = received_date
        self.manufacturing_date = manufacturing_date
        self.expiry_date = expiry_date
        self.project_leader = project_leader
        self.record_reff = record_reff
        self.invoice_no = invoice_no
        self.purchasing_order = purchasing_order
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
        self.lead_type_id = lead_type_id


db.create_all()
db.session.commit()
