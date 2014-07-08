# coding: utf-8
__author__ = 'Jeremy'

import os.path
import config
import data_change_service as dataChangeService
from flask import request, redirect, url_for, Blueprint, jsonify, g, send_from_directory, session
from flask import abort, render_template, flash
from flask_login import login_required
from DoctorSpring.models import Doctor, Hospital, Location, Skill, User, Position, Patient, Diagnose, Pathology, PathologyPostion, File, DiagnoseLog, Comment,UserRole,Message
from database import db_session
from werkzeug.utils import secure_filename
from forms import DiagnoseForm1, DoctorList, DiagnoseForm2, DiagnoseForm3, DiagnoseForm4
from DoctorSpring.util import result_status as rs, object2dict, constant, oss_util
from datetime import datetime, date
from DoctorSpring.util.constant import PatientStatus, Pagger, DiagnoseStatus, ModelStatus, FileType, DiagnoseLogAction, RoleId, UserStatus
from DoctorSpring.util.authenticated import authenticated
from DoctorSpring.util.result_status import *
import random

config = config.rec()
front = Blueprint('front', __name__)

@front.route('/', methods=['GET', 'POST'])
def index():
    return redirect('/homepage')

@front.route('/homepage', methods=['GET', 'POST'])
def homepage():

    resultData={}
    pager = Pagger(1, 6)
    doctors = Doctor.get_doctor_list(0, 0, "", pager)
    doctorsList = dataChangeService.get_doctors_dict(doctors)
    resultData['doctorlist'] = doctorsList
    if len(doctorsList['doctor']) > 0:
        resultData['doctor'] = doctorsList['doctor'][0]
    diagnoseComments=Comment.getRecentComments()
    if diagnoseComments  and  len(diagnoseComments)>0:
        diagnoseCommentsDict=object2dict.objects2dicts_2(diagnoseComments)
        dataChangeService.setDiagnoseCommentsDetailInfo(diagnoseCommentsDict)
        resultData['comments']=diagnoseCommentsDict
    else:
        resultData['comments']=None
    if session.has_key('userId'):
        userId=session['userId']
        messageCount=Message.getMessageCountByReceiver(userId)
        resultData['messageCount']=messageCount
    return render_template("home.html", result=resultData)

@front.route('/applyDiagnose', methods=['GET', 'POST'])
def applyDiagnose():

    if session.has_key('userId'):
        userId=session['userId']
    if userId is None:
        return redirect('/loginPage')

    data = {}
    hospitals = Hospital.getAllHospitals(db_session)
    hospitalsDict = object2dict.objects2dicts(hospitals)
    data['hospitals'] = hospitalsDict

    positions = Position.getPositions()
    positionsDict = object2dict.objects2dicts(positions)
    data['positions'] = positionsDict

    locations = Location.getAllLocations(db_session)
    locationsDict = object2dict.objects2dicts(locations)
    data['locations'] = locationsDict


    if 'edit' in request.args.keys() and 'diagnoseid' in request.args.keys():
        new_diagnose = Diagnose.getDiagnoseById(request.args['diagnoseid'])
        data['edit'] = 1
    else:
        new_diagnose = Diagnose.getNewDiagnoseByStatus(ModelStatus.Draft, session['userId'])

    if new_diagnose is not None:
        data['doctor'] = new_diagnose.doctor
        data['patient'] = new_diagnose.patient
        data['pathology'] = new_diagnose.pathology

        new_file = File.getFiles(new_diagnose.pathologyId, constant.FileType.Dicom)
        data['dicomfile'] = new_file
        new_files = File.getFiles(new_diagnose.pathologyId, constant.FileType.FileAboutDiagnose)
        data['fileAboutDiagnose'] = new_files

        pathologyPositions = []
        if hasattr(new_diagnose, 'pathology') and hasattr(new_diagnose.pathology, 'pathologyPostions'):
            pathologyPositions = object2dict.objects2dicts(new_diagnose.pathology.pathologyPostions)
        data['pathologyPositions'] = pathologyPositions


    patients = Patient.get_patient_by_user(session['userId'])
    if patients is None or len(patients) < 1:
        patientdict = []
    else:
        patientdict = object2dict.objects2dicts(patients)

    data['patientdict'] = patientdict

    return render_template("applyDiagnose.html", result=data)


