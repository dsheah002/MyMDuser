from app import app, db
from app.models_lead import LeadType, LeadDescription

from flask import Flask, render_template


@app.route("/lead_frame")
def show_lead():
    all_lead = db.session.query(LeadType, LeadDescription).join(LeadDescription).all()
    return render_template("lead.html", leads=all_lead)


@app.route("/lead_type")
def show_lead_types():
    all_lead_type = LeadType.query.order_by(LeadType.lead_type_id).all()
    return render_template("lead_type.html", lead_types=all_lead_type)


@app.route("/lead_type/<lead_type_id>")
def show_lead_descriptions(lead_type_id):
    all_lead_description = LeadDescription.query.filter_by(lead_type_id=lead_type_id). \
        order_by(LeadDescription.received_date.desc(), LeadDescription.created_time.desc(),
                 LeadDescription.withdraw_date).all()

    return render_template("lead_description.html",
                           lead_type=LeadType.query.filter_by(lead_type_id=lead_type_id).first(),
                           lead_descriptions=all_lead_description)
