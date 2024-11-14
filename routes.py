from flask import Blueprint, render_template, redirect, url_for, session, flash
from app import db
from forms import PersonalInfoForm, TravelPreferencesForm, HealthSafetyForm
from models import Applicant

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# Stage 1 - Personal Information
@bp.route('/stage1', methods=['GET', 'POST'])
def stage1():
    form = PersonalInfoForm()

    if form.validate_on_submit():
        # Store the personal information in session
        session['personal_info'] = {
            'full_name': form.full_name.data,
            'date_of_birth': form.date_of_birth.data,
            'nationality': form.nationality.data,
            'email': form.email.data,
            'phone': form.phone.data
        }
        return redirect(url_for('main.stage2'))

    return render_template('stage1_personal_info.html', form=form)

# Stage 2 - Travel Preferences
@bp.route('/stage2', methods=['GET', 'POST'])
def stage2():
    form = TravelPreferencesForm()

    if form.validate_on_submit():
        # Store the travel preferences in session
        session['travel_preferences'] = {
            'departure_date': form.departure_date.data,
            'return_date': form.return_date.data,
            'accommodation': form.accommodation.data,
            'special_requests': form.special_requests.data
        }
        return redirect(url_for('main.stage3'))

    return render_template('stage2_travel_preferences.html', form=form)

# Stage 3 - Health and Safety
@bp.route('/stage3', methods=['GET', 'POST'])
def stage3():
    form = HealthSafetyForm()

    # Populate form with previous stage data from session
    if 'personal_info' in session:
        form.full_name.data = session['personal_info'].get('full_name', '')
        form.date_of_birth.data = session['personal_info'].get('date_of_birth', '')
        form.nationality.data = session['personal_info'].get('nationality', '')
        form.email.data = session['personal_info'].get('email', '')
        form.phone.data = session['personal_info'].get('phone', '')
    
    if 'travel_preferences' in session:
        form.departure_date.data = session['travel_preferences'].get('departure_date', '')
        form.return_date.data = session['travel_preferences'].get('return_date', '')
        form.accommodation.data = session['travel_preferences'].get('accommodation', '')
        form.special_requests.data = session['travel_preferences'].get('special_requests', '')

    if form.validate_on_submit():
        # If the user clicks 'Back' to go back to stage 2
        if form.back.data:
            return redirect(url_for('main.stage2'))
        
        # Combine all data from session and current form
        data = {**session['personal_info'], **session['travel_preferences'], **form.data}

        # Create an Applicant instance and save to the database
        applicant = Applicant(
            full_name=data['full_name'],
            date_of_birth=str(data['date_of_birth']),
            nationality=data['nationality'],
            email=data['email'],
            phone=data['phone'],
            departure_date=str(data['departure_date']),
            return_date=str(data['return_date']),
            accommodation=data['accommodation'],
            special_requests=data.get('special_requests', ''),
            health_declaration=data['health_declaration'],
            emergency_contact=data['emergency_contact'],
            medical_conditions=data.get('medical_conditions', '')
        )
        db.session.add(applicant)
        db.session.commit()

        # Clear session after saving
        session.clear()
        
        # Redirect to success page
        return redirect(url_for('main.success'))

    return render_template('stage3_health_safety.html', form=form)

@bp.route('/success')
def success():
    return render_template('success.html')


@bp.route('/admin/applications')
def admin_applications():
    applicants = Applicant.query.all()
    return render_template('admin_applications.html', applicants=applicants)
