# coding: utf-8
__author__ = 'Jeremy'

import os.path
from flask import request, redirect, url_for, Blueprint, jsonify, g, send_from_directory, session
from flask import abort, render_template, flash
from flask_login import login_required
from DoctorSpring.models import Doctor, User, Department, Patient
from database import db_session
from werkzeug.utils import secure_filename
#from flask.ext.storage import get_default_storage_class
#from flask.ext.uploads import delete, init, save, Upload
import config
from forms import DiagnoseForm1
from DoctorSpring.util import result_status as rs, object2dict, constant
from datetime import datetime
from DoctorSpring.util.constant import PatientStatus



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


    return render_template("home.html", result = res_list)

@front.route('/applyDiagnose', methods=['GET', 'POST'])
@login_required
def applyDiagnose():
    return render_template("applyDiagnose.html")


@front.route('/save/diagnose/<formid>', methods=['GET', 'POST'])
@login_required
def applyDiagnoseForm(formid):
    if (int(formid) == 1) :
        form = DiagnoseForm1(request.form)
        form_result = form.validate()
        if form_result.status == rs.SUCCESS.status:
            new_patient = Patient()
            new_patient.type = PatientStatus.diagnose
            new_patient.userID = session['userId']
            new_patient.realname = form.patientname
            new_patient.gender = form.patientsex
            new_patient.birthDate = datetime.strptime(form.birthdate, "%Y-%m-%d")
            new_patient.identityCode = form.identitynumber
            new_patient.identityPhone = form.phonenumber
            # new_patient.locationId = form.location
            Patient.save(new_patient)
            form_result.data = {'formId': 2}
        # return jsonify(form_result.__dict__)
        return jsonify({'code': 0,  'message' : "success", 'data': {'formId': 2}})
    elif (int(formid) == 2) :
        return jsonify({'code': 0,  'message' : "success", 'data': {'formId': 3}})
    elif (int(formid) == 3) :
        return jsonify({'code': 0,  'message' : "success", 'data': {'formId': 4}})
    else :
        return jsonify({'code': 0,  'message' : "success", 'data': ''})

UPLOAD_FOLDER = 'DoctorSpring/static/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html','zip'])

@front.route('/dicomfile/upload', methods=['POST'])
def upload():
    try:
        if request.method == 'GET':
            file_infos = []
            files = request.files
            for key, file in files.iteritems():
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_size = os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
                    file_url = "http://127.0.0.1:5000/static/tmp/"+filename
                    file_infos.append(dict(name=filename,
                                           size=file_size,
                                           url=file_url))
            return jsonify(files=file_infos)
        if request.method == 'POST':
            file_infos = []
            files = request.files
            for key, file in files.iteritems():
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    file_size = os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
                    file_url = "http://127.0.0.1:5000/static/tmp/"+filename
                    file_infos.append(dict(name=filename,
                                           size=file_size,
                                           url=file_url))
                else:
                    return jsonify({'code': 1,  'message' : "error", 'data': ''})
            return jsonify(files=file_infos)
    except:
        raise
        return jsonify({'code': 1,  'message' : "error", 'data': ''})


def _handleUpload(files):
    if not files:
        return None
    filenames = []
    saved_files_urls = []
    for key, file in files.iteritems():
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print os.path.join(UPLOAD_FOLDER, filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            #saved_files_urls.append(url_for('uploaded_file', filename=filename))
            filenames.append("%s" % (file.filename))
            #print saved_files_urls[0]

    return filenames

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@front.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)
