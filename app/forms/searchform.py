
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional


"""форма поисковой строки
"""
class SearchForm(FlaskForm):
    query = StringField('SEARCH', validators=[Optional()] )
    submit = SubmitField(('🔍'))