# coding: utf-8
__author__ = 'jeremyxu'

import unittest
from DoctorSpring.models import Skill, Location, User, Doctor, Hospital, Department, Patient, Doctor2Skill ,Position, UserRole, DoctorProfile
from DoctorSpring.util.constant import UserStatus, RoleId, DoctorProfileType
from database import db_session as session
from DoctorSpring.models.comment import Comment

class RoleTestCase(unittest.TestCase):
    def test_addAllRole(self):
        from DoctorSpring.models.user import Role,UserRole
        role=Role()
        role.id=1
        role.roleName='admin'
        session.add(role)

        role=Role()
        role.id=2
        role.roleName='doctor'
        session.add(role)

        role=Role()
        role.id=3
        role.roleName='patient'
        session.add(role)

        role=Role()
        role.id=4
        role.roleName='hospitalUser'
        session.add(role)

        session.commit()
        session.flush()

class RealModelTestCase(unittest.TestCase):

    def test_add_skill(self):
        new_skill_1 = Skill("神经系统")
        Skill.save(new_skill_1)
        new_skill_2 = Skill("肿瘤")
        Skill.save(new_skill_2)
        new_skill_3 = Skill("骨科")
        Skill.save(new_skill_3)
        new_skill_4 = Skill("内分泌科")
        Skill.save(new_skill_4)

    def test_add_position(self):
        new_skill_1 = Position("头颅")
        Skill.save(new_skill_1)
        new_skill_2 = Position("腹部")
        Skill.save(new_skill_2)
        new_skill_3 = Position("胸部")
        Skill.save(new_skill_3)
        new_skill_4 = Position("呼吸纵隔")
        Skill.save(new_skill_4)


    def test_add_location(self):
        new_location_1 = Location("陕西，西安")
        Skill.save(new_location_1)
        new_location_2 = Location("陕西，汉中")
        Skill.save(new_location_2)
        new_location_3 = Location("北京")
        Skill.save(new_location_3)
        new_location_4 = Location("四川，成都")
        Skill.save(new_location_4)

    def test_add_department(self):
        new_department_1 = Department("放射科")
        Skill.save(new_department_1)
        new_department_2 = Department("内科")
        Skill.save(new_department_2)
        new_department_3 = Department("外科")
        Skill.save(new_department_3)
        new_department_4 = Department("肿瘤科")
        Skill.save(new_department_4)

    def test_add_hospital(self):
        new_hospital_1 = Hospital("西安西京医院", "地址——西安西京医院", "描述-西安西京医院", 1)
        Skill.save(new_hospital_1)


