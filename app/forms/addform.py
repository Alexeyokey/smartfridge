
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import Optional, DataRequired, NumberRange

class AddForm(FlaskForm):
    """форма для добавления товаров в таблицу Product(создания)

    Args:
        FlaskForm (_type_): _description_
    """
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type',  choices=[],  validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    allergic = BooleanField('Allergic', validators=[DataRequired()])
    submit = SubmitField('Add Product')