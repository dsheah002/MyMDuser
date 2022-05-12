from app import app, db
from app.models import EditHistory
from app.models_wafer import WaferType, WaferDescription

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_required
from datetime import datetime


@app.route("/wafer")
@login_required
def show_wafer():
    all_wafer = db.session.query(WaferType, WaferDescription).join(WaferDescription).all()
    return render_template("wafer.html", wafers=all_wafer)


@app.route("/wafer_type")
@login_required
def show_wafer_types():
    all_wafer_type = WaferType.query.order_by(WaferType.wafer_type_id).all()
    return render_template("wafer_type.html", wafer_types=all_wafer_type)


@app.route("/wafer_type/<wafer_type_id>")
@login_required
def show_wafer_descriptions(wafer_type_id):
    all_wafer_description = WaferDescription.query.filter_by(wafer_type_id=wafer_type_id). \
        order_by(WaferDescription.slice_no, WaferDescription.wafer_description_id).all()

    return render_template("wafer_description.html",
                           wafer_type=WaferType.query.filter_by(wafer_type_id=wafer_type_id).first(),
                           wafer_descriptions=all_wafer_description)


@app.route("/wafer_type/insert", methods=['POST'])
def insert_wafer_type():
    if request.method == 'POST':
        wafer_device = request.form['wafer_device']
        wafer_charge = request.form['wafer_charge']

        new_content = wafer_device + ', ' + wafer_charge
        new_wafer_type = WaferType(wafer_device, wafer_charge)

        db.session.add(new_wafer_type)
        db.session.commit()
        flash("Wafer type added successfully")

        new_edit = EditHistory(edit_type="Add", edit_material="Wafer", edit_page="Transaction 1st page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_wafer_types'))


@app.route("/wafer_description/insert/<wafer_type_id>", methods=['POST'])
def insert_wafer_description(wafer_type_id):
    original_wafer_type = WaferType.query.filter_by(wafer_type_id=wafer_type_id).first()
    if request.method == 'POST':
        storage_location = request.form['storage_location']
        received_date = request.form['received_date']
        project_leader = request.form['project_leader']
        incoming_qty = request.form['incoming_qty']
        slice_no = ""
        withdraw_date = ""
        withdraw_by = ""
        withdraw_purpose = ""
        balance = incoming_qty
        trans_type = "incoming"
        release_status = ""
        created_time = datetime.now()

        new_content = '(Wafer device)' + original_wafer_type.wafer_device + ', ' + \
                      '(Wafer charge)' + original_wafer_type.wafer_charge + ', ' + storage_location + ', ' + \
                      received_date + ', ' + project_leader + ', ' + incoming_qty

        new_wafer_description = WaferDescription(storage_location, received_date, project_leader, incoming_qty,
                                                 slice_no, withdraw_date, withdraw_by, withdraw_purpose, balance,
                                                 trans_type, release_status, created_time,
                                                 wafer_type_id=wafer_type_id)
        db.session.add(new_wafer_description)

        for i in range(int(incoming_qty)):
            new_wafer_description_child = WaferDescription(storage_location, received_date, project_leader,
                                                           incoming_qty, slice_no, withdraw_date, withdraw_by,
                                                           withdraw_purpose, balance, trans_type, release_status,
                                                           created_time, wafer_type_id=wafer_type_id)
            new_wafer_description_child.incoming_qty = 1
            new_wafer_description_child.slice_no = "to be updated"
            new_wafer_description_child.balance = 1
            new_wafer_description_child.trans_type = "available"
            db.session.add(new_wafer_description_child)

        db.session.commit()
        flash("Wafer description added successfully")

        new_edit = EditHistory(edit_type="Add", edit_material="Wafer", edit_page="Transaction 2nd page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_wafer_descriptions', wafer_type_id=wafer_type_id))


@app.route('/wafer_type/update', methods=['GET', 'POST'])
def update_wafer_type():
    if request.method == 'POST':
        wafer_type_to_update = WaferType.query.get(request.form.get('wafer_type_id'))
        old_content = wafer_type_to_update.wafer_device + ', ' + wafer_type_to_update.wafer_charge

        wafer_type_to_update.wafer_device = request.form['wafer_device']
        wafer_type_to_update.wafer_charge = request.form['wafer_charge']

        db.session.commit()
        flash("Wafer device [" + str(wafer_type_to_update.wafer_device) + "] and wafer charge ["
              + str(wafer_type_to_update.wafer_charge) + "] is updated successfully")

        new_content = wafer_type_to_update.wafer_device + ', ' + wafer_type_to_update.wafer_charge

        new_edit = EditHistory(edit_type="Update", edit_material="Wafer", edit_page="Transaction 1st page",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

        return redirect(url_for('show_wafer_types'))


@app.route('/wafer_description/update/<wafer_description_id>', methods=['GET', 'POST'])
def update_wafer_description(wafer_description_id):
    if request.method == 'POST':
        wafer_description_to_update = WaferDescription.query. \
            filter_by(wafer_description_id=wafer_description_id).first()
        original_wafer_type_id = wafer_description_to_update.wafer_type_id
        original_wafer_type = WaferType.query.filter_by(wafer_type_id=original_wafer_type_id).first()

        old_content = '(Wafer device)' + original_wafer_type.wafer_device + ', ' + \
                      '(Wafer charge)' + original_wafer_type.wafer_charge + ', ' + \
                      '(Slice no.)' + wafer_description_to_update.slice_no

        wafer_description_to_update.slice_no = request.form['slice_no']
        flash("Wafer slice no. [" + str(wafer_description_to_update.slice_no) + "] is updated successfully")

        new_content = '(Wafer device)' + original_wafer_type.wafer_device \
                      + ', (Wafer charge)' + original_wafer_type.wafer_charge \
                      + ', (Slice no.)' + wafer_description_to_update.slice_no

        new_edit = EditHistory(edit_type="Update", edit_material="Wafer", edit_page="Transaction 2nd page",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_wafer_descriptions', wafer_type_id=original_wafer_type_id))


@app.route('/wafer_inventory/update/<wafer_description_id>', methods=['GET', 'POST'])
def update_wafer_inventory(wafer_description_id):
    if request.method == 'POST':
        wafer_to_update = WaferDescription.query.filter_by(wafer_description_id=wafer_description_id).first()
        original_wafer_type_id = wafer_to_update.wafer_type_id
        original_wafer_type = WaferType.query.filter_by(wafer_type_id=original_wafer_type_id).first()

        old_content = '(Wafer device)' + original_wafer_type.wafer_device \
                      + ', (Wafer charge)' + original_wafer_type.wafer_charge + ', ' \
                      + wafer_to_update.balance + ', ' + wafer_to_update.release_status

        wafer_to_update.balance = request.form['balance']
        wafer_to_update.release_status = request.form['release_status']

        db.session.commit()
        flash("Wafer information for wafer device [" + str(original_wafer_type.wafer_device) + "] and wafer charge [" +
              str(original_wafer_type.wafer_charge) + "] is updated successfully")

        new_content = '(Wafer device)' + original_wafer_type.wafer_device \
                      + ', (Wafer charge)' + original_wafer_type.wafer_charge + ', ' \
                      + wafer_to_update.balance + ', ' + wafer_to_update.release_status
        new_edit = EditHistory(edit_type="Update", edit_material="Wafer", edit_page="Inventory",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_wafer'))


@app.route('/wafer_description/withdraw/<wafer_description_id>', methods=['GET', 'POST'])
def withdraw_wafer_description(wafer_description_id):
    if request.method == 'POST':
        wafer_description_to_withdraw = WaferDescription.query. \
            filter_by(wafer_description_id=wafer_description_id).first()
        original_wafer_type_id = wafer_description_to_withdraw.wafer_type_id
        original_wafer_type = WaferType.query.filter_by(wafer_type_id=original_wafer_type_id).first()

        new_wafer_description = WaferDescription(storage_location=wafer_description_to_withdraw.storage_location,
                                                 received_date=wafer_description_to_withdraw.received_date,
                                                 project_leader=wafer_description_to_withdraw.project_leader,
                                                 incoming_qty=wafer_description_to_withdraw.incoming_qty,
                                                 slice_no=wafer_description_to_withdraw.slice_no,
                                                 withdraw_date=wafer_description_to_withdraw.withdraw_date,
                                                 withdraw_by=wafer_description_to_withdraw.withdraw_by,
                                                 withdraw_purpose=wafer_description_to_withdraw.withdraw_purpose,
                                                 balance=wafer_description_to_withdraw.balance,
                                                 trans_type=wafer_description_to_withdraw.trans_type,
                                                 release_status=wafer_description_to_withdraw.release_status,
                                                 created_time=wafer_description_to_withdraw.created_time,
                                                 wafer_type_id=wafer_description_to_withdraw.wafer_type_id)

        new_wafer_description.withdraw_date = request.form['withdraw_date']
        new_wafer_description.withdraw_by = request.form['withdraw_by']
        new_wafer_description.withdraw_purpose = request.form['withdraw_purpose']
        new_wafer_description.trans_type = request.form['trans_type']

        # update parent row balance: - 1 for withdrawal transaction, + 1 for returning transaction
        wafer_description_to_update_parent = WaferDescription.query.filter_by(
            trans_type="incoming", created_time=new_wafer_description.created_time).first()
        if new_wafer_description.trans_type == "withdrawal":
            wafer_description_to_withdraw.balance = 0
            wafer_description_to_withdraw.trans_type = "not available"
            wafer_description_to_update_parent.balance = \
                int(wafer_description_to_update_parent.balance) - 1
        else:
            wafer_description_to_withdraw.balance = 1
            wafer_description_to_withdraw.trans_type = "available"
            wafer_description_to_update_parent.balance = \
                int(wafer_description_to_update_parent.balance) + int(wafer_description_to_withdraw.balance) \
                - int(new_wafer_description.balance)

        new_wafer_description.balance = ""
        db.session.add(new_wafer_description)
        flash("Wafer transaction added successfully")

        new_content = '(Wafer device)' + original_wafer_type.wafer_device \
                      + ', (Wafer charge)' + original_wafer_type.wafer_charge + ', ' \
                      + new_wafer_description.withdraw_date + ', ' \
                      + new_wafer_description.withdraw_by + ', ' \
                      + new_wafer_description.withdraw_purpose

        new_edit = EditHistory(edit_type=new_wafer_description.trans_type.capitalize(), edit_material="Wafer",
                               edit_page="Transaction 2nd page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_wafer_descriptions', wafer_type_id=original_wafer_type_id))


@app.route("/wafer_description/delete/<wafer_description_id>", methods=['GET', 'POST'])
def delete_wafer_description(wafer_description_id):
    wafer_description_to_delete = WaferDescription.query.filter_by(wafer_description_id=wafer_description_id).first()
    original_wafer_type_id = wafer_description_to_delete.wafer_type.wafer_type_id
    original_wafer_type = WaferType.query.filter_by(wafer_type_id=original_wafer_type_id).first()

    # update parent row balance: + 1 for deleting withdrawal transaction,
    # - 1 for returning transaction if the row before is withdrawal transaction
    if wafer_description_to_delete.trans_type == "withdrawal" or \
            wafer_description_to_delete.trans_type == "returning partial" or \
            wafer_description_to_delete.trans_type == "returning full":
        wafer_description_to_update_parent = WaferDescription.query.filter_by(
            trans_type="incoming", created_time=wafer_description_to_delete.created_time).first()
        wafer_description_to_update = WaferDescription.query.\
            filter_by(slice_no=wafer_description_to_delete.slice_no,
                      created_time=wafer_description_to_delete.created_time).\
            order_by(WaferDescription.wafer_description_id).first()
        if wafer_description_to_delete.trans_type == "withdrawal":
            wafer_description_to_update.balance = 1
            wafer_description_to_update.trans_type = "available"
            wafer_description_to_update_parent.balance = int(wafer_description_to_update_parent.balance) + 1
        else:
            # find the 2nd last row of the same slice no. to check
            wafer_description_to_check = WaferDescription.query.\
                filter_by(slice_no=wafer_description_to_delete.slice_no,
                          created_time=wafer_description_to_delete.created_time).\
                order_by(WaferDescription.wafer_description_id.desc()).offset(1).first()
            if wafer_description_to_check.trans_type == "withdrawal":
                wafer_description_to_update.balance = 0
                wafer_description_to_update.trans_type = "not available"
                wafer_description_to_update_parent.balance = int(wafer_description_to_update_parent.balance) - 1

        # edit history
        old_content = '(Wafer device)' + original_wafer_type.wafer_device \
                      + ', (Wafer charge)' + original_wafer_type.wafer_charge \
                      + ', (Slice no.)' + wafer_description_to_delete.slice_no + ', ' \
                      + wafer_description_to_delete.withdraw_date \
                      + ', ' + wafer_description_to_delete.withdraw_by + ', ' \
                      + wafer_description_to_delete.withdraw_purpose + ', ' + wafer_description_to_delete.trans_type
        new_edit = EditHistory(edit_type="Delete child row", edit_material="Wafer", edit_page="Transaction 2nd page",
                               old_content=old_content, new_content="", changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)

        db.session.delete(wafer_description_to_delete)
        db.session.commit()
        flash("Transaction deleted successfully")

    if wafer_description_to_delete.trans_type == "available" or \
            wafer_description_to_delete.trans_type == "not available":
        wafer_description_related = WaferDescription.query.\
            filter_by(slice_no=wafer_description_to_delete.slice_no,
                      created_time=wafer_description_to_delete.created_time).all()
        for w in wafer_description_related:
            old_content = '(Wafer device)' + original_wafer_type.wafer_device \
                          + ', (Wafer charge)' + original_wafer_type.wafer_charge + ', ' \
                          + ', (Slice no.)' + w.slice_no + w.withdraw_date + ', ' + w.withdraw_by \
                          + ', ' + w.withdraw_purpose + ', ' + w.trans_type
            new_edit = EditHistory(edit_type="Delete child rows", edit_material="Wafer",
                                   edit_page="Transaction 2nd page", old_content=old_content, new_content="",
                                   changed_by=current_user.username,
                                   changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_edit)
            db.session.delete(w)
        db.session.commit()
        flash("Wafer slice no. [" + wafer_description_to_delete.slice_no
              + "] and related transactions are deleted successfully")

    if wafer_description_to_delete.trans_type == "incoming":
        wafer_description_related = WaferDescription.query. \
            filter_by(created_time=wafer_description_to_delete.created_time).all()
        for w in wafer_description_related:
            old_content = '(Wafer device)' + original_wafer_type.wafer_device \
                          + ', (Wafer charge)' + original_wafer_type.wafer_charge + ', ' \
                          + w.storage_location + ', ' + w.received_date + ', ' + w.project_leader + ', ' \
                          + w.incoming_qty + ', (Slice no.)' + w.slice_no + w.withdraw_date + ', ' + w.withdraw_by \
                          + ', ' + w.withdraw_purpose + ', ' + w.trans_type
            new_edit = EditHistory(edit_type="Delete", edit_material="Wafer",
                                   edit_page="Transaction 2nd page", old_content=old_content, new_content="",
                                   changed_by=current_user.username,
                                   changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_edit)
            db.session.delete(w)
        db.session.commit()
        flash("Wafer transactions deleted successfully")

    return redirect(url_for('show_wafer_descriptions', wafer_type_id=original_wafer_type_id))


@app.route("/wafer_type/delete/<wafer_type_id>", methods=['GET', 'POST'])
def delete_wafer_type(wafer_type_id):
    wafer_type_to_delete = WaferType.query.filter_by(wafer_type_id=wafer_type_id).first()
    old_content = wafer_type_to_delete.wafer_device + ', ' + wafer_type_to_delete.wafer_charge

    new_edit = EditHistory(edit_type="Delete", edit_material="Wafer", edit_page="Transaction 1st page",
                           old_content=old_content, new_content="", changed_by=current_user.username,
                           changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(new_edit)

    db.session.delete(wafer_type_to_delete)
    db.session.commit()
    flash("Wafer description deleted successfully")

    return redirect(url_for('show_wafer_types'))
