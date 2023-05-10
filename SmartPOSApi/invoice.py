from flask import abort, make_response

from config import db
from models import Invoice, invoice_schema, Client, invoiceall_schema


def read_all(client_id):
    invoice = Invoice.query.filter(Invoice.client_id == client_id)

    if invoice is not None:
        return invoiceall_schema.dump(invoice)
    else:
        abort(404, f"Invoice(s) for Client {client_id} not found")


def create(invoice):
    client_id = invoice.get("client_id")
    existing_client = Client.query.filter(Client.id == client_id).one_or_none()

    if existing_client is None:
        abort(406, f"Invalid Client {client_id}")
    else:
        new_invoice = invoice_schema.load(invoice, session=db.session)
        db.session.add(new_invoice)
        db.session.commit()
        return invoice_schema.dump(new_invoice), 201


def read_one(client_id, invoice_id):
    invoice = Invoice.query.filter(Invoice.client_id == client_id, Invoice.id == invoice_id).one_or_none()

    if invoice is not None:
        return invoice_schema.dump(invoice)
    else:
        abort(404, f"Invoice with id {invoice_id} not found")


def delete(client_id, invoice_id):
    existing_Invoice = Invoice.query.filter(Invoice.client_id == client_id, Invoice.id == invoice_id).one_or_none()

    if existing_Invoice:
        db.session.delete(existing_Invoice)
        db.session.commit()
        return make_response(f"{invoice_id} successfully deleted", 200)
    else:
        abort(404, f"Invoice with id {invoice_id} not found")
