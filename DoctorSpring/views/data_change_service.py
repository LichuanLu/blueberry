# coding: utf-8
__author__ = 'chengc017'

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
        if diagnose.createDate:
            diagDict["createDate"]=diagnose.createDate.strftime('%Y-%m-%d')
        if hasattr(diagnose,"pathology") and diagnose.pathology:
            pathology=diagnose.pathology
            if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
                pathologyPositons=pathology.pathologyPostions
                if pathologyPositons and len(pathologyPositons)>0:
                    positions=u''
                    for pathologyPositon in pathologyPositons:
                        position=pathologyPositon.position
                        positions+=(u' '+position.name)
                    diagDict['positons']=positions
        #print diagDict['doctorName'],diagDict['positons']
        result.append(diagDict)

    return result
def getDiagnoseDetailInfo(diagnose):
    if diagnose is None:
        return
    diagDict={}
    if hasattr(diagnose,"patient") and diagnose.patient:
        diagDict['patientName']=diagnose.patient.realname
        diagDict['patientGender']=diagnose.patient.gender
        diagnose['patientBirthDate']=diagnose.patient.birthDate

    #diagDict['type']=diagnose.type
    if hasattr(diagnose,"doctor") and diagnose.doctor:
        diagDict['doctorName']=diagnose.doctor.username
    if diagnose.createDate:
        diagDict["createDate"]=diagnose.createDate.strftime('%Y-%m-%d')

    if hasattr(diagnose,"hospital") and diagnose.hospital:
        diagDict['hospitalName']=diagnose.hospital.name

    if hasattr(diagnose,"pathology") and diagnose.pathology:
        pathology=diagnose.pathology
        diagDict['caseHistory']=pathology.caseHistory
        diagDict['diagnoseMethod']=pathology.diagnoseMethod
        if hasattr(pathology,"pathologyPostions") and pathology.pathologyPostions:
            pathologyPositons=pathology.pathologyPostions
            if pathologyPositons and len(pathologyPositons)>0:
                positions=u''
                for pathologyPositon in pathologyPositons:
                    position=pathologyPositon.position
                    positions+=(u' '+position.name)
                diagDict['positons']=positions

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
    content='您好，系统中有一个新到的影像需要您来诊断！'
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





