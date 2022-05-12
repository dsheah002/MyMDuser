from app import app, db
from app.models import EditHistory
from app.models_mold import MoldType, MoldDescription

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_required
from datetime import datetime


@app.route("/mold_compound")
@login_required
def show_mold():
    all_mold = db.session.query(MoldType, MoldDescription).join(MoldDescription).all()
    return render_template("mold.html", molds=all_mold)


@app.route("/mold_type")
@login_required
def show_mold_types():
    all_mold_type = MoldType.query.order_by(MoldType.mold_type_id).all()
    return render_template("mold_type.html", mold_types=all_mold_type)


@app.route("/mold_type/<mold_type_id>")
@login_required
def show_mold_descriptions(mold_type_id):
    all_mold_description = MoldDescription.query.filter_by(mold_type_id=mold_type_id). \
        order_by(MoldDescription.received_date.desc(), MoldDescription.created_time.desc(),
                 MoldDescription.withdraw_date).all()

    return render_template("mold_description.html",
                           mold_type=MoldType.query.filter_by(mold_type_id=mold_type_id).first(),
                           mold_descriptions=all_mold_description)


@app.route("/mold_type/insert", methods=['POST'])
def insert_mold_type():
    if request.method == 'POST':
        mold_name = request.form['mold_name']
        supplier = request.form['supplier']
        pellet_size = request.form['pellet_size']
        part_no = request.form['part_no']

        new_content = mold_name + ', ' + supplier + ', ' + pellet_size + ', ' + part_no
        new_mold_type = MoldType(mold_name, supplier, pellet_size, part_no)

        db.session.add(new_mold_type)
        db.session.commit()
        flash("Mold type added successfully")

        new_edit = EditHistory(edit_type="Add", edit_material="Mold", edit_page="Transaction 1st page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_mold_types'))


@app.route("/mold_description/insert/<mold_type_id>", methods=['POST'])
def insert_mold_description(mold_type_id):
    original_mold_type = MoldType.query.filter_by(mold_type_id=mold_type_id).first()
    if request.method == 'POST':
        lot_no = request.form['lot_no']
        received_date = request.form['received_date']
        manufacturing_date = request.form['manufacturing_date']
        expiry_date = request.form['expiry_date']
        project_leader = request.form['project_leader']
        incoming_qty = request.form['incoming_qty']
        withdraw_date = ""
        withdraw_qty = ""
        withdraw_by = ""
        withdraw_purpose = ""
        balance = incoming_qty
        trans_type = "incoming"
        release_status = ""
        expiry_status = ""
        created_time = datetime.now()

        new_content = '(Mold type)' + original_mold_type.mold_name + ', ' + lot_no + ', ' + received_date + ', ' \
                      + expiry_date + ', ' + manufacturing_date + ', ' + project_leader + ', ' + incoming_qty

        new_mold_description = MoldDescription(lot_no, received_date, expiry_date, manufacturing_date, project_leader,
                                               float(incoming_qty), withdraw_date, withdraw_by, withdraw_qty,
                                               withdraw_purpose, float(balance), trans_type, release_status,
                                               expiry_status, created_time, mold_type_id=mold_type_id)

        db.session.add(new_mold_description)
        db.session.commit()
        flash("Mold description added successfully")

        new_edit = EditHistory(edit_type="Add", edit_material="Mold", edit_page="Transaction 2nd page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_mold_descriptions', mold_type_id=mold_type_id))


@app.route('/mold_type/update', methods=['GET', 'POST'])
def update_mold_type():
    if request.method == 'POST':
        mold_type_to_update = MoldType.query.get(request.form.get('mold_type_id'))
        old_content = mold_type_to_update.mold_name + ', ' + mold_type_to_update.supplier + ', ' \
                      + mold_type_to_update.pellet_size + ', ' + mold_type_to_update.part_no

        mold_type_to_update.mold_name = request.form['mold_name']
        mold_type_to_update.supplier = request.form['supplier']
        mold_type_to_update.pellet_size = request.form['pellet_size']
        mold_type_to_update.part_no = request.form['part_no']

        db.session.commit()
        flash("Mold type [" + str(mold_type_to_update.mold_name) + "] is updated successfully")

        new_content = mold_type_to_update.mold_name + ', ' + mold_type_to_update.supplier + ', ' \
                      + mold_type_to_update.pellet_size + ', ' + mold_type_to_update.part_no

        new_edit = EditHistory(edit_type="Update", edit_material="Mold", edit_page="Transaction 1st page",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

        return redirect(url_for('show_mold_types'))


@app.route('/mold_description/update/<mold_description_id>', methods=['GET', 'POST'])
def update_mold_description(mold_description_id):
    if request.method == 'POST':
        mold_description_to_update = MoldDescription.query.filter_by(mold_description_id=mold_description_id).first()
        original_mold_type_id = mold_description_to_update.mold_type_id
        original_mold_type = MoldType.query.filter_by(mold_type_id=original_mold_type_id).first()

        old_content = '(Mold type)' + original_mold_type.mold_name + ', ' + mold_description_to_update.lot_no + ', ' \
                      + mold_description_to_update.received_date + ', ' \
                      + mold_description_to_update.manufacturing_date + ', ' + mold_description_to_update.expiry_date \
                      + mold_description_to_update.project_leader + ', ' + mold_description_to_update.incoming_qty

        mold_description_to_update.lot_no = request.form['lot_no']
        mold_description_to_update.received_date = request.form['received_date']
        mold_description_to_update.manufacturing_date = request.form['manufacturing_date']
        mold_description_to_update.expiry_date = request.form['expiry_date']
        mold_description_to_update.project_leader = request.form['project_leader']
        mold_description_to_update.incoming_qty = request.form['incoming_qty']
        mold_description_to_update.balance = mold_description_to_update.incoming_qty

        db.session.commit()
        flash("Mold description for lot no. [" + str(mold_description_to_update.lot_no) + "] is updated successfully")

        new_content = '(Mold type)' + original_mold_type.mold_name + ', ' + mold_description_to_update.lot_no + ', ' \
                      + mold_description_to_update.received_date + ', ' + mold_description_to_update.manufacturing_date + ', ' \
                      + mold_description_to_update.expiry_date + ', ' + mold_description_to_update.project_leader \
                      + ', ' + mold_description_to_update.incoming_qty

        new_edit = EditHistory(edit_type="Update", edit_material="Mold", edit_page="Transaction 2nd page",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_mold_descriptions', mold_type_id=original_mold_type_id))


@app.route('/mold_inventory/update/<mold_description_id>', methods=['GET', 'POST'])
def update_mold_inventory(mold_description_id):
    if request.method == 'POST':
        mold_to_update = MoldDescription.query.filter_by(mold_description_id=mold_description_id).first()
        original_mold_type_id = mold_to_update.mold_type_id
        original_mold_type = MoldType.query.filter_by(mold_type_id=original_mold_type_id).first()

        old_content = '(Mold type)' + original_mold_type.mold_name + ', (lot no.)' + mold_to_update.lot_no + ', ' \
                      + mold_to_update.balance + ', ' + mold_to_update.release_status

        mold_to_update.balance = request.form['balance']
        mold_to_update.release_status = request.form['release_status']
        flash("Mold information for mold type [" + str(original_mold_type.mold_name) + "] and lot no. [" +
              str(mold_to_update.lot_no) + "] is updated successfully")

        # edit history
        new_content = '(Mold type)' + original_mold_type.mold_name + ', (lot no.)' + mold_to_update.lot_no + ', ' \
                      + mold_to_update.balance + ', ' + mold_to_update.release_status
        new_edit = EditHistory(edit_type="Update", edit_material="Mold", edit_page="Inventory",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_mold'))


@app.route('/mold_description/withdraw/<mold_description_id>', methods=['GET', 'POST'])
def withdraw_mold_description(mold_description_id):
    if request.method == 'POST':
        mold_description_to_withdraw = MoldDescription.query.filter_by(mold_description_id=mold_description_id).first()
        original_mold_type_id = mold_description_to_withdraw.mold_type_id
        original_mold_type = MoldType.query.filter_by(mold_type_id=original_mold_type_id).first()

        new_mold_description = MoldDescription(lot_no=mold_description_to_withdraw.lot_no,
                                               received_date=mold_description_to_withdraw.received_date,
                                               manufacturing_date=mold_description_to_withdraw.manufacturing_date,
                                               expiry_date=mold_description_to_withdraw.expiry_date,
                                               project_leader=mold_description_to_withdraw.project_leader,
                                               incoming_qty=mold_description_to_withdraw.incoming_qty,
                                               withdraw_date=mold_description_to_withdraw.withdraw_date,
                                               withdraw_qty=mold_description_to_withdraw.withdraw_qty,
                                               withdraw_by=mold_description_to_withdraw.withdraw_by,
                                               withdraw_purpose=mold_description_to_withdraw.withdraw_purpose,
                                               balance=mold_description_to_withdraw.balance,
                                               trans_type=mold_description_to_withdraw.trans_type,
                                               release_status=mold_description_to_withdraw.release_status,
                                               expiry_status=mold_description_to_withdraw.expiry_status,
                                               created_time=mold_description_to_withdraw.created_time,
                                               mold_type_id=mold_description_to_withdraw.mold_type_id)

        new_mold_description.withdraw_date = request.form['withdraw_date']
        new_mold_description.withdraw_qty = request.form['withdraw_qty']
        new_mold_description.withdraw_by = request.form['withdraw_by']
        new_mold_description.withdraw_purpose = request.form['withdraw_purpose']
        new_mold_description.incoming_qty = ""
        new_mold_description.balance = ""
        new_mold_description.release_status = ""
        new_mold_description.expiry_status = ""
        new_mold_description.trans_type = "withdrawal"

        mold_description_to_withdraw.balance = \
            float(mold_description_to_withdraw.balance) - float(new_mold_description.withdraw_qty)

        if mold_description_to_withdraw.balance >= 0:
            db.session.add(new_mold_description)
            flash("Mold withdrawal transaction added successfully")

            new_content = '(Mold type)' + original_mold_type.mold_name \
                          + ', (Lot no.)' + new_mold_description.lot_no + ', ' \
                          + new_mold_description.received_date + ', ' \
                          + new_mold_description.withdraw_date + ', ' + new_mold_description.withdraw_qty + ', ' \
                          + new_mold_description.withdraw_by + ', ' + new_mold_description.withdraw_purpose

            new_edit = EditHistory(edit_type="Withdraw", edit_material="Mold",
                                   edit_page="Transaction 2nd page",
                                   old_content="", new_content=new_content, changed_by=current_user.username,
                                   changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_edit)
            db.session.commit()
        else:
            mold_description_to_withdraw.balance = \
                float(mold_description_to_withdraw.balance) + float(new_mold_description.withdraw_qty)
            flash("Withdrawal failed. Balance cannot be negative", category="error")

    return redirect(url_for('show_mold_descriptions', mold_type_id=original_mold_type_id))


@app.route("/mold_description/delete/<mold_description_id>", methods=['GET', 'POST'])
def delete_mold_description(mold_description_id):
    mold_description_to_delete = MoldDescription.query.filter_by(mold_description_id=mold_description_id).first()
    original_mold_type_id = mold_description_to_delete.mold_type.mold_type_id
    original_mold_type = MoldType.query.filter_by(mold_type_id=original_mold_type_id).first()

    if mold_description_to_delete.trans_type == "withdrawal":
        mold_description_to_update = MoldDescription.query.filter_by(
            lot_no=mold_description_to_delete.lot_no, created_time=mold_description_to_delete.created_time,
            trans_type="incoming").first()
        mold_description_to_update.balance = \
            float(mold_description_to_update.balance) + float(mold_description_to_delete.withdraw_qty)

        # edit history
        old_content = '(Mold type)' + original_mold_type.mold_name + ', ' + mold_description_to_delete.lot_no + ', ' \
                      + mold_description_to_delete.received_date + ', ' + mold_description_to_delete.manufacturing_date + ', ' \
                      + mold_description_to_delete.expiry_date + ', ' + mold_description_to_delete.project_leader + ', ' \
                      + mold_description_to_delete.incoming_qty + ', ' + mold_description_to_delete.withdraw_date + ', ' \
                      + mold_description_to_delete.withdraw_qty + ', ' + mold_description_to_delete.withdraw_by \
                      + mold_description_to_delete.withdraw_purpose
        new_edit = EditHistory(edit_type="Delete", edit_material="Mold", edit_page="Transaction 2nd page",
                               old_content=old_content, new_content="", changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)

        db.session.delete(mold_description_to_delete)
        db.session.commit()
        flash("Withdrawal transaction deleted successfully")

    if mold_description_to_delete.trans_type == "incoming":
        mold_description_related = MoldDescription.query.filter_by(
            lot_no=mold_description_to_delete.lot_no, created_time=mold_description_to_delete.created_time).all()
        for m in mold_description_related:
            old_content = '(Mold type)' + original_mold_type.mold_name + ', ' + m.lot_no + ', ' + m.received_date \
                          + ', ' + m.manufacturing_date + ', ' + m.expiry_date + ', ' + m.project_leader + ', ' \
                          + m.incoming_qty + ', ' + m.withdraw_date + ', ' + m.withdraw_qty + ', ' + m.withdraw_by \
                          + ', ' + m.withdraw_purpose + ', ' + m.balance
            new_edit = EditHistory(edit_type="Delete", edit_material="Mold", edit_page="Transaction 2nd page",
                                   old_content=old_content, new_content="", changed_by=current_user.username,
                                   changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_edit)

            db.session.delete(m)
        db.session.commit()
        flash("Incoming transaction and related withdrawal transactions are deleted successfully")

    return redirect(url_for('show_mold_descriptions', mold_type_id=original_mold_type_id))


@app.route("/mold_type/delete/<mold_type_id>", methods=['GET', 'POST'])
def delete_mold_type(mold_type_id):
    mold_type_to_delete = MoldType.query.filter_by(mold_type_id=mold_type_id).first()
    old_content = mold_type_to_delete.mold_name + ', ' + mold_type_to_delete.supplier + ', ' \
                  + mold_type_to_delete.pellet_size + ', ' + mold_type_to_delete.part_no

    new_edit = EditHistory(edit_type="Delete", edit_material="Mold", edit_page="Transaction 1st page",
                           old_content=old_content, new_content="", changed_by=current_user.username,
                           changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(new_edit)
    db.session.commit()

    db.session.delete(mold_type_to_delete)
    db.session.commit()
    flash("Mold description deleted successfully")

    return redirect(url_for('show_mold_types'))
