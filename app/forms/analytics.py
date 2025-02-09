
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, NumberRange

class AnalyticsDates(FlaskForm):
    """форма для добавления товаров в таблицу QR(создания)

    Args:
        FlaskForm (_type_): _description_
    """
    start_date = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Обновить')