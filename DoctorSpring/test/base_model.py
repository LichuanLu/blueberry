# coding: utf-8
__author__ = 'jeremyxu'

import unittest
from DoctorSpring.models import Skill, Location, User, Doctor, Hospital, Department, Patient, Doctor2Skill ,Position, UserRole
from DoctorSpring.util.constant import UserStatus, RoleId

class ModelTestCase(unittest.TestCase):

    def test_add_skill(self):
        new_skill_1 = Skill("头部")
        Skill.save(new_skill_1)
        new_skill_2 = Skill("颈部")
        Skill.save(new_skill_2)
        new_skill_3 = Skill("胸部")
        Skill.save(new_skill_3)

    def test_add_position(self):
        new_skill_1 = Position("头部")
        Skill.save(new_skill_1)
        new_skill_2 = Position("颈部")
        Skill.save(new_skill_2)
        new_skill_3 = Position("胸部")
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
        new_userrole = UserRole(new_user.id, RoleId.Patient)
        UserRole.save(new_userrole)


    def test_add_doctor(self):


        new_location_1 = Location("西安_1")
        Skill.save(new_location_1)
        new_location_2 = Location("西安_2")
        Skill.save(new_location_2)
        new_location_3 = Location("西安_3")
        Skill.save(new_location_3)

        new_skill_1 = Skill("头部")
        Skill.save(new_skill_1)
        new_skill_2 = Skill("颈部")
        Skill.save(new_skill_2)
        new_skill_3 = Skill("胸部")
        Skill.save(new_skill_3)

        new_skill_1 = Position("头部")
        Skill.save(new_skill_1)
        new_skill_2 = Position("颈部")
        Skill.save(new_skill_2)
        new_skill_3 = Position("胸部")
        Skill.save(new_skill_3)

        new_hospital = Hospital("西22安西京医院", "地址——西22安西京医院", "描述-西22安西京医院", "22")
        Hospital.save(new_hospital)

        new_department_1 = Department("影像科")
        Skill.save(new_department_1)
        new_department_2 = Department("内科")
        Skill.save(new_department_2)
        new_department_3 = Department("外科")
        Skill.save(new_department_3)

        new_user_1 = User("18511134676", "123456")
        new_user_1.email = "renzhiqiang@qq.com"
        new_user_1.phone = "18511134676"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "010-12345567"
        new_doctor_1.username = "任大强"
        new_doctor_1.diagnoseCount = 777
        new_doctor_1.feedbackCount = 888

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师1"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)

        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)


        new_user_2 = User("18511122567", "123456")
        new_user_2.email = "renxiaoqiang@qq.com"
        new_user_2.phone = "18511122567"
        new_user_2.type = UserStatus.doctor
        User.save(new_user_2)

        new_doctor_2 = Doctor(new_user_2.id)
        new_doctor_2.identityPhone = "010-12345667"
        new_doctor_2.username = "任小强"
        new_doctor_2.diagnoseCount = 666
        new_doctor_2.feedbackCount = 777

        new_doctor_2.hospitalId = new_hospital.id
        new_doctor_2.departmentId = new_department_2.id
        new_doctor_2.title = "副主任医师2"

        Doctor.save(new_doctor_2)
        new_doctor2skill_2_1 = Doctor2Skill(new_doctor_2.id, new_skill_2.id)
        Doctor2Skill.save(new_doctor2skill_2_1)
        new_doctor2skill_2_2 = Doctor2Skill(new_doctor_2.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_2_2)

        new_userrole = UserRole(new_user_2.id, RoleId.Doctor)
        UserRole.save(new_userrole)

        new_user_3 = User("18511142567", "123456")
        new_user_3.email = "rendaqiang@qq.com"
        new_user_3.phone = "18511142567"
        new_user_3.type = UserStatus.doctor
        User.save(new_user_3)

        new_doctor_3 = Doctor(new_user_3.id)
        new_doctor_3.identityPhone = "020-12346678"
        new_doctor_3.username = "任志强"

        new_doctor_3.hospitalId = new_hospital.id
        new_doctor_3.departmentId = new_department_3.id
        new_doctor_3.title = "副主任医师2"
        new_doctor_3.diagnoseCount = 999
        new_doctor_3.feedbackCount = 1000
        Doctor.save(new_doctor_3)
        new_doctor2skill_3_1 = Doctor2Skill(new_doctor_3.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_3_1)
        new_doctor2skill_3_2 = Doctor2Skill(new_doctor_3.id, new_skill_2.id)
        Doctor2Skill.save(new_doctor2skill_3_2)
        new_userrole = UserRole(new_user_3.id, RoleId.Doctor)
        UserRole.save(new_userrole)


        new_user_1 = User("18511114676", "123456")
        new_user_1.email = "renzh2qiang@qq.com"
        new_user_1.phone = "18511234676"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "020-12345567"
        new_doctor_1.username = "任1强"
        new_doctor_1.diagnoseCount = 775
        new_doctor_1.feedbackCount = 788

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师2"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)

        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)


        new_user_1 = User("18511114676", "123456")
        new_user_1.email = "renzh2qiang@qq.com"
        new_user_1.phone = "18511234676"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "020-12345567"
        new_doctor_1.username = "任1强"
        new_doctor_1.diagnoseCount = 775
        new_doctor_1.feedbackCount = 788

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师2"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)
        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)


        new_user_1 = User("18511114676", "123456")
        new_user_1.email = "renzh2qiang@qq.com"
        new_user_1.phone = "18511234676"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "020-12345567"
        new_doctor_1.username = "任1强"
        new_doctor_1.diagnoseCount = 775
        new_doctor_1.feedbackCount = 788

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师2"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)
        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)



        new_user_1 = User("18511114676", "123456")
        new_user_1.email = "renzh2qiang@qq.com"
        new_user_1.phone = "18511234676"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "020-12345567"
        new_doctor_1.username = "任1强"
        new_doctor_1.diagnoseCount = 775
        new_doctor_1.feedbackCount = 788

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师2"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)

        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)


        new_user_1 = User("18511114676", "123456")
        new_user_1.email = "renzh2qiang@qq.com"
        new_user_1.phone = "18511234676"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "020-12345567"
        new_doctor_1.username = "任1强"
        new_doctor_1.diagnoseCount = 775
        new_doctor_1.feedbackCount = 788

        new_doctor_1.hospitalId = new_hospital.id
        new_doctor_1.departmentId = new_department_1.id
        new_doctor_1.title = "副主任医师2"

        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id, new_skill_1.id)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_1.id, new_skill_3.id)
        Doctor2Skill.save(new_doctor2skill_1_2)

        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)