from app import app, db
from app.models_mold import MoldType, MoldDescription

from flask import Flask, render_template


@app.route("/mold_compound")
def show_mold():
    all_mold = db.session.query(MoldType, MoldDescription).join(MoldDescription).all()
    return render_template("mold.html", molds=all_mold)


@app.route("/mold_type")
def show_mold_types():
    all_mold_type = MoldType.query.order_by(MoldType.mold_type_id).all()
    return render_template("mold_type.html", mold_types=all_mold_type)


@app.route("/mold_type/<mold_type_id>")
def show_mold_descriptions(mold_type_id):
    all_mold_description = MoldDescription.query.filter_by(mold_type_id=mold_type_id). \
        order_by(MoldDescription.received_date.desc(), MoldDescription.created_time.desc(),
                 MoldDescription.withdraw_date).all()

    return render_template("mold_description.html",
                           mold_type=MoldType.query.filter_by(mold_type_id=mold_type_id).first(),
                           mold_descriptions=all_mold_description)
