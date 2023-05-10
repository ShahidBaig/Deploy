from datetime import datetime
from config import app, db
from models import Item, Client

CLIENTS = [
    {
        "id": "test1",
        "companyname": "test1",
        "companyaddress": "Columbus",
    },
    {
        "id": "test2",
        "companyname": "test2",
        "companyaddress": "Columbus",
    },
    {
        "id": "test3",
        "companyname": "test3",
        "companyaddress": "Columbus",
    },
]

ITEMS = [
    {
        "id": "item1",
        "itemname": "item1",
        "description": "this is a test description",
    },
    {
        "id": "item2",
        "itemname": "item2",
        "description": "this is a test description",
    },
    {
        "id": "item3",
        "itemname": "item3",
        "description": "this is a test description",
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for data in CLIENTS:
        new_client = Client(id=data.get("id"), companyname=data.get("companyname"), companyaddress=data.get("companyaddress"))
        db.session.add(new_client)

    for data in ITEMS:
        new_item = Item(id=data.get("id"), itemname=data.get("itemname"), description=data.get("description"))
        db.session.add(new_item)

    db.session.commit()
