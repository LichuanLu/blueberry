# coding: utf-8
__author__ = 'Jeremy'

import os.path
import config
import data_change_service as dataChangeService
from flask import request, redirect, url_for, Blueprint, jsonify, g, send_from_directory, session
from flask import abort, render_template, flash
from flask_login import login_required
from DoctorSpring.models import Doctor, Hospital, Skill, User, Department, Patient, Diagnose, Pathology, PathologyPostion, File, DiagnoseLog, Comment,UserRole,Message
from database import db_session
from werkzeug.utils import secure_filename
from forms import DiagnoseForm1, DoctorList, DiagnoseForm2, DiagnoseForm3, DiagnoseForm4
from DoctorSpring.util import result_status as rs, object2dict, constant, oss_util
from datetime import datetime
from DoctorSpring.util.constant import PatientStatus, Pagger, DiagnoseStatus, ModelStatus, FileType, DiagnoseLogAction
from DoctorSpring.util.result_status import *

config = config.rec()
front = Blueprint('front', __name__)

@front.route('/', methods=['GET', 'POST'])
@front.route('/homepage', methods=['GET', 'POST'])
def homepage():

    resultData={}
    pager = Pagger(1, 6)
    doctors = Doctor.get_doctor_list(0, 0, "", pager)
    doctorsDict = dataChangeService.get_doctors_dict(doctors)
    resultData['doctorlist'] = doctorsDict
    doctor = Doctor.get_doctor_list(0, 0, "", pager, True)
    if doctor is not None:
        doctorDict = dataChangeService.get_doctor(doctor)
    resultData['doctor'] = doctorDict
    
    diagnoseComments=Comment.getRecentComments()
    if diagnoseComments  and  len(diagnoseComments)>0:
        diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
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
    data = {}

    editStatus = 'false'
    hospitals = Hospital.getAllHospitals(db_session)
    hospitalsDict = object2dict.objects2dicts(hospitals)
    data['hospitals'] = hospitalsDict

    skills = Skill.getSkills()
    skillsDict = object2dict.objects2dicts(skills)
    data['skills'] = skillsDict


    if hasattr(request.args, "edit"):
        editStatus = request.args['edit']
    data['edit'] = editStatus
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
            new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, session['userId'])
            if(new_diagnose is None):
                new_diagnose = Diagnose()
            new_diagnose.doctorId = form.doctorId
            new_diagnose.uploadUserId = session['userId']
            new_diagnose.status = DiagnoseStatus.Draft
            Diagnose.save(new_diagnose)
            form_result.data = {'formId': 2}
        return jsonify(form_result.__dict__)
    elif (int(formid) == 2) :
        form = DiagnoseForm1(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, int(session['userId']))
            if(new_diagnose is not None):
                # 去拿没有draft的用户
                new_patient = Patient.get_patient_draft(new_diagnose.patientId)
                if new_patient is None:
                    new_patient = Patient()
                    new_patient.type = PatientStatus.diagnose
                    new_patient.userID = session['userId']
                    new_patient.realname = form.patientname
                    new_patient.gender = form.patientsex
                    new_patient.birthDate = datetime.strptime(form.birthdate, "%Y-%m-%d")
                    new_patient.identityCode = form.identitynumber

                    new_patient.identityPhone = form.phonenumber
                    new_patient.status = ModelStatus.Draft
                    # new_patient.locationId = form.location
                    Patient.save(new_patient)
                new_diagnose.patientId = new_patient.id
                form_result.data = {'formId': 3}
            else:
                form_result = ResultStatus(FAILURE.status, "找不到第一步草稿")
        return jsonify(form_result.__dict__)
    elif (int(formid) == 3):
        form = DiagnoseForm2(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, session['userId'])
            if(new_diagnose is not None):
                new_pathology = Pathology()
                new_pathology.diagnoseMethod = form.dicomtype
                new_pathology.status = ModelStatus.Draft
                new_pathology.save(new_pathology)
                new_diagnose.pathologyId = new_pathology.id
                Diagnose.save(new_diagnose)
                for position in form.patientlocation:
                    new_position_id = PathologyPostion(position, new_pathology.id)
                    PathologyPostion.save(new_position_id)

                new_file = File(FileType.Dicom, form.fileurl, new_pathology.id)
                File.save(new_file)
                Pathology.save(new_pathology)
                form_result.data = {'formId': 4}
            else:
                form_result = ResultStatus(FAILURE.status, "找不到上步的草稿")
        return jsonify(form_result.__dict__)
    elif (int(formid) == 4):
        form = DiagnoseForm4(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, session['userId'])
            if(new_diagnose is not None):
                new_pathology = Pathology.getById(new_diagnose.pathologyId)
                if(new_pathology is not None):
                    new_pathology.caseHistory = form.illnessHistory
                    new_pathology.hospticalId = form.hospitalId
                    for fileurl in form.fileurl:
                        new_file = File(FileType.FileAboutDiagnose, fileurl, new_pathology.id)
                        File.save(new_file)
                    new_pathology.status = ModelStatus.Normal
                    Pathology.save(new_pathology)
                    new_patient = Patient.get_patient_by_id(new_diagnose.patientId)
                    new_patient.status = PatientStatus.diagnose
                    new_diagnose.status = DiagnoseStatus.NeedDiagnose
                    new_diagnoselog = DiagnoseLog(new_diagnose.uploadUserId, new_diagnose.id, DiagnoseLogAction.NewDiagnoseAction)
                    DiagnoseLog.save(db_session, new_diagnoselog)
                else:
                    form_result = ResultStatus(FAILURE.status, "找不到上步的草稿1")
            else:
                form_result = ResultStatus(FAILURE.status, "找不到上步的草稿2")
        return jsonify(form_result.__dict__)
    else:
        return jsonify(ResultStatus(FAILURE.status, "错误的表单号").__dict__)

