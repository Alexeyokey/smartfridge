
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired



"""форма для заказа на закупку (количество)
"""
class Quantity(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()], render_kw={"placeholder": "Штук"})