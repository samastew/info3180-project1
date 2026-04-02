from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired, DataRequired, NumberRange

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired(message="Title is required")])
    description = TextAreaField('Description', validators=[DataRequired(message="Description is required")])
    rooms = IntegerField('No. of Bedrooms', validators=[
        DataRequired(message="Number of bedrooms is required"),
        NumberRange(min=1, message="Must have at least 1 bedroom")
    ])
    bathrooms = DecimalField('No. of Bathrooms', validators=[
        DataRequired(message="Number of bathrooms is required"),
        NumberRange(min=0.5, message="Must have at least 0.5 bathrooms")
    ])
    price = DecimalField('Price', validators=[
        DataRequired(message="Price is required"),
        NumberRange(min=0, message="Price must be positive")
    ])
    location = StringField('Location', validators=[DataRequired(message="Location is required")])
    prop_type = SelectField('Property Type', 
                           choices=[('House', 'House'), ('Apartment', 'Apartment')], 
                           validators=[DataRequired(message="Property type is required")])
    photo = FileField('Photo', validators=[
        FileRequired(message="Please select a photo"),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only! Allowed: JPG, PNG, JPEG')
    ])