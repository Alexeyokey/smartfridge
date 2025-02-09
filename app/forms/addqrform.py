
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, NumberRange

class AddQRForm(FlaskForm):
    """форма для добавления товаров в таблицу QR(создания)

    Args:
        FlaskForm (_type_): _description_
    """
    choices = ['Миллилитры', "Литры", "Граммы", "Килограммы", "Количество"]
    product = SelectField('Продукт', choices=[], coerce=int, validators=[DataRequired()])
    count = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    measurement = IntegerField('Измерение', validators=[DataRequired(), NumberRange(min=1)])
    type_measurement = SelectField('Тип измерения', choices=choices)
    price = IntegerField('Цена', validators=[DataRequired(), NumberRange(min=0)], render_kw={"placeholder": "Рублей"})
    discount_percent = IntegerField('Скидка', validators=[NumberRange(min=0, max=100)], render_kw={"placeholder": "Процентов"})
    produced_date = DateTimeField('Изготовлен', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"type": "date"})
    last_date = DateTimeField('Годен до', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"type": "date"})
    submit = SubmitField('Добавить')