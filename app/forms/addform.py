
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import Optional, DataRequired, NumberRange

class AddForm(FlaskForm):
    """форма для добавления товаров в таблицу Product(создания)

    Args:
        FlaskForm (_type_): _description_
    """
    name = StringField('Название', validators=[DataRequired()])
    type = StringField('Тип', validators=[DataRequired()])
    calories = IntegerField('Калории', validators=[DataRequired()], render_kw={"placeholder": "Ккал"})
    ingredients = TextAreaField('Ингредиенты', validators=[DataRequired()])
    allergic = BooleanField('Аллергический', validators=[Optional()])
    submit = SubmitField('Добавить продукт')