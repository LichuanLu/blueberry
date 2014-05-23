# coding: utf-8
__author__ = 'chengc017'

def userCenterDiagnoses(diagnoses):
    if diagnoses is None or len(diagnoses)<1:
        return
    result=[]
    for diagnose in diagnoses:
        diagDict={}
        if hasattr(diagnose,"patient") and diagnose.patient:
            diagDict['patientName']=diagnose.patient.name
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
        print diagDict['doctorName'],diagDict['positons']
        result.append(diagDict)

    return result


