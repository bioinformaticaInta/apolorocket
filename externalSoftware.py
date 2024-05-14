#!/usr/bin/python

import subprocess
import os
import shutil
import glob

import apoloRocket.annotationFunctions as annotationFunctions
import apoloRocket.inputOutputFunctions as inputOutputFunctions
import apoloRocket.TargetSequence as TargetSequence
import apoloRocket.constants as constants

def baseDirFromInputData(inputData:dict)->str:
    refType = "genome" if inputData["genomic"] else "transcriptome"
    baseDir = f"{constants.REFERENCEDIR}/{inputData['genus']}/{inputData['specie']}/{refType}/{inputData['version']}"
    return baseDir, refType

def createBowtieIndexes(inputData:dict)->str:
    bowtieIndexDir,refType = baseDirFromInputData(inputData)
    if not os.path.exists(bowtieIndexDir): os.makedirs(bowtieIndexDir)
    bowtieIndex = f"{bowtieIndexDir}/reference.fasta"
    shutil.copyfile(inputData["referenceFile"],bowtieIndex)
    process = subprocess.Popen(["bowtie-build", bowtieIndex, bowtieIndex])
    process.wait()
    if not os.path.exists(bowtieIndex+".rev.2.ebwt"):
        bowtieIndex = None
    return bowtieIndex

def referenceLenghts(referenceData:dict)->dict:
    refLenghts = {}
    bowtieDBDir,refType = baseDirFromInputData(referenceData)
    bowtieDB = f"{bowtieDBDir}/reference.fasta"
    process = subprocess.Popen(["bowtie-inspect", "-s", bowtieDB], stdout=subprocess.PIPE)
    out,err = process.communicate()
    if not process.returncode:
        out = str(out)
        for line in out.split('\\n'):
            if "Sequence" in line:
                line = line.split('\\t')
                refLenghts[line[1].split(" ")[0]] = int(line[2])
    return refLenghts

def runBowtie(referenceData:dict, inputData:dict, sirnaData:dict, sirnaFastaFileName)->dict:
    allTargets = {}
    bowtieDBDir,refType = baseDirFromInputData(referenceData)
    bowtieDB = f"{bowtieDBDir}/reference.fasta"
    bowtieOutFile = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.bowtiehit"
    process = subprocess.Popen(["bowtie", "-a", "-l", str(inputData["sirnaSize"]), "-n", str(inputData["missmatches"]), 
                                "-y", "-x", bowtieDB, "-f", sirnaFastaFileName, bowtieOutFile])
    process.wait()
    if os.path.exists(bowtieOutFile):
        allTargets = loadBowtieData(inputData, referenceData, bowtieOutFile, sirnaData)
        os.remove(bowtieOutFile)
    return allTargets

def loadBowtieData(inputData:dict, referenceData:dict, bowtieFileName:str, sirnaData:dict)->dict:
    #Load list with all alignments information contains: [sirnaName, hitTarget, hitPos, hitStrand, hitMissmatches]
    allTargets = {}
    refLenghts = referenceLenghts(referenceData)
    bowtieAlignments, targetsRegions = bowtieToList(referenceData, refLenghts, bowtieFileName)
    #Take the targets per regions defined with alignment overlaps
    if bowtieAlignments:
        if inputData["targetsInRegions"]:
            #Add the positions of the region for each alignment in the reference
            targetsRegions = addTargetsRegions(bowtieAlignments, inputData["maxGapSize"], inputData["sirnaSize"])
        #Add annotation from gff file
        if referenceData["annotation"]:
            annotationDir, refType = baseDirFromInputData(referenceData)            
            annotationFile = f"{annotationDir}/annotation.json"
            annotationFunctions.addAnnotations(annotationFile, bowtieAlignments, referenceData["genomic"], 
                                                inputData["targetsInRegions"], targetsRegions)
        #Load bowtie alignments for each Sirna
        countedSirnas = set()
        for alignment in bowtieAlignments:
            sirnaName = alignment[0]
            hitTarget = alignment[1]
            sirnaData[sirnaName].addBowtieAlignment(*alignment[1:])
            #Count number of hits for each target only one time for each
            if hitTarget not in allTargets:
                allTargets[hitTarget] = 1
            elif (sirnaName,hitTarget) not in countedSirnas:
                allTargets[hitTarget] += 1
            countedSirnas.add((sirnaName,hitTarget))
    return allTargets

