from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Optional

class PersonalInfoForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth (YYYY-MM-DD)', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^[0-9\-\+]{9,15}$')])
    next = SubmitField('Next')

class TravelPreferencesForm(FlaskForm):
    departure_date = DateField('Departure Date (YYYY-MM-DD)', validators=[DataRequired()])
    return_date = DateField('Return Date (YYYY-MM-DD)', validators=[DataRequired()])
    accommodation = SelectField('Accommodation Preference', choices=[('space_hotel', 'Space Hotel'), ('martian_base', 'Martian Base')])
    special_requests = TextAreaField('Special Requests or Preferences', validators=[Optional()])
    back = SubmitField('Back')
    next = SubmitField('Next')

class HealthSafetyForm(FlaskForm):
    health_declaration = BooleanField('I declare that I am in good health', validators=[DataRequired()])
    emergency_contact = StringField('Emergency Contact Information', validators=[DataRequired()])
    medical_conditions = TextAreaField('Medical Conditions (if any)', validators=[Optional()])
    back = SubmitField('Back')
    submit = SubmitField('Submit')