@front.route('/save/diagnose/<formid>', methods=['GET', 'POST'])
def applyDiagnoseForm(formid):
    if (int(formid) == 1) :
        form = DiagnoseForm3(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            if(form.diagnoseId):
                new_diagnose = Diagnose.getDiagnoseById(form.diagnoseId)
            else:
                new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, session['userId'])
            if(new_diagnose is None):
                new_diagnose = Diagnose()
                new_diagnose.status = DiagnoseStatus.Draft

            new_diagnose.doctorId = form.doctorId
            new_diagnose.uploadUserId = session['userId']

            Diagnose.save(new_diagnose)
            form_result.data = {'formId': 2, 'diagnoseId': new_diagnose.id}
        return jsonify(form_result.__dict__)
    elif (int(formid) == 2) :
        form = DiagnoseForm1(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            if form.diagnoseId is not None:
                new_diagnose = Diagnose.getDiagnoseById(form.diagnoseId)
            else:
                new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, int(session['userId']))
            if(new_diagnose is not None):
                # 去拿没有draft的用户
                if(form.exist):
                    new_patient = Patient.get_patient_by_id(form.patientid)
                else:
                    new_patient = Patient.get_patient_draft(new_diagnose.patientId)
                if new_patient is None:
                    new_patient = Patient()
                    new_patient.type = PatientStatus.diagnose
                    new_patient.userID = session['userId']
                    new_patient.realname = form.patientname
                    new_patient.gender = form.patientsex
                    new_patient.birthDate = datetime.strptime(form.birthdate, "%Y-%m-%d")
                    new_patient.identityCode = form.identitynumber
                    new_patient.locationId = form.locationId
                    new_patient.identityPhone = form.phonenumber
                    new_patient.status = ModelStatus.Draft
                    # new_patient.locationId = form.location
                    Patient.save(new_patient)
                new_diagnose.patientId = new_patient.id
                Diagnose.save(new_diagnose)

                # Hospital User 注册用户
                if(form.isHospitalUser):
                    new_user = User(form.phonenumber, random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',6), False)
                    new_user.type = UserStatus.patent
                    new_user.status = ModelStatus.Draft
                    User.save(new_user)
                    new_patient.userID = new_user.id
                    Patient.save(new_patient)
                    new_userrole = UserRole(new_user.id, RoleId.Patient)
                    UserRole.save(new_userrole)

                form_result.data = {'formId': 3, }
            else:
                form_result = ResultStatus(FAILURE.status, "找不到第一步草稿")
        return jsonify(form_result.__dict__)
    elif (int(formid) == 3):
        form = DiagnoseForm2(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:

            if form.diagnoseId is not None:
                new_diagnose = Diagnose.getDiagnoseById(form.diagnoseId)
            else:
                new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, int(session['userId']))

            if new_diagnose is not None:

                if form.exist:
                    new_pathology = Pathology.getById(form.pathologyId)
                elif new_diagnose.pathologyId:
                    new_pathology = Pathology.getById(new_diagnose.pathologyId)
                else:
                    new_pathology = Pathology.getByPatientStatus(session['userId'], ModelStatus.Draft)

                if new_pathology is None:
                    new_pathology = Pathology(new_diagnose.patientId)

                new_pathology.diagnoseMethod = form.dicomtype
                new_pathology.status = ModelStatus.Draft
                new_pathology.save(new_pathology)

                PathologyPostion.deleteByPathologyId(new_pathology.id)
                for position in form.patientlocation:
                    new_position_id = PathologyPostion(new_pathology.id, position)
                    PathologyPostion.save(new_position_id)

                File.cleanDirtyFile(form.fileurl, new_pathology.id, FileType.Dicom)
                for fileurl in form.fileurl:
                    new_file = File.getFilebyId(int(fileurl))
                    new_file.pathologyId = new_pathology.id
                    File.save(new_file)

                new_diagnose.pathologyId = new_pathology.id
                Diagnose.save(new_diagnose)
                form_result.data = {'formId': 4}
            else:
                form_result = ResultStatus(FAILURE.status, "找不到上步的草稿")
        return jsonify(form_result.__dict__)
    elif (int(formid) == 4):
        form = DiagnoseForm4(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            if form.diagnoseId is not None:
                new_diagnose = Diagnose.getDiagnoseById(form.diagnoseId)
            else:
                new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, int(session['userId']))
            if(new_diagnose is not None):
                new_pathology = Pathology.getById(new_diagnose.pathologyId)
                if(new_pathology is not None):
                    new_pathology.caseHistory = form.illnessHistory
                    new_pathology.hospitalId = form.hospitalId
                    new_pathology.status = ModelStatus.Normal
                    Pathology.save(new_pathology)

                    File.cleanDirtyFile(form.fileurl, new_pathology.id, FileType.FileAboutDiagnose)
                    for fileurl in form.fileurl:
                        new_file = File.getFilebyId(int(fileurl))
                        new_file.pathologyId = new_pathology.id
                        File.save(new_file)

                    new_patient = Patient.get_patient_by_id(new_diagnose.patientId)
                    new_patient.status = PatientStatus.diagnose
                    new_diagnose.status = DiagnoseStatus.NeedPay
                    Diagnose.save(new_diagnose)
                    new_diagnoselog = DiagnoseLog(new_diagnose.uploadUserId, new_diagnose.id, DiagnoseLogAction.NewDiagnoseAction)
                    DiagnoseLog.save(db_session, new_diagnoselog)
                else:
                    form_result = ResultStatus(FAILURE.status, "找不到上步的草稿1")
            else:
                form_result = ResultStatus(FAILURE.status, "找不到上步的草稿2")
        form_result.data = {'isFinal': True}
        return jsonify(form_result.__dict__)
    else:
        return jsonify(ResultStatus(FAILURE.status, "错误的表单号").__dict__)

UPLOAD_FOLDER = 'DoctorSpring/static/tmp/'
ALLOWED_EXTENSIONS = set(['doc', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'zip', 'rar'])

@front.route('/dicomfile/upload', methods=['POST'])
def dicomfileUpload():
    try:
        if request.method == 'POST':
            file_infos = []
            files = request.files
            for key, file in files.iteritems():
                if file and allowed_file(file.filename):
                    filename = file.filename
                    # file_url = oss_util.uploadFile(diagnoseId, filename)
                    from DoctorSpring.util.oss_util import uploadFileFromFileStorage
                    fileurl = uploadFileFromFileStorage(4, filename, file,'',{})


                    new_file = File(FileType.Dicom, filename, '11', fileurl)
                    File.save(new_file)

                    file_infos.append(dict(id=new_file.id,
                                           name=filename,
                                           size=11,
                                           url=fileurl))
                else:
                    return jsonify({'code': 1,  'message' : "error", 'data': ''})
            return jsonify(files=file_infos)
    except Exception,e:
        print e.message
        return jsonify({'code': 1,  'message' : "error", 'data': ''})

@front.route('/patientreport/upload', methods=['POST'])
@login_required
def patientReportUpload():
    try:
        if request.method == 'POST':
            file_infos = []
            files = request.files
            for key, file in files.iteritems():
                if file and allowed_file(file.filename):
                    filename = file.filename
                    # file_url = oss_util.uploadFile(diagnoseId, filename)
                    from DoctorSpring.util.oss_util import uploadFileFromFileStorage
                    fileurl = uploadFileFromFileStorage(4, filename, file,'',{})


                    new_file = File(FileType.FileAboutDiagnose, filename, '11', fileurl)
                    File.save(new_file)

                    file_infos.append(dict(id=new_file.id,
                                           name=filename,
                                           size=11,
                                           url=fileurl))

                else:
                    return jsonify({'code': 1,  'message' : "error", 'data': ''})
            return jsonify(files=file_infos)
    except Exception,e:
        print e.message
        return jsonify({'code': 1,  'message' : "error", 'data': ''})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@front.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)



