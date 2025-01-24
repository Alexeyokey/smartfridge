
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Optional, DataRequired, NumberRange

class AddQRForm(FlaskForm):
    """форма для добавления товаров в таблицу QR(создания продуктов)

    Args:
        FlaskForm (_type_): _description_
    """
    product = SelectField('Product', choices=[], coerce=int, validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired(), NumberRange(min=1)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discount_percent = IntegerField('Discount Percent', validators=[NumberRange(min=0, max=100)])
    produced_date = DateTimeField('Produced Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    last_date = DateTimeField('Last Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Add Product')