# coding: utf-8
__author__ = 'Jeremy'

from DoctorSpring import app
from database import init_db
init_db()
app.run(debug = True)