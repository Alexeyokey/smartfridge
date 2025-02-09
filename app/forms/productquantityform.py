
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired



"""
Форма для заказа на закупку (количество)
"""
class ProductOrder(FlaskForm):
    quantity = IntegerField('Количество', validators=[DataRequired()], render_kw={"placeholder": "Штук"})
    product_id = HiddenField()
    submit = SubmitField(('Добавить в список покупок'))