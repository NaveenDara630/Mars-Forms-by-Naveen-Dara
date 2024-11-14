from app import db

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    departure_date = db.Column(db.String(10), nullable=False)
    return_date = db.Column(db.String(10), nullable=False)
    accommodation = db.Column(db.String(50), nullable=False)
    special_requests = db.Column(db.Text)
    health_declaration = db.Column(db.Boolean, nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=False)
    medical_conditions = db.Column(db.Text)

    def __repr__(self):
        return f'<Applicant {self.full_name}>'
