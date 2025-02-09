
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional


"""
Форма поисковой строки
"""
class SearchForm(FlaskForm):
    query = StringField('SEARCH', validators=[Optional()] )
    submit = SubmitField(('🔍'))