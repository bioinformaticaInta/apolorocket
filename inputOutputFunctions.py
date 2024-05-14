#!/usr/bin/python

from Bio import SeqIO
import json
import random
import string

import apoloRocket.Sirna as Sirna
import apoloRocket.TargetSequence as TargetSequence
import apoloRocket.constants as constants

def getRandomName():
    return ''.join(random.sample(string.ascii_lowercase, 20))

def createJsonFile(data, jsonFileName:str)->None:
    jsonFile = open(jsonFileName, "w")
    json.dump(data, jsonFile, indent=4, default=str)
    jsonFile.close()

def readJsonFile(jsonFile:str):
    jsonInput = open(jsonFile)
    jsonData = json.load(jsonInput)
    jsonInput.close()
    return jsonData

def createQueryFile(inputData:dict, queryFileName:str)->dict:
    queryFile = open(queryFileName, 'w')
    queryFile.write('>' + inputData["queryName"]+ '\n')
    queryFile.write(inputData["querySequence"] + '\n')
    queryFile.close()

def createSirnas(inputData:dict, sirnaFastaFileName:str=None)->dict:
    #Create all siRNA's of size "self.sirnaSize" of a sequence.
    # Slice over sequence and split into xmers.
    sirnaData = {}
    if sirnaFastaFileName: sirnaFastaFile = open(sirnaFastaFileName, 'w')
    start = constants.STARTPOSITION
    querySequence = inputData["querySequence"]
    sirnaSize = inputData["sirnaSize"]
    for start in range(start , len(querySequence)-sirnaSize+1):
        sequence = querySequence[start:start+sirnaSize]
        sequence.upper()
        #Add Sirna object to sirnaData dict
        sirnaData[start+1] = Sirna.Sirna(sequence)
        #Write sirna sequence to multifasta file for bowtie
        if sirnaFastaFileName:
            sirnaFastaFile.write('>' + str(start+1) + '\n')
            sirnaFastaFile.write(sequence + '\n')
    if sirnaFastaFileName: sirnaFastaFile.close()
    return sirnaData