# coding: utf-8

__author__ = 'lichuan'

from xhtml2pdf import pisa,default
from cStringIO import StringIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import constant,oss_util
from DoctorSpring.models import Diagnose

from flask import abort, render_template, flash



def save_pdf(pdf_data,file,diagnoseId,fileName):
    default.DEFAULT_FONT["helvetica"]="msyh"
    fontFile = os.path.join( constant.DirConstant.ROOT_DIR+ '/DoctorSpring/static/font', 'msyh.ttf')
    pdfmetrics.registerFont(TTFont('msyh',fontFile))
    # from xhtml2pdf.pisa.sx.pisa3 import pisa_default
    pdf = pisa.pisaDocument(StringIO(
        pdf_data.encode("UTF-8")), file,encoding='utf-8')
    file.close()
    fileUrl=upload_pdf(fileName,diagnoseId)
    return fileUrl
def upload_pdf(fileName,diagnoseId):
      fileUrl=oss_util.uploadFile(diagnoseId,fileName)
      return fileUrl
def generatorPdf(diagnoseId):
    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    report=None
    if hasattr(diagnose,'report'):
        report=diagnose.report
        if diagnose and report and report.type==constant.ReportType.Doctor:
            data={}
            data['techDesc']=report.techDesc
            data['imageDesc']=report.imageDesc
            data['diagnoseDesc']=report.diagnoseDesc
            data['seriesNumber']=report.seriesNumber
            data['fileUrl']=report.fileUrl
            createDate=report.createDate
            if createDate:
                createDate=createDate.strftime('%Y-%m-%d')
                data['createDate']=createDate
            import  DoctorSpring.views.data_change_service as dataChangeService
            postions=dataChangeService.getDiagnosePositonFromDiagnose(diagnose)
            if postions:
                data['postions']=postions
            if hasattr(diagnose,'patient') and diagnose.patient:
                data['gender']=diagnose.patient.gender
                birthDate=diagnose.patient.birthDate
                if birthDate:
                    birthDate=birthDate.strftime('%Y-%m-%d')
                    data['birthDate']=birthDate
                data['name']=diagnose.patient.realname
            if hasattr(diagnose,'doctor'):
                data['doctorName']=diagnose.doctor.username

            html =  render_template('diagnoseResultPdf.html',data=data)
            fileName=constant.DirConstant.DIAGNOSE_PDF_DIR+'test.pdf'
            result = open(fileName, 'wb') # Changed from file to filename

            url = save_pdf(html,result,diagnoseId,fileName)
            result.close()
            # return render_template("testpdf.html",getAvatar=getAvatar)
            return url
    return None



# def fetch_resources(uri, rel):
#     path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
#     return path


