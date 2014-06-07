# coding: utf-8
__author__ = 'jeremyxu'

import unittest
from DoctorSpring.models import Skill, Location, User, Doctor, Hospital, Department, Patient, Doctor2Skill ,Diagnose
from DoctorSpring.util.constant import UserStatus

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

    def test_add_department(self):
        new_department_1 = Department("影像科")
        Skill.save(new_department_1)
        new_department_2 = Department("内科")
        Skill.save(new_department_2)
        new_department_3 = Department("外科")
        Skill.save(new_department_3)

    def test_add_hospital(self):
        new_hospital_1 = Hospital("西11安西京医院", "地址——西11安西京医院", "描述-西22安西京医院", "11")
        Skill.save(new_hospital_1)
        new_hospital_2 = Hospital("西22安西京医院", "地址——西22安西京医院", "描述-西22安西京医院", "22")
        Skill.save(new_hospital_2)
        new_hospital_3 = Hospital("西33安西京医院", "地址——西33安西京医院", "描述-西22安西京医院", "33")
        Skill.save(new_hospital_3)

class UserTestCase(unittest.TestCase):

    def test_add_patient(self):
        new_user = User("xuyanbj@cn.ibm.com", "123456")
        new_user.type = UserStatus.patent
        User.save(new_user)
        new_patient = Patient(new_user.id)
        Patient.save(new_patient)

    def test_getById(self):
        diagnose=Diagnose.getDiagnoseById(1)
        print diagnose.id

    def test_add_doctor(self):

        new_skill_1 = Skill("头部")
        Skill.save(new_skill_1)
        new_skill_2 = Skill("颈部")
        Skill.save(new_skill_2)
        new_skill_3 = Skill("胸部")
        Skill.save(new_skill_3)

        new_hospital = Hospital("西22安西京医院", "地址——西22安西京医院", "描述-西22安西京医院", "22")
        Hospital.save(new_hospital)

        new_department_1 = Department("影像科")
        Skill.save(new_department_1)
        new_department_2 = Department("内科")
        Skill.save(new_department_2)
        new_department_3 = Department("外科")
        Skill.save(new_department_3)

        new_user_1 = User("任志强", "123456")
        new_user_1.email = "renzhiqiang@qq.com"
        new_user_1.phone = "1851113456767"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "010-123455678"

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师1"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)


        new_user_2 = User("任小强", "123456")
        new_user_2.email = "renxiaoqiang@qq.com"
        new_user_2.phone = "1851112256767"
        new_user_2.type = UserStatus.doctor
        User.save(new_user_2)

        new_doctor_2 = Doctor(new_user_2.id)
        new_doctor_2.identityPhone = "010-123456678"

        new_doctor_2.hospitalId = new_hospital.id
        new_doctor_2.departmentId = new_department_2.id
        new_doctor_2.title = "副主任医师2"

        Doctor.save(new_doctor_2)
        new_doctor2skill_2_1 = Doctor2Skill(new_doctor_2.id, new_skill_2.id)
        Doctor2Skill.save(new_doctor2skill_2_1)
        new_doctor2skill_2_2 = Doctor2Skill(new_doctor_2.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_2_2)


        new_user_3 = User("任大强", "123456")
        new_user_3.email = "rendaqiang@qq.com"
        new_user_3.phone = "1851114256767"
        new_user_3.type = UserStatus.doctor
        User.save(new_user_3)

        new_doctor_3 = Doctor(new_user_3.id)
        new_doctor_3.identityPhone = "020-123456678"

        new_doctor_3.hospitalId = new_hospital.id
        new_doctor_3.departmentId = new_department_3.id
        new_doctor_3.title = "副主任医师2"

        Doctor.save(new_doctor_3)
        new_doctor2skill_3_1 = Doctor2Skill(new_doctor_3.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_3_1)
        new_doctor2skill_3_2 = Doctor2Skill(new_doctor_3.id, new_skill_2.id)
        Doctor2Skill.save(new_doctor2skill_3_2)