@front.route('/doctors/list.json')
# /doctors/list.json?hospitalId=1&sectionId=0&doctorname=ddd&pageNumber=1&pageSize=6
def doctor_list_json():
    form = DoctorList(request)
    form_result = form.validate()
    if form_result.status == rs.SUCCESS.status:
        pager = Pagger(form.pageNumber, form.pageSize)
        pager.count = Doctor.get_doctor_count(form.hospitalId, form.sectionId, form.doctorname, pager)
        doctors = Doctor.get_doctor_list(form.hospitalId, form.sectionId, form.doctorname, pager)
        if doctors is None or len(doctors) < 1:
            return jsonify(rs.SUCCESS.__dict__, ensure_ascii=False)
        doctorsDict = dataChangeService.get_doctors_dict(doctors, form.pageNumber, pager.count/pager.pageSize+1)
        resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, doctorsDict)
        return jsonify(resultStatus.__dict__, ensure_ascii=False)
    return jsonify(FAILURE)


@front.route('/doctor/recommanded')
def doctor_rec():

    doctor = None

    if 'doctorid' in request.args.keys():
        doctorId = request.args['doctorid']
        doctor = Doctor.get_doctor(doctorId)
    elif 'diagnoseId' in request.args.keys():
        diagnoseId = int(request.args['diagnoseId'])
        diagnose = Diagnose.getDiagnoseById(diagnoseId)
        if diagnose is not None:
            doctor = diagnose.doctor
    else:
        doctor = Doctor.get_doctor(0, True)

    if doctor is None:
        return jsonify(rs.SUCCESS.__dict__, ensure_ascii=False)
    doctors_dict = dataChangeService.get_doctor(doctor)
    resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, doctors_dict)
    return jsonify(resultStatus.__dict__, ensure_ascii=False)