UPLOAD_FOLDER = 'DoctorSpring/static/tmp/'
ALLOWED_EXTENSIONS = set(['doc', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'zip', 'rar'])

@front.route('/dicomfile/upload', methods=['POST'])
@login_required
def dicomfileUpload():
    try:
        if request.method == 'POST':
            file_infos = []
            files = request.files
            for key, file in files.iteritems():
                if file and allowed_file(file.filename):
                    from DoctorSpring.util.oss_util import uploadFileFromFileStorage
                    uploadFileFromFileStorage(4,'cc',file,'',{})
                    file_infos.append(dict(name='cc',
                                           size=11,
                                           url='ccc'))
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
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    file_size = os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
                    file_url = "/static/patientreport/"+filename
                    file_infos.append(dict(name=filename,
                                           size=file_size,
                                           url=file_url))
                else:
                    return jsonify({'code': 1,  'message' : "error", 'data': ''})
            return jsonify(files=file_infos)
    except:
        raise
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
        count = Doctor.get_doctor_count(form.hospitalId, form.sectionId, form.doctorname, pager)
        doctors = Doctor.get_doctor_list(form.hospitalId, form.sectionId, form.doctorname, pager)
        if doctors is None or len(doctors) < 1:
            return jsonify(rs.SUCCESS.__dict__, ensure_ascii=False)
        doctorsDict = dataChangeService.get_doctors_dict(doctors, form.pageNumber, count)
        resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, doctorsDict)
        return jsonify(resultStatus.__dict__, ensure_ascii=False)
    return jsonify(FAILURE)


@front.route('/doctor/recommanded')
def doctor_rec():
    doctor = Doctor.get_doctor_list(0, 0, '', None, True)
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
    if hasattr(request.args, 'patientId'):
        patientId = request.args['patientId']
        patient = Patient.get_patient_by_id(patientId)
        resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, patient.__dict__)
        if patient is None:
            return jsonify(resultStatus.__dict__)
        resultStatus.data = dataChangeService.get_patient(patient)
        return jsonify(resultStatus.__dict__)
    return jsonify(SUCCESS.__dict__)


@front.route('/pathlogy/list.json')
def pathlogy_list():
    if hasattr(request.args, 'patientId'):
        patientId = request.args['patientId']
        pathlogys = Pathology.getByPatientId(patientId)
        if pathlogys is None or len(pathlogys) < 1:
            return jsonify(rs.SUCCESS.__dict__, ensure_ascii=False)
        patientsDict = object2dict.objects2dicts(pathlogys)
        resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, patientsDict)
        return jsonify(resultStatus.__dict__, ensure_ascii=False)
    return jsonify(SUCCESS.__dict__)


@front.route('/pathlogy/dicominfo.json')
def get_pathology():
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

