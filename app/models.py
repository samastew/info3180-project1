from app import db

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Numeric(12, 2), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    property_type = db.Column(db.String(20), nullable=False)  # House or Apartment
    photo = db.Column(db.String(255), nullable=False)
    
    def __init__(self, title, description, rooms, bathrooms, price, location, property_type, photo):
        self.title = title
        self.description = description
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.price = price
        self.location = location
        self.property_type = property_type
        self.photo = photo
    
    def to_dict(self):
        """Convert property object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'rooms': self.rooms,
            'bathrooms': float(self.bathrooms),
            'price': float(self.price),
            'location': self.location,
            'property_type': self.property_type,
            'photo': self.photo
        }