@front.route('/doctor/list')
def doctor_list():
    result = {}
    hospitals = Hospital.getAllHospitals(db_session)
    hospitalsDict = object2dict.objects2dicts(hospitals)
    result['hospitals'] = hospitalsDict

    skills = Skill.getSkills()
    skillsDict = object2dict.objects2dicts(skills)
    result['skills'] = skillsDict
    return render_template("doctorList.html", result=result)


@front.route('/patient/profile.json')
def patient_profile():
    patientId = request.args['patientId']
    patient = Patient.get_patient_by_id(patientId)
    resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, patient.__dict__)
    if patient is None:
        return jsonify(resultStatus.__dict__)
    resultStatus.data = dataChangeService.get_patient(patient)
    return jsonify(resultStatus.__dict__)


@front.route('/pathlogy/list.json')
def pathlogy_list():
    if 'patientId' in request.args.keys():
        patientId = request.args['patientId']
        pathlogys = Pathology.getByPatientId(patientId)
        if pathlogys is None or len(pathlogys) < 1:
            return jsonify(rs.SUCCESS.__dict__, ensure_ascii=False)
        pathlogysDict = dataChangeService.get_pathology_list(pathlogys)
        resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, pathlogysDict)
        return jsonify(resultStatus.__dict__, ensure_ascii=False)
    return jsonify(SUCCESS.__dict__)


@front.route('/pathlogy/dicominfo.json')
def get_pathology():
    if 'pathologyId' in request.args.keys():
        new_pathology = Pathology.getById(request.args['pathologyId'])
        if new_pathology is not None:
            pathologyDict = dataChangeService.get_pathology(new_pathology)
            result = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, pathologyDict)
            return jsonify(result.__dict__, ensure_ascii=False)
    return jsonify(rs.SUCCESS.__dict__, ensure_ascii=False)


@front.route('/loginPage', methods=['GET', 'POST'])
def loginPage():
    return render_template("loginPage.html")


@front.route('/error', methods=['GET', 'POST'])
def errorPage():
    return render_template("errorPage.html")


@front.route('/userCenter/<int:userId>', methods=['GET', 'POST'])
def userCenter(userId):
    userRole=UserRole.getUserRole(db_session,userId)
    if userRole:
        if userRole.roleId==constant.RoleId.Admin:
            return redirect('/admin/fenzhen')
        if userRole.roleId==constant.RoleId.Doctor:
            return redirect('/doctorhome')
        if userRole.roleId==constant.RoleId.HospitalUser:
            return redirect('/hospital/user')
        if userRole.roleId==constant.RoleId.Patient:
            return redirect('/patienthome')
    return render_template("errorPage.html")

@front.route('/help/center', methods=['GET', 'POST'])
def helpCenterPage():
    return render_template("helpcenter.html")

@front.route('/help/doc', methods=['GET', 'POST'])
def helpDocPage():
    return render_template("helpdoc.html")


@front.route('/about', methods=['GET', 'POST'])
def aboutPage():
    return render_template("about.html")