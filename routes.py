from flask import Blueprint, render_template, redirect, url_for, session, flash
from app import db
from forms import PersonalInfoForm, TravelPreferencesForm, HealthSafetyForm
from models import Applicant

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/stage1', methods=['GET', 'POST'])
def stage1():
    form = PersonalInfoForm()
    if form.validate_on_submit():
        session['personal_info'] = form.data
        return redirect(url_for('main.stage2'))
    return render_template('stage1_personal_info.html', form=form)

@bp.route('/stage2', methods=['GET', 'POST'])
def stage2():
    form = TravelPreferencesForm()
    if form.validate_on_submit():
        if form.back.data:
            return redirect(url_for('main.stage1'))
        session['travel_preferences'] = form.data
        return redirect(url_for('main.stage3'))
    return render_template('stage2_travel_preferences.html', form=form)

@bp.route('/stage3', methods=['GET', 'POST'])
def stage3():
    form = HealthSafetyForm()
    if form.validate_on_submit():
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

        session.clear()  # Clear session after saving
        return redirect(url_for('main.success'))
    return render_template('stage3_health_safety.html', form=form)

@bp.route('/success')
def success():
    return render_template('success.html')


@bp.route('/admin/applications')
def admin_applications():
    applicants = Applicant.query.all()
    return render_template('admin_applications.html', applicants=applicants)
