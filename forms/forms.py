from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Regexp

import re

class UserInputForm(FlaskForm):

    route_len = StringField("Довжина маршруту (км):",
                             validators=[DataRequired("Будь ласка, уведіть дані"),
                                         Regexp(regex=r'^\d+.*\d+$', message='Уведіть число з крапкою або без')])

    number_of_vehicles = StringField("Кількість транспортних засобів:",
                                      validators=[DataRequired("Будь ласка, уведіть дані"),
                                                  Regexp(regex=r'^\d+$', message='Уведіть число без крапки')])

    passenger_capacity = StringField("Середня пасажиромісткість (люд):",
                                      validators=[DataRequired("Будь ласка, уведіть дані"),
                                                  Regexp(regex=r'^\d+$', message='Уведіть число без крапки')])

    route_time = StringField("Час повного обороту (гг:хх):",
                             validators=[DataRequired("Будь ласка, уведіть дані"),
                                         Regexp(regex=r'[0-2]?[0-9]\:[0-5][0-9]$', message='Уведіть коректний час')])

    first_guard = StringField("Початок першої зміни (гг:хх):",
                              validators=[DataRequired("Будь ласка, уведіть дані"),
                                          Regexp(regex=r'^[0-2]?[0-9]\:[0-5][0-9]$', message='Уведіть коректний час')])

    guard_duration = SelectField("Тривалість зміни (г):",
                                 choices=[('1', '1'),
                                          ('2', '2'),
                                          ('3', '3'),
                                          ('4', '4'),
                                          ('5', '5'),
                                          ('6', '6'),
                                          ('7', '7'),
                                          ('8', '8')],
                                 validators=[DataRequired("Будь ласка, уведіть дані")])

    number_of_guards = SelectField("Кількість змін:",
                                   choices=[('1', '1'),
                                            ('2', '2'),
                                            ('3', '3'),
                                            ('4', '4'),
                                            ('5', '5'),
                                            ('6', '6'),
                                            ('7', '7'),
                                            ('8', '8')],
                                    validators=[DataRequired("Будь ласка, уведіть дані")])

    area_population = StringField("Населення міста (люд):",
                                   validators=[DataRequired("Будь ласка, уведіть дані"),
                                               Regexp(regex=r'^\d+$', message='Уведіть число без крапки')])

    area_square = StringField("Площа міста (км2): ",
                               validators=[DataRequired("Будь ласка, уведіть дані"),
                                           Regexp(regex=r'^\d+.\d+$', message='Уведіть коректні дані')])

    submit = SubmitField("Результат!")
