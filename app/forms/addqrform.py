
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, NumberRange

class AddQRForm(FlaskForm):
    """форма для добавления товаров в таблицу QR(создания)

    Args:
        FlaskForm (_type_): _description_
    """
    product = SelectField('Product', choices=[], coerce=int, validators=[DataRequired()])
    count = IntegerField('Count', validators=[DataRequired(), NumberRange(min=1)], render_kw={"placeholder": "Штук"})
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)], render_kw={"placeholder": "Рублей"})
    discount_percent = IntegerField('Discount Percent', validators=[NumberRange(min=0, max=100)], render_kw={"placeholder": "Процентов"})
    produced_date = DateTimeField('Produced Date', format='%Y-%m-%d', validators=[DataRequired()])
    last_date = DateTimeField('Last Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Product')