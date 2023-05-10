from datetime import datetime
from marshmallow_sqlalchemy import fields
from config import db, ma


class Client(db.Model):
    __tablename__ = "Client"
    id = db.Column(db.String(25), primary_key=True)
    companyname = db.Column(db.String(50))
    companyaddress = db.Column(db.String(250))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
        sqla_session = db.session


class Item(db.Model):
    __tablename__ = "Item"
    id = db.Column(db.String(25), primary_key=True)
    itemname = db.Column(db.String(50))
    description = db.Column(db.String(250))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        sqla_session = db.session


class InvoiceDetail(db.Model):
    __tablename__ = "InvoiceDetail"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("Invoice.id"), nullable=False)
    item_id = db.Column(db.String(25), db.ForeignKey("Item.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    taxrate = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class InvoiceDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InvoiceDetail
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Invoice(db.Model):
    __tablename__ = "Invoice"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(25), db.ForeignKey("Client.id"))
    customername = db.Column(db.String(50), nullable=False)
    customeraddress = db.Column(db.String(250), nullable=True)
    totalqty = db.Column(db.Integer, nullable=False)
    totalamount = db.Column(db.Float, nullable=False)
    totaltax = db.Column(db.Float, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    invoicedetails = db.relationship(
        InvoiceDetail,
        backref="Invoice",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(InvoiceDetail.timestamp)",
    )


class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True

    InvoiceDetails = fields.Nested(InvoiceDetailSchema, many=True)

client_schema = ClientSchema()
item_schema = ItemSchema()
invoicedetail_schema = InvoiceDetailSchema()
invoicedetailall_schema = InvoiceDetailSchema(many=True)
invoice_schema = InvoiceSchema()
invoiceall_schema = InvoiceSchema(many=True)