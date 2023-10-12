from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    #secondary for many to many relationship
    #it will go to secondry to table to find what items here need to mention
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")