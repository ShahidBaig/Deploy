from flask import abort, make_response

from config import db
from models import InvoiceDetail, Invoice, invoicedetail_schema, invoicedetailall_schema


def read_one(invoicedetail_id):
    invoicedetail = InvoiceDetail.query.get(invoicedetail_id)

    if invoicedetail is not None:
        return invoicedetail_schema.dump(invoicedetail)
    else:
        abort(404, f"Invoice Detail with ID {invoicedetail_id} not found")


def read_all(invoice_id):
    invoicedetail = InvoiceDetail.query.filter(InvoiceDetail.invoice_id == invoice_id)

    if invoicedetail is not None:
        return invoicedetailall_schema.dump(invoicedetail)
    else:
        abort(404, f"Invoice Detail for Invoice {invoice_id} not found")


def delete(invoicedetail_id):
    existing_invoicedetail = InvoiceDetail.query.get(invoicedetail_id)

    if existing_invoicedetail:
        invoice_id = existing_invoicedetail.invoice_id
        invoice = Invoice.query.get(invoice_id)

        if invoice:
            invoice.totalqty = invoice.totalqty - existing_invoicedetail.qty
            invoice.totalamount = invoice.totalamount - existing_invoicedetail.amount
            invoice.totaltax = invoice.totaltax - (existing_invoicedetail.amount * ( existing_invoicedetail.taxrate/100))

            db.session.merge(invoice)
            db.session.delete(existing_invoicedetail)
            db.session.commit()
            return make_response(f"{invoicedetail_id} successfully deleted", 204)
        else:
            abort(404, f"Invoice not found for ID: {invoice_id}")
    else:
        abort(404, f"Invoice Detail with ID {invoicedetail_id} not found")


def create(invoicedetail):
    invoice_id = invoicedetail.get("invoice_id")
    amount = invoicedetail.get("amount")
    taxrate = invoicedetail.get("taxrate")
    invoice = Invoice.query.get(invoice_id)

    if invoice:
        new_invoicedetail = invoicedetail_schema.load(invoicedetail, session=db.session)
        invoice.invoicedetails.append(new_invoicedetail)
        invoice.totalqty = invoice.totalqty + invoicedetail.get("qty")
        invoice.totalamount = invoice.totalamount + amount
        invoice.totaltax = invoice.totaltax + (amount * (taxrate/100))

        db.session.merge(invoice)
        db.session.commit()
        return invoicedetail_schema.dump(new_invoicedetail), 201
    else:
        abort(404, f"Invoice not found for ID: {invoice_id}")
