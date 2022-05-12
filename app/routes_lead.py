from app import app, db
from app.models import EditHistory
from app.models_lead import LeadType, LeadDescription

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_required
from datetime import datetime


@app.route("/lead_frame")
@login_required
def show_lead():
    all_lead = db.session.query(LeadType, LeadDescription).join(LeadDescription).all()
    return render_template("lead.html", leads=all_lead)


@app.route("/lead_type")
@login_required
def show_lead_types():
    all_lead_type = LeadType.query.order_by(LeadType.lead_type_id).all()
    return render_template("lead_type.html", lead_types=all_lead_type)


@app.route("/lead_type/<lead_type_id>")
@login_required
def show_lead_descriptions(lead_type_id):
    all_lead_description = LeadDescription.query.filter_by(lead_type_id=lead_type_id). \
        order_by(LeadDescription.received_date.desc(), LeadDescription.created_time.desc(),
                 LeadDescription.withdraw_date).all()

    return render_template("lead_description.html",
                           lead_type=LeadType.query.filter_by(lead_type_id=lead_type_id).first(),
                           lead_descriptions=all_lead_description)


@app.route("/lead_type/insert", methods=['POST'])
def insert_lead_type():
    if request.method == 'POST':
        lead_no = request.form['lead_no']
        supplier = request.form['supplier']
        package_no = request.form['package_no']
        title = request.form['title']

        new_content = lead_no + ', ' + supplier + ', ' + package_no + ', ' + title
        new_lead_type = LeadType(lead_no, supplier, package_no, title)

        db.session.add(new_lead_type)
        db.session.commit()
        flash("Lead Frame type added successfully")

        new_edit = EditHistory(edit_type="Add", edit_material="Lead", edit_page="Transaction 1st page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_lead_types'))


@app.route("/lead_description/insert/<lead_type_id>", methods=['POST'])
def insert_lead_description(lead_type_id):
    original_lead_type = LeadType.query.filter_by(lead_type_id=lead_type_id).first()
    if request.method == 'POST':
        lot_no = request.form['lot_no']
        row_location = request.form['row_location']
        received_date = request.form['received_date']
        manufacturing_date = request.form['manufacturing_date']
        expiry_date = request.form['expiry_date']
        project_leader = request.form['project_leader']
        record_reff = request.form['record_reff']
        invoice_no = request.form['invoice_no']
        purchasing_order = request.form['purchasing_order']
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

        new_content = '(Lead type)' + original_lead_type.lead_no + ', ' + lot_no + ', ' + row_location + ', ' + \
                      received_date + ', ' + manufacturing_date + ', ' + expiry_date + ', ' + project_leader + \
                      ', ' + record_reff + ', ' + invoice_no + ', ' + purchasing_order + ', ' + incoming_qty

        new_lead_description = LeadDescription(lot_no, row_location, received_date, manufacturing_date, expiry_date,
                                               project_leader, record_reff, invoice_no, purchasing_order, incoming_qty,
                                               withdraw_date, withdraw_by, withdraw_qty, withdraw_purpose, balance,
                                               trans_type, release_status, expiry_status, created_time,
                                               lead_type_id=lead_type_id)

        db.session.add(new_lead_description)
        db.session.commit()
        flash("Lead Frame description added successfully")

        new_edit = EditHistory(edit_type="Add", edit_material="Lead", edit_page="Transaction 2nd page",
                               old_content="", new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_lead_descriptions', lead_type_id=lead_type_id))


@app.route('/lead_type/update', methods=['GET', 'POST'])
def update_lead_type():
    if request.method == 'POST':
        lead_type_to_update = LeadType.query.get(request.form.get('lead_type_id'))
        old_content = lead_type_to_update.lead_no + ', ' + lead_type_to_update.supplier + ', ' \
                      + lead_type_to_update.package_no + ', ' + lead_type_to_update.title

        lead_type_to_update.lead_no = request.form['lead_no']
        lead_type_to_update.supplier = request.form['supplier']
        lead_type_to_update.package_no = request.form['package_no']
        lead_type_to_update.title = request.form['title']

        db.session.commit()
        flash("Lead Frame type [" + str(lead_type_to_update.lead_no) + "] is updated successfully")

        new_content = lead_type_to_update.lead_no + ', ' + lead_type_to_update.supplier + ', ' \
                      + lead_type_to_update.package_no + ', ' + lead_type_to_update.title

        new_edit = EditHistory(edit_type="Update", edit_material="Lead", edit_page="Transaction 1st page",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

        return redirect(url_for('show_lead_types'))


@app.route('/lead_description/update/<lead_description_id>', methods=['GET', 'POST'])
def update_lead_description(lead_description_id):
    if request.method == 'POST':
        lead_description_to_update = LeadDescription.query.filter_by(lead_description_id=lead_description_id).first()
        original_lead_type_id = lead_description_to_update.lead_type_id
        original_lead_type = LeadType.query.filter_by(lead_type_id=original_lead_type_id).first()

        old_content = '(Lead type)' + original_lead_type.lead_no + ', ' + lead_description_to_update.lot_no + ', ' \
                      + lead_description_to_update.row_location + ', ' + lead_description_to_update.received_date + ', ' \
                      + lead_description_to_update.manufacturing_date + ', ' + lead_description_to_update.expiry_date + ', ' \
                      + lead_description_to_update.project_leader + ', ' + lead_description_to_update.record_reff + ', ' \
                      + lead_description_to_update.invoice_no + ', ' + lead_description_to_update.purchasing_order + ', ' \
                      + lead_description_to_update.incoming_qty

        lead_description_to_update.lot_no = request.form['lot_no']
        lead_description_to_update.row_location = request.form['row_location']
        lead_description_to_update.received_date = request.form['received_date']
        lead_description_to_update.manufacturing_date = request.form['manufacturing_date']
        lead_description_to_update.expiry_date = request.form['expiry_date']
        lead_description_to_update.project_leader = request.form['project_leader']
        lead_description_to_update.record_reff = request.form['record_reff']
        lead_description_to_update.invoice_no = request.form['invoice_no']
        lead_description_to_update.purchasing_order = request.form['purchasing_order']
        lead_description_to_update.incoming_qty = request.form['incoming_qty']
        lead_description_to_update.balance = lead_description_to_update.incoming_qty

        db.session.commit()
        flash("Lead Frame description for lot no. [" + str(
            lead_description_to_update.lot_no) + "] is updated successfully")

        new_content = '(Lead type)' + original_lead_type.lead_no + ', ' + lead_description_to_update.lot_no + ', ' \
                      + lead_description_to_update.row_location + ', ' + lead_description_to_update.received_date + ', ' \
                      + lead_description_to_update.manufacturing_date + ', ' + lead_description_to_update.expiry_date + ', ' \
                      + lead_description_to_update.project_leader + ', ' + lead_description_to_update.record_reff + ', ' \
                      + lead_description_to_update.invoice_no + ', ' + lead_description_to_update.purchasing_order + \
                      ', ' + lead_description_to_update.incoming_qty

        new_edit = EditHistory(edit_type="Update", edit_material="Lead", edit_page="Transaction 2nd page",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_lead_descriptions', lead_type_id=original_lead_type_id))


@app.route('/lead_inventory/update/<lead_description_id>', methods=['GET', 'POST'])
def update_lead_inventory(lead_description_id):
    if request.method == 'POST':
        lead_to_update = LeadDescription.query.filter_by(lead_description_id=lead_description_id).first()
        original_lead_type_id = lead_to_update.lead_type_id
        original_lead_type = LeadType.query.filter_by(lead_type_id=original_lead_type_id).first()

        old_content = '(Lead type)' + original_lead_type.lead_no + ', (lot no.)' + lead_to_update.lot_no + ', (row location)' \
                      + lead_to_update.row_location + ', ' + lead_to_update.balance + ', ' \
                      + lead_to_update.release_status

        lead_to_update.balance = request.form['balance']
        lead_to_update.release_status = request.form['release_status']

        db.session.commit()
        flash("Lead Frame information for lead frame type [" + str(original_lead_type.lead_no) + "] and lot no. [" +
              str(lead_to_update.lot_no) + "] is updated successfully")

        new_content = '(Lead type)' + original_lead_type.lead_no + ', (lot no.)' + lead_to_update.lot_no + ', (row location)' \
                      + lead_to_update.row_location + ', ' + lead_to_update.balance + ', ' + lead_to_update.release_status

        new_edit = EditHistory(edit_type="Update", edit_material="Lead", edit_page="Inventory",
                               old_content=old_content, new_content=new_content, changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)
        db.session.commit()

    return redirect(url_for('show_lead'))


@app.route('/lead_description/withdraw/<lead_description_id>', methods=['GET', 'POST'])
def withdraw_lead_description(lead_description_id):
    if request.method == 'POST':
        lead_description_to_withdraw = LeadDescription.query.filter_by(lead_description_id=lead_description_id).first()
        original_lead_type_id = lead_description_to_withdraw.lead_type_id
        original_lead_type = LeadType.query.filter_by(lead_type_id=original_lead_type_id).first()

        new_lead_description = LeadDescription(lot_no=lead_description_to_withdraw.lot_no,
                                               row_location=lead_description_to_withdraw.row_location,
                                               received_date=lead_description_to_withdraw.received_date,
                                               manufacturing_date=lead_description_to_withdraw.manufacturing_date,
                                               expiry_date=lead_description_to_withdraw.expiry_date,
                                               project_leader=lead_description_to_withdraw.project_leader,
                                               record_reff=lead_description_to_withdraw.record_reff,
                                               invoice_no=lead_description_to_withdraw.invoice_no,
                                               purchasing_order=lead_description_to_withdraw.purchasing_order,
                                               incoming_qty=lead_description_to_withdraw.incoming_qty,
                                               withdraw_date=lead_description_to_withdraw.withdraw_date,
                                               withdraw_qty=lead_description_to_withdraw.withdraw_qty,
                                               withdraw_by=lead_description_to_withdraw.withdraw_by,
                                               withdraw_purpose=lead_description_to_withdraw.withdraw_purpose,
                                               balance=lead_description_to_withdraw.balance,
                                               trans_type=lead_description_to_withdraw.trans_type,
                                               release_status=lead_description_to_withdraw.release_status,
                                               expiry_status=lead_description_to_withdraw.expiry_status,
                                               created_time=lead_description_to_withdraw.created_time,
                                               lead_type_id=lead_description_to_withdraw.lead_type_id)

        new_lead_description.withdraw_date = request.form['withdraw_date']
        new_lead_description.withdraw_qty = request.form['withdraw_qty']
        new_lead_description.withdraw_by = request.form['withdraw_by']
        new_lead_description.withdraw_purpose = request.form['withdraw_purpose']
        new_lead_description.incoming_qty = ""
        new_lead_description.balance = ""
        new_lead_description.release_status = ""
        new_lead_description.expiry_status = ""
        new_lead_description.trans_type = "withdrawal"

        lead_description_to_withdraw.balance = \
            int(lead_description_to_withdraw.balance) - int(new_lead_description.withdraw_qty)

        if lead_description_to_withdraw.balance >= 0:
            db.session.add(new_lead_description)
            db.session.commit()
            flash("Lead Frame withdrawal transaction added successfully")

            new_content = '(Lead no.)' + original_lead_type.lead_no \
                          + ', (Lot no.)' + new_lead_description.lot_no + ', ' \
                          + new_lead_description.withdraw_date + ', ' \
                          + new_lead_description.withdraw_qty + ', ' + new_lead_description.withdraw_by + ', ' \
                          + new_lead_description.withdraw_purpose

            new_edit = EditHistory(edit_type="Withdraw", edit_material="Lead",
                                   edit_page="Transaction 2nd page",
                                   old_content="", new_content=new_content, changed_by=current_user.username,
                                   changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_edit)
            db.session.commit()
        else:
            lead_description_to_withdraw.balance = \
                int(lead_description_to_withdraw.balance) + int(new_lead_description.withdraw_qty)
            flash("Withdrawal failed. Balance cannot be negative", category="error")

    return redirect(url_for('show_lead_descriptions', lead_type_id=original_lead_type_id))


@app.route("/lead_description/delete/<lead_description_id>", methods=['GET', 'POST'])
def delete_lead_description(lead_description_id):
    lead_description_to_delete = LeadDescription.query.filter_by(lead_description_id=lead_description_id).first()
    original_lead_type_id = lead_description_to_delete.lead_type.lead_type_id
    original_lead_type = LeadType.query.filter_by(lead_type_id=original_lead_type_id).first()

    if lead_description_to_delete.trans_type == "withdrawal":
        lead_description_to_update = LeadDescription.query.filter_by(
            lot_no=lead_description_to_delete.lot_no, created_time=lead_description_to_delete.created_time,
            trans_type="incoming").first()
        lead_description_to_update.balance = \
            int(lead_description_to_update.balance) + int(lead_description_to_delete.withdraw_qty)

        # edit history
        old_content = '(Lead type)' + original_lead_type.lead_no + ', ' + lead_description_to_delete.lot_no + ', ' \
                      + lead_description_to_delete.row_location + ', ' + lead_description_to_delete.received_date + ', ' \
                      + lead_description_to_delete.manufacturing_date + ', ' + lead_description_to_delete.expiry_date + ', ' \
                      + lead_description_to_delete.project_leader + lead_description_to_delete.record_reff + ', ' \
                      + lead_description_to_delete.invoice_no + ', ' + lead_description_to_delete.purchasing_order + ', ' \
                      + lead_description_to_delete.incoming_qty + ', ' + lead_description_to_delete.withdraw_date + ', ' \
                      + lead_description_to_delete.withdraw_qty + ', ' + lead_description_to_delete.withdraw_by + ', ' \
                      + lead_description_to_delete.withdraw_purpose
        new_edit = EditHistory(edit_type="Delete", edit_material="Lead", edit_page="Transaction 2nd page",
                               old_content=old_content, new_content="", changed_by=current_user.username,
                               changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(new_edit)

        db.session.delete(lead_description_to_delete)
        db.session.commit()
        flash("Withdrawal transaction deleted successfully")

    if lead_description_to_delete.trans_type == "incoming":
        lead_description_related = LeadDescription.query.filter_by(
            lot_no=lead_description_to_delete.lot_no, created_time=lead_description_to_delete.created_time).all()
        for l in lead_description_related:
            old_content = '(Lead type)' + original_lead_type.lead_no + ', ' + l.lot_no + ', ' + l.row_location + \
                          ', ' + l.received_date + ', ' + l.manufacturing_date + ', ' + l.expiry_date + ', ' + \
                          l.project_leader + ', ' + l.record_reff + ', ' + l.invoice_no + ', ' + l.purchasing_order + \
                          ', ' + l.incoming_qty + ', ' + l.withdraw_date + ', ' + l.withdraw_qty + ', ' + \
                          l.withdraw_by + ', ' + l.withdraw_purpose + ', ' + l.balance
            new_edit = EditHistory(edit_type="Delete", edit_material="Lead", edit_page="Transaction 2nd page",
                                   old_content=old_content, new_content="", changed_by=current_user.username,
                                   changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_edit)

            db.session.delete(l)
        db.session.commit()
        flash("Incoming transaction and related withdrawal transactions are deleted successfully")

    return redirect(url_for('show_lead_descriptions', lead_type_id=original_lead_type_id))


@app.route("/lead_type/delete/<lead_type_id>", methods=['GET', 'POST'])
def delete_lead_type(lead_type_id):
    lead_type_to_delete = LeadType.query.filter_by(lead_type_id=lead_type_id).first()
    old_content = lead_type_to_delete.lead_no + ', ' + lead_type_to_delete.supplier + ', ' + \
                  lead_type_to_delete.package_no + ', ' + lead_type_to_delete.title

    new_edit = EditHistory(edit_type="Delete", edit_material="Lead", edit_page="Transaction 1st page",
                           old_content=old_content, new_content="", changed_by=current_user.username,
                           changed_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.session.add(new_edit)
    db.session.commit()

    db.session.delete(lead_type_to_delete)
    db.session.commit()
    flash("Lead Frame description deleted successfully")

    return redirect(url_for('show_lead_types'))
