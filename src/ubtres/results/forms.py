from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class ResultForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    build_date = DateTimeField('Build Date', validators=[DataRequired()])
    arch = StringField('Arch', validators=[DataRequired()])
    cpu = StringField('CPU', validators=[DataRequired()])
    soc = StringField('SoC', validators=[DataRequired()])
    toolchain = StringField('Toolchain', validators=[DataRequired()])
    basecommit = StringField('Base commit', validators=[DataRequired()])
    boardname = StringField('Boardname', validators=[DataRequired()])
    defconfig = StringField('Used default config', validators=[DataRequired()])
    splsize = IntegerField('SPL image size', default=0)
    ubsize = IntegerField('U-Boot image size')
    success = BooleanField('success')

    content = TextAreaField('Content')
    submit = SubmitField('Post')
