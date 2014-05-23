# coding: utf-8
__author__ = 'Jeremy'

import os.path
from flask import request, redirect, url_for, Blueprint, jsonify, g, send_from_directory
from flask import abort, render_template, flash
from DoctorSpring.models import Doctor, User, Department
from  database import db_session
from werkzeug.utils import secure_filename
#from flask.ext.storage import get_default_storage_class
#from flask.ext.uploads import delete, init, save, Upload
import config


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
    for t in doctors:
        count += 1
        user = db_session.query(User).filter(t.userId == User.id).first()
        res_dict['id'] = user.id
        res_dict['name'] = t.username
        res_dict['title'] = t.title
        department = db_session.query(Department).filter(t.departmentId == Department.id).first()
        res_dict['department'] = department.description
        res_dict['image'] = '/static/assets/image/9-small.jpg'
        res_dict['count'] = 'image' + str(count)
        res_list.append(res_dict)


    return render_template("home.html", result = res_list)

@front.route('/applyDiagnose', methods=['GET', 'POST'])
def applyDiagnose():
    return render_template("applyDiagnose.html")


@front.route('/save/diagnose/<formid>', methods=['GET', 'POST'])
def applyDiagnoseForm(formid):
    if (formid == 1) :
        return jsonify({'code': 0,  'message' : "success", 'data': {'formId': 2}})
    elif (formid == 2) :
        return jsonify({'code': 0,  'message' : "success", 'data': {'formId': 3}})
    elif (formid == 3) :
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
