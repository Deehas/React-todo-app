from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    category = db.Column(db.String, db.ForeignKey("category.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "date": self.date.strftime("%Y-%m-%d") if self.date else None,
            "time": self.time.strftime("%H:%M") if self.time else None,
            "categoryID": self.category,
            "userID": self.user_id,
        }
        return data

    def __repr__(self):
        return "<ToDo {}>".format(self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
        }
        return data

    def __repr__(self):
        return "<Category {}>".format(self.name)
