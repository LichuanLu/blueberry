# coding: utf-8
__author__ = 'Jeremy'

import os.path
import config
import data_change_service as dataChangeService
from flask import request, redirect, url_for, Blueprint, jsonify, g, send_from_directory, session
from flask import abort, render_template, flash
from flask_login import login_required
from DoctorSpring.models import Doctor, User, Department, Patient, Diagnose, Pathology, PathologyPostion, File2Pathology
from database import db_session
from werkzeug.utils import secure_filename
from forms import DiagnoseForm1, DoctorList, DiagnoseForm2, DiagnoseForm3, DiagnoseForm4
from DoctorSpring.util import result_status as rs, object2dict, constant
from datetime import datetime
from DoctorSpring.util.constant import PatientStatus, Pagger, DiagnoseStatus
from DoctorSpring.util.result_status import *

config = config.rec()
front = Blueprint('front', __name__)

@front.route('/', methods=['GET', 'POST'])
@front.route('/homepage', methods=['GET', 'POST'])
def homepage():
    doctors = db_session.query(Doctor).all()
    res_dict = {}
    res_dict['id'] = ''
    res_dict['name'] = ''
    res_dict['title'] = ''
    res_dict['department'] = ''
    res_dict['image'] = ''
    res_dict['count'] = ''
    res_list = []
    count = 0
    # for t in doctors:
    #     count += 1
    #     user = db_session.query(User).filter(t.userId == User.id).first()
    #     res_dict['id'] = user.id
    #     res_dict['name'] = t.username
    #     res_dict['title'] = t.title
    #     department = db_session.query(Department).filter(t.departmentId == Department.id).first()
    #     res_dict['department'] = department.description
    #     res_dict['image'] = '/static/assets/image/9-small.jpg'
    #     res_dict['count'] = 'image' + str(count)
    #     res_list.append(res_dict)


    return render_template("home.html", result=res_list)

@front.route('/applyDiagnose', methods=['GET', 'POST'])
@login_required
def applyDiagnose():
    new_patient = Patient.get_patient_by_user(session['userId'])
    patientdict = object2dict.objects2dicts(new_patient)

    return render_template("applyDiagnose.html", result=patientdict)


@front.route('/save/diagnose/<formid>', methods=['GET', 'POST'])
@login_required
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
            new_diagnose = Diagnose.getNewDiagnoseByStatus(DiagnoseStatus.Draft, session['userId'])
            if(new_diagnose is not None):
                if(new_diagnose.patientId):
                    new_patient = Patient.get_patient_by_id(new_diagnose.patientId)
                if(new_patient is None):
                    new_patient = Patient()
                new_patient.type = PatientStatus.diagnose
                new_patient.userID = session['userId']
                new_patient.realname = form.patientname
                new_patient.gender = form.patientsex
                new_patient.birthDate = datetime.strptime(form.birthdate, "%Y-%m-%d")
                new_patient.identityCode = form.identitynumber
                new_patient.identityPhone = form.phonenumber
                new_patient.status = PatientStatus.diagnose
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
                new_pathology.save(new_pathology)
                new_diagnose.pathologyId = new_pathology.id
                Diagnose.save(new_diagnose)
                positions = form.patientlocation.split(',')
                for position in positions:
                    if position is not '':
                        new_position_id = PathologyPostion(position, new_pathology.id)
                        PathologyPostion.save(new_position_id)
                fileurls = form.fileurl.split(',')
                for url in fileurls:
                    if url is not '':
                        new_file2pathology = File2Pathology(new_pathology.id, url)
                        File2Pathology.save(new_file2pathology)
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
                    new_pathology.hospticalId = 2
                    Pathology.save(new_pathology)
                else:
                    form_result = ResultStatus(FAILURE.status, "找不到上步的草稿")
            else:
                form_result = ResultStatus(FAILURE.status, "找不到上步的草稿")
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
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    file_size = os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
                    file_url = "/static/tmp/"+filename
                    file_infos.append(dict(name=filename,
                                           size=file_size,
                                           url=file_url))
                else:
                    return jsonify({'code': 1,  'message' : "error", 'data': ''})
            return jsonify(files=file_infos)
    except:
        raise
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
    form = DoctorList(request.form)
    form_result = form.validate()
    if form_result.status == rs.SUCCESS.status:
        pager = Pagger(form.pageNumber, form.pageSize)
        doctors = Doctor.get_doctor_list(form.hospitalId, form.sectionId, form.doctorname, pager)
        if doctors is None or len(doctors) < 1:
            return jsonify(rs.SUCCESS.__dict__, ensure_ascii = False)
        doctorsDict = dataChangeService.get_doctors_dict(doctors, form.pageNumber)
        resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, doctorsDict)
        return jsonify(resultStatus.__dict__, ensure_ascii=False)


@front.route('/doctor/recommanded')
def doctor_rec():
    doctor = Doctor.get_doctor_list(0, 0, '', None, True)
    if doctor is None:
        return jsonify(rs.SUCCESS.__dict__, ensure_ascii = False)
    doctors_dict = dataChangeService.get_doctor(doctor)
    resultStatus = rs.ResultStatus(rs.SUCCESS.status, rs.SUCCESS.msg, doctors_dict)
    return jsonify(resultStatus.__dict__, ensure_ascii=False)


@front.route('/doctor/list')
def doctor_list():
    return render_template("doctorList.html")

