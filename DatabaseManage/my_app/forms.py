import re

from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError

class CreateTableForm(FlaskForm):
	def validate_table_name(self, table_name_to_check):
		regex = re.compile("[^a-zA-Z0-9_.-]")
		match = regex.match(table_name_to_check)
		if match:
			raise ValidationError("Invalid input")

	name_database = fields.StringField(label='nameDatabase', validators=[DataRequired(), Length(min=3, max=255)])
	name_table = fields.StringField(label='nameTable', validators=[DataRequired(), Length(min=3, max=255)])

class LoginForm(FlaskForm):
	username = fields.StringField(label='User Name:', validators=[DataRequired()])
	password = fields.PasswordField(label='Password:', validators=[Length(min=8, max=60), DataRequired()])
	submit = fields.SubmitField(label='Sign In')
