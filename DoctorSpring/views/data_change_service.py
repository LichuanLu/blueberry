# coding: utf-8
__author__ = 'chengc017'
from DoctorSpring.util import constant
from DoctorSpring.models import File ,Diagnose,User

def userCenterDiagnoses(diagnoses):
    if diagnoses is None or len(diagnoses)<1:
        return
    result=[]
    for diagnose in diagnoses:
        diagDict={}

        if hasattr(diagnose,"patient") and diagnose.patient:
            diagDict['patientName']=diagnose.patient.realname
        if hasattr(diagnose,"doctor") and diagnose.doctor:
            diagDict['doctorName']=diagnose.doctor.username
        if hasattr(diagnose,"hospital") and diagnose.hospital:
            diagDict['hispital']=diagnose.hospital.name

        if diagnose.createDate:
            diagDict["date"]=diagnose.createDate.strftime('%Y-%m-%d')
        if diagnose.id:
            diagDict['id']=diagnose.id
        if diagnose.diagnoseSeriesNumber:
            diagDict['diagnosenumber']=diagnose.diagnoseSeriesNumber
        if diagnose.status or diagnose.status==0:
            diagDict['statusId']=diagnose.status
            diagDict['status']=constant.DiagnoseStatus.getStatusName(diagnose.status)
        if diagnose.pathologyId:
            diagDict['dicomUrl']=File.getDicomFileUrl(diagnose.pathologyId)


        if hasattr(diagnose,"pathology") and diagnose.pathology:
            pathology=diagnose.pathology
            if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
                pathologyPositons=pathology.pathologyPostions
                if pathologyPositons and len(pathologyPositons)>0:
                    positions=u''
                    for pathologyPositon in pathologyPositons:
                        position=pathologyPositon.position
                        positions+=(u' '+position.name)
                    diagDict['positionName']=positions
        #print diagDict['doctorName'],diagDict['positons']
        result.append(diagDict)

    return result
def getDiagnoseDetailInfo(diagnose):
    if diagnose is None:
        return
    diagDict={}
    diagDict['id']=diagnose.id
    if hasattr(diagnose,"patient") and diagnose.patient:
        diagDict['patientName']=diagnose.patient.realname
        diagDict['gender']=diagnose.patient.gender
        if diagnose.patient.birthDate:
            diagnose['birthDate']=diagnose.patient.birthDate.strftime('%Y-%m-%d')

    #diagDict['type']=diagnose.type
    if hasattr(diagnose,"doctor") and diagnose.doctor:
        diagDict['doctorName']=diagnose.doctor.username
    if diagnose.createDate:
        diagDict["date"]=diagnose.createDate.strftime('%Y-%m-%d')

    if hasattr(diagnose,"hospital") and diagnose.hospital:
        diagDict['hospitalHistory']=diagnose.hospital.name

    if diagnose.pathologyId:
        diagDict['dicomUrl']=File.getDicomFileUrl(diagnose.pathologyId)

    if diagnose.pathologyId:
        diagDict['docUrl']=File.getFilesUrl(diagnose.pathologyId)


    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        diagDict['caseHistory']=pathology.caseHistory
        diagDict['diagnoseType']=pathology.diagnoseMethod
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    positions+=(u' '+position.name)
                diagDict['positionName']=positions

def getDiagnosePositonFromDiagnose(diagnose):
    if diagnose is None:
        return
    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    positions+=(u' '+position.name)
                return positions

def getDoctorNeedDiagnoseMessageContent(diagnose,doctor):
    content=' 您好，系统中有一个新到的影像需要您来诊断！'
    if doctor.username:
        content=doctor.username+content
    diagnoseContent=u''
    if diagnose.diagnoseSeriesNumber:
        diagnoseContent=" 诊断号:"+diagnose.diagnoseSeriesNumber

    if hasattr(diagnose,"patient") and diagnose.patient:
        if diagnose.patient.name:
            diagnoseContent+=' | 患者:'+diagnose.patient.realname

    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        if pathology.diagnoseMethod:
            diagnoseContent+=' | 诊断类型:'+pathology.diagnoseMethod
    if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
        pathologyPositons=pathology.pathologyPostions
        if pathologyPositons and len(pathologyPositons)>0:
            positions=u''
            for pathologyPositon in pathologyPositons:
                position=pathologyPositon.position
                if position and position.name:
                    positions+=(u' '+position.name)
            diagnoseContent+=' | 诊断部位:'+positions
    content+=diagnoseContent
    return content
def getPatienDiagnoseMessageContent(diagnose,doctor):
    content=' 您好，系统中有一个影像已被处理，请查看处理结果！'
    #content=' 您好，系统中有一个新到的影像需要您来诊断！'
    if diagnose and hasattr(diagnose,'patient') and hasattr(diagnose.patient,'user') and diagnose.patient.user:
        content=diagnose.patient.user.name+content
    diagnoseContent=u''
    if diagnose.diagnoseSeriesNumber:
        diagnoseContent=" 诊断号:"+diagnose.diagnoseSeriesNumber

    if hasattr(diagnose,"patient") and diagnose.patient:
        if diagnose.patient.name:
            diagnoseContent+=' | 患者:'+diagnose.patient.realname

    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        if pathology.diagnoseMethod:
            diagnoseContent+=' | 诊断类型:'+pathology.diagnoseMethod
    if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
        pathologyPositons=pathology.pathologyPostions
        if pathologyPositons and len(pathologyPositons)>0:
            positions=u''
            for pathologyPositon in pathologyPositons:
                position=pathologyPositon.position
                if position and position.name:
                    positions+=(u' '+position.name)
            diagnoseContent+=' | 诊断部位:'+positions
    content+=diagnoseContent
    return content




def setDiagnoseCommentsDetailInfo(diagnoseCommentsDict):
    if diagnoseCommentsDict is None or len(diagnoseCommentsDict)<1:
        return
    for diagnoseComment in diagnoseCommentsDict:
        if diagnoseComment.has_key('observer'):
           observer=diagnoseComment.get('observer')
           user=User.getById(observer)
           if user:
               diagnoseComment['observerName']=user.name
        if diagnoseComment.has_key('receiver'):
            receiver=diagnoseComment.get('receiver')
            user=User.getById(receiver)
            if user:
                diagnoseComment['receiverName']=user.name

        if diagnoseComment.diagnoseId:
            diagnose=Diagnose.getDiagnoseById(diagnoseComment.diagnoseId)
            if diagnose:
                if diagnose.score:
                    diagnoseComment['scoreName']=constant.DiagnoseScore[diagnose.score]
                if diagnose.hospitalId and hasattr(diagnose,'hospital') and diagnose.hospital.name:
                    diagnoseComment['hospitalId']= diagnose.hospitalId
                    diagnoseComment['hospitalName']=diagnose.hospital.name
                if hasattr(diagnose,"pathology") and diagnose.pathology:
                    pathology=diagnose.pathology
                    if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
                        pathologyPositons=pathology.pathologyPostions
                        if pathologyPositons and len(pathologyPositons)>0:
                            positions=u''
                            for pathologyPositon in pathologyPositons:
                                position=pathologyPositon.position
                                positions+=(u' '+position.name)
                            diagnoseComment['positionName']=positions


def setThanksNoteDetail(thanksNoteDicts):
    if thanksNoteDicts and len(thanksNoteDicts)<1:
        return
    for thanksNoteDict in thanksNoteDicts:
        if thanksNoteDict.has_key('sender'):
            observer=thanksNoteDict.get('sender')
            user=User.getById(observer)
            if user:
                thanksNoteDict['observer']=observer
                thanksNoteDict['observerName']=user.name









