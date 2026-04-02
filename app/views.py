from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from werkzeug.utils import secure_filename
import os
from app import app, db
from app.models import Property
from app.forms import PropertyForm

# Add this helper function at the top of your views.py
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods=['GET', 'POST'])
def add_property():
    """Route for displaying the form to add a new property."""
    form = PropertyForm()
    
    # Ensure upload directory exists
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    if form.validate_on_submit():
        # Check if this is a duplicate submission (using session)
        import hashlib
        form_data = f"{form.title.data}{form.location.data}{form.price.data}"
        form_hash = hashlib.md5(form_data.encode()).hexdigest()
        
        if session.get('last_submission') == form_hash:
            flash('This property appears to be a duplicate. Please wait before submitting again.', 'warning')
            return redirect(url_for('display_properties'))
        
        # Handle file upload for the 'photo' field
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        
        # Save the file
        filepath = os.path.join(upload_folder, filename)
        photo.save(filepath)
        
        # Create new property
        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            rooms=form.rooms.data,
            bathrooms=form.bathrooms.data,
            price=form.price.data,
            location=form.location.data,
            property_type=form.prop_type.data,
            photo=filename
        )
        
        try:
            db.session.add(new_property)
            db.session.commit()
            session['last_submission'] = form_hash
            flash('Property was successfully added!', 'success')
            return redirect(url_for('display_properties'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding property: {str(e)}', 'danger')
            return render_template('create_property.html', form=form)
    
    # If form validation fails, display errors
    if request.method == 'POST':
        flash_errors(form)
    
    return render_template('create_property.html', form=form)

@app.route('/properties')
def display_properties():
    """Display a list of all properties in the database."""
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<int:propertyid>')
def view_property(propertyid):
    """View an individual property by specific id."""
    property_item = Property.query.get_or_404(propertyid)
    return render_template('view_property.html', property=property_item)

@app.route('/uploads/<filename>')
def get_image(filename):
    """Helper route to serve uploaded property photos."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404