
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import Optional, DataRequired, NumberRange

class AddForm(FlaskForm):
    """форма для добавления товаров в таблицу Product(создания)

    Args:
        FlaskForm (_type_): _description_
    """
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type',  choices=[],  validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()], render_kw={"placeholder": "Ккал"})
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    allergic = BooleanField('Allergic', validators=[Optional()])
    submit = SubmitField('Add Product')