def bowtieToList(refData:dict, refLenghts:dict, bowtieFileName:str)->tuple[list,dict]:
    bowtieFile = open(bowtieFileName)
    bowtieAlignments = []                                                                                                              
    targetsRegions = {}
    for bowtieMatch in bowtieFile:
        bowtieMatch = bowtieMatch.strip().split('\t')                                                                                  
        sirnaName = int(bowtieMatch[0])
        hitStrand = bowtieMatch[1]
        hitTarget = TargetSequence.TargetSequence(refData["id"], refData["genus"], refData["specie"], 
                                                refData["genomic"], refData["version"], bowtieMatch[2])
        hitTarget.setRegion(1,refLenghts[bowtieMatch[2]])
        hitPos = int(bowtieMatch[3])+1
        hitMissmatches = 0
        if len(bowtieMatch) == 8:
            hitMissmatches = int(bowtieMatch[7])
        bowtieAlignments.append([sirnaName, hitTarget, hitPos, hitStrand, hitMissmatches])
        targetsRegions[bowtieMatch[2]] = [[1,refLenghts[bowtieMatch[2]]]]
    bowtieFile.close()
    return bowtieAlignments,targetsRegions

def addTargetsRegions(bowtieAlignments:list, gapSize:int, xmer:int)->dict:
    #The input is a list of lists containing: [sirna, hitTarget, hitPos, hitStrand, hitMissmatches]
    targetsRegions = {}
    #Traversing ordered by hit positions assembling the regions shared between matches
    for alignment in sorted(bowtieAlignments, key =lambda x: x[2]):
        start = alignment[2]
        end = start + xmer-1
        hitTarget = alignment[1]
        if not hitTarget.getSeqName() in targetsRegions:
            targetsRegions[hitTarget.getSeqName()] = [[start,end]]
        else:
            #if any region exists, search the possible overlap
            regions = targetsRegions[hitTarget.getSeqName()]
            posRegion = 0
            prevRegion = False
            while not prevRegion and posRegion < len(regions):
                region = regions[posRegion]
                if region[0] <= start <= region[1] or (start-region[1]) <= gapSize: #overlap!!!
                    #Change the end of the region for the new end (extend) and set the flag
                    region[1] = end
                    prevRegion = True
                posRegion += 1
            if not prevRegion: #Insert new regions if not overlaping
                regions.append([start,end])
    #Add position of the region to each hit name
    for alignment in bowtieAlignments:
        hitTarget = alignment[1]
        regions = targetsRegions[hitTarget.getSeqName()]
        for region in regions:
            if region[0] <= alignment[2] <= region[1]:
                hitTarget.setRegion(*region)
    return targetsRegions

def runRnaplfold(inputData:dict, sirnaData:dict, queryFileName:str)->None:
    querySequence = open(queryFileName, 'r').read()
    rnaplfoldDir = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}_RNAplfold"
    if not os.path.exists(rnaplfoldDir): os.makedirs(rnaplfoldDir)
    prc_stdout = subprocess.PIPE
    prc = subprocess.Popen(['RNAplfold', '-W', '%d'%constants.WINSIZE,'-L', '%d'% constants.SPAN, '-u', 
                            '%d'%inputData["sirnaSize"], '-T', '%.2f'%constants.TEMPERATURE], 
                            stdin=subprocess.PIPE, stdout=prc_stdout, cwd=rnaplfoldDir)
    prc.stdin.write(querySequence.encode('utf-8'))
    prc.stdin.write('\n'.encode('utf-8'))
    prc.communicate()

    lunpFileName = glob.glob(f"{rnaplfoldDir}/*lunp")
    if lunpFileName:
        loadRnaplfoldData(lunpFileName[0], inputData["sirnaSize"], sirnaData)
    shutil.rmtree(rnaplfoldDir)

def loadRnaplfoldData(lunpFileName:str, sirnaSize:int, sirnaData:dict)->None:
    lunpFile = open(lunpFileName)
    for lunpLine in lunpFile:
        if "#" not in lunpLine:
            lunpLine = lunpLine[:-1].split("\t")
            end = int(lunpLine[0])
            if end >= sirnaSize:
                sirnaName = end-sirnaSize+1
                sirnaData[sirnaName].addRnaplfoldData(lunpLine[1:])

def calculateAllSirnasEfficiency(inputData:dict, sirnaData:dict)->None:
    for sirnaName in sirnaData:
        sirna = sirnaData[sirnaName]
        if sirnaName < 3:
            sequenceN2 = None
        else:
            sequenceN2 = sirnaData[sirnaName-2].getSequence()
        sirna.calculateEfficiency(sequenceN2, inputData["accessibilityWindow"], inputData["tsAccessibilityTreshold"], 
                                inputData["endStabilityTreshold"], constants.STARTPOSITION, constants.ENDNUCLEOTIDES, 
                                constants.OVERHANG, inputData["terminalCheck"], inputData["strandCheck"], inputData["endCheck"], 
                                inputData["accessibilityCheck"])
