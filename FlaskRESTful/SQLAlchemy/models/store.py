from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    items = db.relationship('ItemModel', lazy='dynamic')  # using lazy='dynamic' cuz, if many items it should not create many objects of items in DB

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}  # using .all() cuz, lazy is dynamic (like a query builder)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()   #SELECT * FROM items WHERE name=name LIMIT 1;

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
