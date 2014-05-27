# coding: utf-8

__author__ = 'jeremyxu'
import os
import unittest
from DoctorSpring.models import Skill, Location
from database import db_session as session



import tempfile

class ModelTestCase(unittest.TestCase):

    def test_add_skill(self):
        new_skill_1 = Skill("头部")
        Skill.save(new_skill_1)
        new_skill_2 = Skill("颈部")
        Skill.save(new_skill_2)
        new_skill_3 = Skill("胸部")
        Skill.save(new_skill_3)

    def test_add_location(self):
        new_location_1 = Location("西安_1")
        Skill.save(new_location_1)
        new_location_2 = Location("西安_2")
        Skill.save(new_location_2)
        new_location_3 = Location("西安_3")
        Skill.save(new_location_3)


    def test_add_location(self):
        new_location_1 = Location("西安_1")
        Skill.save(new_location_1)
        new_location_2 = Location("西安_2")
        Skill.save(new_location_2)
        new_location_3 = Location("西安_3")
        Skill.save(new_location_3)
