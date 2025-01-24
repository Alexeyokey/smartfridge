
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Optional, DataRequired, NumberRange



"""форма поисковой строки
"""
class SearchForm(FlaskForm):
    query = StringField('SEARCH', validators=[Optional()] )
    submit = SubmitField(('🔍'))