class UserTestCase(unittest.TestCase):
    def test_addPatient(self):
        source='123456'
        from DoctorSpring.util.hash_method import getHashPasswd
        passwd=getHashPasswd(source)
        user=User('liclu',passwd)
        user.sex=0
        user.status=0
        user.email='liclu@adobe.com'
        user.address='四川省 通江县'
        user.phone = '15210892443'
        User.save(user)
        patient=Patient()
        patient.gender=0
        patient.Name='程成'
        patient.status=0
        patient.userID=user.id
        Patient.save(patient)
        new_userrole = UserRole(user.id, RoleId.Patient)
        UserRole.save(new_userrole)


    def test_addDoctor(self):
        new_user_1 = User("11111111111", "123456")
        new_user_1.email = "yinhong@qq.com"
        new_user_1.phone = "111111111111"
        new_user_1.type = UserStatus.doctor
        User.save(new_user_1)

        new_doctor_1 = Doctor(new_user_1.id)
        new_doctor_1.identityPhone = "029-12345567"
        new_doctor_1.username = "印弘"
        new_doctor_1.diagnoseCount = 10
        new_doctor_1.feedbackCount = 5
        new_doctor_1.goodFeedbackCount = 5
        new_doctor_1.hospitalId = 1
        new_doctor_1.departmentId = 1
        new_doctor_1.title = "主任医师"
        new_doctor_1.status = 0


        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id,1)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_userrole = UserRole(new_user_1.id, RoleId.Doctor)
        UserRole.save(new_userrole)




        new_user_2 = User("22222222222", "123456")
        new_user_2.email = "huanyi@qq.com"
        new_user_2.phone = "22222222222"
        new_user_2.type = UserStatus.doctor
        User.save(new_user_2)

        new_doctor_2 = Doctor(new_user_2.id)
        new_doctor_2.identityPhone = "029-12345567"
        new_doctor_2.username = "宦怡"
        new_doctor_2.diagnoseCount = 8
        new_doctor_2.feedbackCount = 3

        new_doctor_2.hospitalId = 1
        new_doctor_2.departmentId = 1
        new_doctor_2.title = "主任医师"
        new_doctor_2.status = 0
        new_doctor_2.goodFeedbackCount = 2

        Doctor.save(new_doctor_2)
        new_doctor2skill_1_2 = Doctor2Skill(new_doctor_2.id,2)
        Doctor2Skill.save(new_doctor2skill_1_2)
        new_userrole2 = UserRole(new_user_2.id, RoleId.Doctor)
        UserRole.save(new_userrole2)

        new_user_3 = User("33333333333", "123456")
        new_user_3.email = "zhangjinsong@qq.com"
        new_user_3.phone = "33333333333"
        new_user_3.type = UserStatus.doctor
        User.save(new_user_3)

        new_doctor_3 = Doctor(new_user_3.id)
        new_doctor_3.identityPhone = "029-12345567"
        new_doctor_3.username = "张劲松"
        new_doctor_3.diagnoseCount = 9
        new_doctor_3.feedbackCount = 4

        new_doctor_3.hospitalId = 1
        new_doctor_3.departmentId = 1
        new_doctor_3.title = "主任医师"
        new_doctor_3.status = 0
        new_doctor_3.goodFeedbackCount = 3

        Doctor.save(new_doctor_3)
        new_doctor2skill_1_3 = Doctor2Skill(new_doctor_3.id,3)
        Doctor2Skill.save(new_doctor2skill_1_3)
        new_userrole3 = UserRole(new_user_3.id, RoleId.Doctor)
        UserRole.save(new_userrole3)


        dp=DoctorProfile()
        dp.type=DoctorProfileType.Intro
        dp.description='从事影像诊断多年，对普通放射、CT以及血管造影的影像诊断有丰富的经验，能够综合各种诊断手段进行诊断。对磁共振的影像诊断有丰富的经验，尤其侧重神经系统疑难疾病的诊断，采用磁共振波谱等多项先进技术，对神经系统肿瘤，肌萎缩性侧索硬化、癫痫以及先天性发育异常、变性疾病等神经系统疾病进行诊断及预后评估，有独到的诊断特色。与神经外科合作，开展肿瘤术前功能定位定向，确保了手术的安全性以及有效性；与身心科合作，开展了精神疾病诊断及临床研究工作。'
        dp.userId= new_user_1.id
        DoctorProfile.save(dp)

        dp=DoctorProfile()
        dp.type=DoctorProfileType.Resume
        dp.userId= new_user_1.id
        dp.description='印弘, 西京医院放射科主任，教授，主任医师，博士，硕士研究生导师。 毕业于第四军医大学。先后在新加坡国立神经科学研究所及美国加州大学旧金山分校作为访问学者工作。承担或参加北京市自然科学基金，新加坡国家医学基金,国家十一五科技支撑项目等多项科研基金，任职期间发表学术论文20余篇，其中SCI 5篇。'
        DoctorProfile.save(dp)


        dp=DoctorProfile()
        dp.type=DoctorProfileType.Award
        dp.userId= new_user_1.id
        dp.description='担任国家自然科学基金委主办杂志《自然》杂志以及《实用放射学杂志》特约审稿专家'
        DoctorProfile.save(dp)


        dp=DoctorProfile()
        dp.type=DoctorProfileType.Other
        dp.userId= new_user_1.id
        dp.description='陕西省影像协会会长'
        DoctorProfile.save(dp)


        dp2=DoctorProfile()
        dp2.type=DoctorProfileType.Intro
        dp2.description='主要从事CT、MRI诊断及相关基础研究。90年代初在国内率先开展CT 影像后处理研究，在3D CE MRA、CTA成像，耳部HRCT、HRMRI影像及影像解剖基础研究，泌尿系疾患CT、MRI成像及前列腺癌的分子影像学方面做了较多的工作，并获得省及国家自然科学基金资助。'
        dp2.userId= new_user_2.id
        DoctorProfile.save(dp2)

        dp2=DoctorProfile()
        dp2.type=DoctorProfileType.Resume
        dp2.userId= new_user_2.id
        dp2.description='宦怡，主任医师，教授，博士生导师。先后共发表论文70余篇，主编副主编专著2部，参编的专著6部。承担国家自然科学基金、陕西省自然科学基金课题各1项，参与国家自然科学基金2项，国家“九五”科技公关攻关课题1项，军队青年基金课题1项。'
        DoctorProfile.save(dp2)


        dp2=DoctorProfile()
        dp2.type=DoctorProfileType.Award
        dp2.userId= new_user_2.id
        dp2.description='军队医疗成果二等奖1项，三等奖5项'
        DoctorProfile.save(dp2)


        dp3=DoctorProfile()
        dp3.type=DoctorProfileType.Intro
        dp3.description='长期坚持临床一线工作，历经放射科X线诊断组、CT组和磁共振组等部门工作，熟练掌握CT、MRI影像诊断。每年承担医疗系和口腔系5年制本科学员、8年制学员等的大课教学工作，发表教学论文4篇；指导进修生多人；参与指导硕士研究生及博士生多名。多次参加全国及省放射学会的专题讲座。'
        dp3.userId= new_user_3.id
        DoctorProfile.save(dp3)

        dp3=DoctorProfile()
        dp3.type=DoctorProfileType.Resume
        dp3.userId= new_user_3.id
        dp3.description='张劲松，男，副主任医师、副教授。1994年本科毕业于第四军医大学临床医学系(6年制本科)，1997年获第四军医大学影像医学硕士学位,2005年获第四军医大学影像医学博士学位。2008年赴美国南加州大学放射科进修学习半年。'
        DoctorProfile.save(dp3)


        dp3=DoctorProfile()
        dp3.type=DoctorProfileType.Award
        dp3.userId= new_user_3.id
        dp3.description='获得省科技进步一等奖1项，全军医疗成果二等奖2项，全军医疗成果三等奖6项'
        DoctorProfile.save(dp3)

    def test_addSuperUser(self):
        source='123456'
        from DoctorSpring.util.hash_method import getHashPasswd
        passwd=getHashPasswd(source)
        user=User('zhoufan',passwd)
        user.sex=0
        user.status=0
        user.email='zhoufan@adobe.com'
        user.address='四川省 通江县'
        user.phone = '13426026573'
        user.type = UserStatus.doctor
        user.name = "张西"
        User.save(user)


        patient=Patient()
        patient.gender=0
        patient.Name='zf'
        patient.status=0
        patient.userID=user.id
        Patient.save(patient)
        new_userrole = UserRole(user.id, RoleId.Patient)
        UserRole.save(new_userrole)

        new_doctor_1 = Doctor(user.id)
        new_doctor_1.identityPhone = "029-12345567"
        new_doctor_1.username = "张西"
        new_doctor_1.diagnoseCount = 10
        new_doctor_1.feedbackCount = 5
        new_doctor_1.goodFeedbackCount = 5
        new_doctor_1.hospitalId = 1
        new_doctor_1.departmentId = 1
        new_doctor_1.title = "副主任医师"
        new_doctor_1.status = 0


        Doctor.save(new_doctor_1)
        new_doctor2skill_1_1 = Doctor2Skill(new_doctor_1.id,1)
        Doctor2Skill.save(new_doctor2skill_1_1)
        new_userrole1 = UserRole(user.id, RoleId.Doctor)
        UserRole.save(new_userrole1)
        new_userrole2 = UserRole(user.id, RoleId.Admin)
        UserRole.save(new_userrole2)






