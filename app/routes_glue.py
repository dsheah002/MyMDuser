from app import app, db
from app.models_glue import GlueType, GlueDescription

from flask import Flask, render_template


@app.route("/glue")
def show_glue():
    all_glue = db.session.query(GlueType, GlueDescription).join(GlueDescription).all()
    return render_template("glue.html", glues=all_glue)


@app.route("/glue_type")
def show_glue_types():
    all_glue_type = GlueType.query.order_by(GlueType.glue_type_id).all()
    return render_template("glue_type.html", glue_types=all_glue_type)


@app.route("/glue_type/<glue_type_id>")
def show_glue_descriptions(glue_type_id):
    all_glue_description = GlueDescription.query.filter_by(glue_type_id=glue_type_id). \
        order_by(GlueDescription.received_date.desc(), GlueDescription.created_time.desc(),
                 GlueDescription.withdraw_date).all()

    return render_template("glue_description.html",
                           glue_type=GlueType.query.filter_by(glue_type_id=glue_type_id).first(),
                           glue_descriptions=all_glue_description)
