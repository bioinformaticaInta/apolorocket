#!/usr/bin/python

import os
from BCBio import GFF
from BCBio.GFF import GFFExaminer

import apoloRocket.constants as constants
import apoloRocket.inputOutputFunctions as inputOutputFunctions
import apoloRocket.externalSoftware as externalSoftware

#####################################################################################################################
#############################################GFF PARSING#############################################################
#####################################################################################################################

def createAnnotationFile(inputData:dict)->str:
    annotationFileDir, refType = externalSoftware.baseDirFromInputData(inputData)
    if not os.path.exists(annotationFileDir): os.makedirs(annotationFileDir)
    annotationFileName = f"{annotationFileDir}/annotation.json"
    selectedTypes = exploreGFFlevels(inputData["annotationFile"])
    annotDict = getGFFAnnotation(inputData, selectedTypes)
    inputOutputFunctions.createJsonFile(annotDict, annotationFileName)
    return annotationFileName

def exploreGFFlevels(annotationFileName:str)->tuple:
    examiner = GFFExaminer()
    annotationFile = open(annotationFileName)
    allTypes = examiner.parent_child_map(annotationFile) 
    annotationFile.close()
    selectedTypes = set()
    gffStructure = {}
    for sourceAndType in allTypes:
        if sum(map(lambda x: sourceAndType in x, allTypes.values())) == 0: #Type of level one (ie. gene)
            gffStructure[sourceAndType] = {}
            for sonSourceAndType in allTypes[sourceAndType]:
                gffStructure[sourceAndType][sonSourceAndType] = []
                if sonSourceAndType in allTypes:
                    gffStructure[sourceAndType][sonSourceAndType]=allTypes[sonSourceAndType]
    for levelOneFeature in gffStructure:
        selectedTypes.add(levelOneFeature[1])
        for levelTwoFeature in gffStructure[levelOneFeature]:
            if not isLevelThree(gffStructure, levelTwoFeature):
                selectedTypes.add(levelTwoFeature[1])
    return selectedTypes

def isLevelThree(gffStructure:dict, feature:tuple)->bool:
    levelThree = False
    for levelOneFeature in gffStructure:
        for levelTwoFeature in gffStructure[levelOneFeature]:
            for levelThreeFeature in gffStructure[levelOneFeature][levelTwoFeature]:
                if feature[1] == levelThreeFeature[1]:
                    levelThree = True
    return levelThree

def getGFFAnnotation(inputData:dict, selectedTypes:set)->dict:
    annotationFile = open(inputData["annotationFile"])
    annotDict = {}
    for rec in GFF.parse(annotationFile, limit_info={"gff_type":selectedTypes}):
        if not rec.id in annotDict: annotDict[rec.id] = {}
        for feature in rec.features:
            annotDict[rec.id][feature.id] = {"type":feature.type, "start":int(feature.location.start), 
                                            "end":int(feature.location.end), "qualifiers":feature.qualifiers,
                                            "subfeatures":None}
            subfDict = {}
            for subfeature in feature.sub_features:
                subfDict[subfeature.id] = {"type":subfeature.type, "qualifiers":subfeature.qualifiers}
            annotDict[rec.id][feature.id]["subfeatures"] = subfDict
    annotationFile.close()
    return annotDict

#####################################################################################################################
#########################################ANNOTATION FOR PLOTS########################################################
#####################################################################################################################

def addAnnotations(JsonAnnotFile:str, bowtieAlignments:list, genomicRef:bool, inRegions:bool, targetsRegions:dict)->None:
    annotData = inputOutputFunctions.readJsonFile(JsonAnnotFile)
    if genomicRef and inRegions:
        #Add annotations to each region
        #targetRegions is a dictionary with {targetName:[targetRegion1, targetRegion2, etc]}
        #targetRegion1=[startRegion1,endRegion1]
        addGenomicAnnotations(annotData, bowtieAlignments, targetsRegions)
    elif not genomicRef:
        #For transcriptomic references not use regions, only target name
        addTranscriptomicAnnotations(annotData, bowtieAlignments)

def addGenomicAnnotations(annotData:dict, bowtieAlignments:list, targetsRegions:dict)->None:
    targetsAnnotations = {}
    for targetName in targetsRegions:
        for region in targetsRegions[targetName]:
            targetsAnnotations[(targetName, *region)] = []
            if targetName in annotData:
                targetsAnnotations[(targetName, *region)] = getGenomicRegionAnnotation(annotData[targetName], *region)
    #Add annotation for each alignment
    for alignment in bowtieAlignments:
        hitTarget = alignment[1]
        for annotation in targetsAnnotations[(hitTarget.getSeqName(), *hitTarget.getRegion())]:
            hitTarget.addAnnotation(annotation)

def getGenomicRegionAnnotation(annotData:dict, startRegion:int, endRegion:int)->list:
    annotInfo = []
    for featureName in annotData:
        feature = annotData[featureName]
        featureInRegion = None
        #region included in reference feature
        if feature["start"] <= startRegion and  feature["end"] >= endRegion:
            featureInRegion = feature
        #reference feature included in region
        elif feature["start"] > startRegion and  feature["end"] < endRegion:
            featureInRegion = feature
        #Partial end of reference feature at the region start
        elif feature["start"] < startRegion and startRegion < feature["end"] <= endRegion:
            featureInRegion = feature
        #Partial start of reference feature at the region end
        elif startRegion <= feature["start"] < endRegion and  feature["end"] > endRegion:
            featureInRegion = feature
        if featureInRegion:
            annotInfo.append({featureName:featureInRegion})
    return annotInfo

def addTranscriptomicAnnotations(annotData:dict, bowtieAlignments:list)->None:
    #Add annotation for each alignment
    for alignment in bowtieAlignments:
        hitTarget = alignment[1]
        annotInfo = getTranscriptomicAnnotation(annotData, hitTarget.getSeqName())
        if annotInfo:
            hitTarget.addAnnotation(annotInfo)
        
def getTranscriptomicAnnotation(annotData:list, hitName:str)->dict:
    annotInfo = None
    seqNames = tuple(annotData.keys())
    posSeq = 0
    while not annotInfo and posSeq < len(seqNames):
        seqData = annotData[seqNames[posSeq]]
        featureNames = tuple(seqData.keys())
        posFeature = 0
        while not annotInfo and posFeature < len(featureNames):
            featureName = featureNames[posFeature]
            featureData = seqData[featureName]
            if hitName in featureName:
                annotInfo = {featureName:featureData}
            else:
                for subFeature in featureData["subfeatures"]:
                    if hitName in subFeature:
                        annotInfo = {featureName:featureData}
            posFeature += 1
        posSeq += 1
    return annotInfo