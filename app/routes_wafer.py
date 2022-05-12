from app import app, db
from app.models_wafer import WaferType, WaferDescription

from flask import Flask, render_template


@app.route("/wafer")
def show_wafer():
    all_wafer = db.session.query(WaferType, WaferDescription).join(WaferDescription).all()
    return render_template("wafer.html", wafers=all_wafer)


@app.route("/wafer_type")
def show_wafer_types():
    all_wafer_type = WaferType.query.order_by(WaferType.wafer_type_id).all()
    return render_template("wafer_type.html", wafer_types=all_wafer_type)


@app.route("/wafer_type/<wafer_type_id>")
def show_wafer_descriptions(wafer_type_id):
    all_wafer_description = WaferDescription.query.filter_by(wafer_type_id=wafer_type_id). \
        order_by(WaferDescription.slice_no, WaferDescription.wafer_description_id).all()

    return render_template("wafer_description.html",
                           wafer_type=WaferType.query.filter_by(wafer_type_id=wafer_type_id).first(),
                           wafer_descriptions=all_wafer_description)
