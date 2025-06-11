from app import db
    
class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    content = db.Column(db.Text)

    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content

    def __repr__(self):
        return "<Post %r>" % self.id