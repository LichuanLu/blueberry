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



def save_pdf(pdf_data,file,diagnoseId,fileName):
    default.DEFAULT_FONT["helvetica"]="msyh"
    fontFile = os.path.join( constant.DirConstant.ROOT_DIR+ '/DoctorSpring/static/font', 'msyh.ttf')
    pdfmetrics.registerFont(TTFont('msyh',fontFile))
    # from xhtml2pdf.pisa.sx.pisa3 import pisa_default
    pdf = pisa.pisaDocument(StringIO(
        pdf_data.encode("UTF-8")), file,encoding='utf-8')
    upload_pdf(fileName,diagnoseId)
def upload_pdf(fileName,diagnoseId):
      oss_util.uploadFile(diagnoseId,fileName)


# def fetch_resources(uri, rel):
#     path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
#     return path


