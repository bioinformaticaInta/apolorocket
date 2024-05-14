#!/usr/bin/python

import os
import datetime

import apoloRocket.databaseFunctions as databaseFunctions
import apoloRocket.annotationFunctions as annotationFunctions
import apoloRocket.inputOutputFunctions as inputOutputFunctions
import apoloRocket.figuresFunctions as figureFunctions
import apoloRocket.externalSoftware as externalSoftware

############################################################################
def getTableInformationFile(tableName:str, onlyFirst:bool, outputDir:str, *columns, **constraints)->tuple:
    jsonFileName = f"{outputDir}/{inputOutputFunctions.getRandomName()}.json"
    data = databaseFunctions.getTableData(tableName, *columns, **constraints)
    if onlyFirst:
        data = data[0] if data else {}
    inputOutputFunctions.createJsonFile(data, jsonFileName)
    return (jsonFileName,)
############################################################################

############################################################################
def getAllProjectsInformation(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    return getTableInformationFile("project", False, inputData["outputDir"])
############################################################################

############################################################################
def getAllReferencesInformation(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    return getTableInformationFile("reference", False, inputData["outputDir"])
############################################################################

############################################################################
def getAllQueriesInformation(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    return getTableInformationFile("query", False, inputData["outputDir"])
############################################################################

############################################################################
def getProjectInformation(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #projectID:int -> id of project in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    return getTableInformationFile("project", True, inputData["outputDir"],
                                                    id=inputData["projectID"])
############################################################################

############################################################################
def getReferenceInformation(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #referenceID:int -> id of reference in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    return getTableInformationFile("reference", True, inputData["outputDir"],
                                                    id=inputData["referenceID"])
############################################################################

############################################################################
def getQueryInformation(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #queryID:int -> id of query in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    return getTableInformationFile("query", True, inputData["outputDir"],
                                                id=inputData["queryID"])
############################################################################

############################################################################
def getProjectComparisons(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #projectID:int -> id of the project in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    jsonFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.json"
    maintargetsData = {"maintargetComparisonID": databaseFunctions.getMaintargetComparisons(inputData["projectID"])}
    offtargetsData = {"offtargetComparisonID": databaseFunctions.getOfftargetComparisons(inputData["projectID"])}
    inputOutputFunctions.createJsonFile([maintargetsData, offtargetsData], jsonFileName)
    return (jsonFileName,)
############################################################################

############################################################################
def getQueryProjects(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #queryID:int -> id of the query in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    jsonFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.json"
    queryProjectsData = databaseFunctions.getQueryProjectsInformation(inputData["queryID"])
    inputOutputFunctions.createJsonFile(queryProjectsData, jsonFileName)
    return (jsonFileName,)
############################################################################

############################################################################
def getReferenceProjects(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #referenceID:int -> id of the reference in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    jsonFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.json"
    referenceProjectsData = databaseFunctions.getReferenceProjectsInformation(inputData["referenceID"])
    inputOutputFunctions.createJsonFile(referenceProjectsData, jsonFileName)
    return (jsonFileName,)
############################################################################

############################################################################
def createNewProject(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #name:str -> Project name
        #description:str -> Project description
        #genus:str -> Genus name
        #specie:str -> Specie name
        #user_name:str -> Name main user of the project
        #outputDir:str -> Output directory complete path
    ########################################################################
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    inputData["initial_date"] = datetime.datetime.today()
    inputData["last_modification_date"] = datetime.datetime.today()
    outputDir = inputData.pop("outputDir")
    try:
        projectID = databaseFunctions.insertTableData("project", **inputData)
    except:
        projectID = None
    jsonFileName = f"{outputDir}/{inputOutputFunctions.getRandomName()}.json"
    inputOutputFunctions.createJsonFile({"projectID":projectID}, jsonFileName)
    return (jsonFileName,)
############################################################################

############################################################################
def createNewReference(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #genus:str -> genus name
        #specie:str -> Specie name
        #version:str -> Reference version
        #genomic:bool -> true if the reference is a genome
        #referenceFile:str -> Reference file name complete path
        #annotationFile:str -> Annotation file name complete path or null if no annotation
    ########################################################################
    indexName = annotationFile = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    ########################################################################
    # Step 1: Create Bowtie indexes
    refID = databaseFunctions.getTableData("reference", "id", genus = inputData["genus"], 
                                                            specie = inputData["specie"],
                                                            version = inputData["version"],
                                                            genomic = inputData["genomic"])
    if not refID:
        try:
            indexName = externalSoftware.createBowtieIndexes(inputData)
        except:
            raise Exception("Error running bowtie-build")
        if indexName:
            refID = databaseFunctions.insertTableData("reference", genus = inputData["genus"], 
                                                                    specie = inputData["specie"],
                                                                    version = inputData["version"],
                                                                    genomic = inputData["genomic"])
        ########################################################################
        # Step 2: Parse and create annotation files
        if indexName and inputData["annotationFile"]:
            try:
                annotationFile = annotationFunctions.createAnnotationFile(inputData)
            except:
                raise Exception("Error parsing GFF3 file")
            databaseFunctions.updateColumnTableData("reference", "annotation", True, id = refID)
    ########################################################################
    return (indexName, annotationFile)
############################################################################

############################################################################
def addNewAnnotationToReference(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #referenceID:int -> id value of reference in database
        #annotationFile:str -> Annotation file name complete path
    ########################################################################
    annotationFile = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    refData = databaseFunctions.getTableData("reference", id=inputData['referenceID'])[0]
    inputData['genus'] = refData['genus']
    inputData['specie'] = refData['specie']
    inputData['version'] = refData['version']
    inputData['genomic'] = refData['genomic']
    ########################################################################
    # Step 1: Parse and create annotation files
    try:
        annotationFile = annotationFunctions.createAnnotationFile(inputData)
    except:
        raise Exception("Error parsing GFF3 file")
    databaseFunctions.updateColumnTableData("reference", "annotation", True, id = inputData["referenceID"])
    ########################################################################
    return (annotationFile,)
############################################################################

############################################################################
def getMaintargetsPlot(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #projectID:int -> ID of the project in database
        #sirnaSize:int -> siRNA size
        #missmatches:int -> Allowed mismatches (can be 0-3)
        #targetsInRegions:bool -> True to take targets separated by regions
        #maxGapSize:int -> Maximum number of gap to join 2 regions
        #queryGenus:str -> Genus of query sequence
        #querySpecie:str -> Specie of query sequence
        #querySequenceName:str -> Name of query sequence
        #querySequence:str -> Query sequence
        #pageSize:int -> Number of rows by page, null for all table in one page
        #referenceIDs:list[int] -> List references ID in "reference" DB table
        #outputDir:str -> Output directory complete path
    ########################################################################
    jsonPageFileName = htmlFigureFileName = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    inputData["queryName"] = f"{inputData['queryGenus']}_{inputData['querySpecie']}_{inputData['querySequenceName']}"
    if inputData["targetsInRegions"] and not inputData["maxGapSize"]: inputData["maxGapSize"] = len(inputData["querySequence"])
    ########################################################################
    # Step 1: Create sirna File and dict
    sirnaFastaFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.sirna.fasta"
    sirnaData = inputOutputFunctions.createSirnas(inputData, sirnaFastaFileName)
    ########################################################################
    # Step 2: Run BOWTIE against DB
    allTargets = {}
    for referenceID in inputData["referenceIDs"]:
        referenceData = databaseFunctions.getTableData("reference", id=referenceID)[0]
        try:
            referenceTargets = externalSoftware.runBowtie(referenceData, inputData, sirnaData, sirnaFastaFileName)
        except:
            raise Exception(f"Error running Bowtie on reference id {referenceID}")
        allTargets |= referenceTargets
    os.remove(sirnaFastaFileName)
    databaseFunctions.insertQueryMaintargetInformation(inputData)
    ########################################################################
    # Step 3: Create alignment figure
    if allTargets:
        randomPrefix = inputOutputFunctions.getRandomName()
        htmlFigureFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.figure.html"
        jsonPageFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.tablepage.json"
        blocksInTargets = figureFunctions.getBlocksInTargets(inputData, sirnaData)
        figureFunctions.mainTargetsFigure(blocksInTargets, htmlFigureFileName)
        inputOutputFunctions.createJsonFile({"totalTargets":len(blocksInTargets), 
                                            "pageNumber":1,"pageSize":inputData["pageSize"],
                                            "maintargetComparisonID":inputData["maintargetComparisonID"],
                                            "outputDir":inputData["outputDir"]}, jsonPageFileName)
        databaseFunctions.insertBlocksInMaintargetsInformation(inputData, blocksInTargets)
    ########################################################################
    return (htmlFigureFileName, jsonPageFileName)
############################################################################

############################################################################
def getMaintargetsPlotFromDB(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #pageSize:int -> Number of rows by page, null for all table in one page
        #maintargetComparisonID:int -> Maintarget comparison ID in DB
        #outputDir:str -> Output directory complete path
    ########################################################################
    htmlFigureFileName = jsonPageFileName = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    blocksInTargets = databaseFunctions.getBlocksInMaintargetsInformation(inputData["maintargetComparisonID"])
    if blocksInTargets:
        randomPrefix = inputOutputFunctions.getRandomName()
        htmlFigureFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.figure.html"
        jsonPageFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.tablepage.json"
        figureFunctions.mainTargetsFigure(blocksInTargets, htmlFigureFileName)
        inputOutputFunctions.createJsonFile({"totalTargets":len(blocksInTargets), 
                                            "pageNumber":1,"pageSize":inputData["pageSize"],
                                            "maintargetComparisonID":inputData["maintargetComparisonID"],
                                            "outputDir":inputData["outputDir"]}, jsonPageFileName)
    ########################################################################
    return (htmlFigureFileName, jsonPageFileName)
############################################################################

############################################################################
def getEfficiencyPlot(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #sirnaSize:int -> siRNA size
        #strandCheck:bool -> Strand selection is enabled or disabled
        #endCheck:bool -> End stability selection is enabled or disabled
        #accessibilityCheck:bool -> Target site accessibility is enabled or disabled
        #accessibilityWindow:int -> Accessibility window
        #endStabilityTreshold:float -> End stability treshold
        #tsAccessibilityTreshold:float -> Target site accessibility threshold
        #terminalCheck:bool
        #method:str -> Method to calculate efficiency ('sifi21' or 'IA')
        #pageSize:int -> Number of rows by page, null for all table in one page
        #maintargetComparisonID:int -> Maintarget_comparison_id value in DB
        #maintargetNumbers:list[int] -> List with main targets regions numbers
        #outputDir:str -> Output directory path
    ########################################################################
    htmlFigureFileName = jsonPageFileName = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    databaseFunctions.getQueryEfficiencyInformation(inputData)
    ########################################################################
    if not inputData["efficiencyData"]:
        # Step 1: Calculate efficiency
        queryFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.query.fasta"
        inputOutputFunctions.createQueryFile(inputData, queryFileName)
        sirnaData = inputOutputFunctions.createSirnas(inputData)
        try:
            externalSoftware.runRnaplfold(inputData, sirnaData, queryFileName)
            externalSoftware.calculateAllSirnasEfficiency(inputData, sirnaData)
            inputData["efficiencyData"] = figureFunctions.efficiencyDataForFigure(inputData, sirnaData)
            databaseFunctions.insertQueryEfficiencyInformation(inputData)
        except:
            raise Exception("Error running Rnaplfold and calculate efficiency")
        os.remove(queryFileName)
    ########################################################################
    # Step 2: Create efficiency figure
    if inputData["efficiencyData"]:
        randomPrefix = inputOutputFunctions.getRandomName()
        htmlFigureFileName = f"{inputData['outputDir']}/{randomPrefix}.efficiency.figure.html"
        jsonPageFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.tablepage.json"
        blocksInTargets = databaseFunctions.getBlocksInMaintargetsInformation(inputData["maintargetComparisonID"])
        figureFunctions.efficiencyFigure(inputData["efficiencyData"], blocksInTargets, htmlFigureFileName)
        inputOutputFunctions.createJsonFile({"totalTargets":len(blocksInTargets), 
                                            "pageNumber":1,"pageSize":inputData["pageSize"],
                                            "maintargetComparisonID":inputData["maintargetComparisonID"],
                                            "outputDir":inputData["outputDir"]}, jsonPageFileName)
    ########################################################################
    return (htmlFigureFileName, jsonPageFileName)
############################################################################

############################################################################
def getEfficiencyPlotFromDB(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #method:str -> Method to calculate efficiency ('sifi21' or 'IA')
        #pageSize:int -> Number of rows by page, null for all table in one page
        #maintargetComparisonID:int -> Maintarget_comparison_id value in DB
        #outputDir:str -> Output directory path
    ########################################################################
    htmlFigureFileName = jsonPageFileName = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    databaseFunctions.getQueryEfficiencyInformation(inputData)
    blocksInTargets = databaseFunctions.getBlocksInMaintargetsInformation(inputData["maintargetComparisonID"])
    if inputData["efficiencyData"]:
        randomPrefix = inputOutputFunctions.getRandomName()
        htmlFigureFileName = f"{inputData['outputDir']}/{randomPrefix}.efficiency.figure.html"
        jsonPageFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.tablepage.json"
        figureFunctions.efficiencyFigure(inputData["efficiencyData"], blocksInTargets, htmlFigureFileName)
        inputOutputFunctions.createJsonFile({"totalTargets":len(blocksInTargets), 
                                            "pageNumber":1,"pageSize":inputData["pageSize"],
                                            "maintargetComparisonID":inputData["maintargetComparisonID"],
                                            "outputDir":inputData["outputDir"]}, jsonPageFileName)
    ########################################################################
    return (htmlFigureFileName, jsonPageFileName)
############################################################################

############################################################################
def getOfftargetsPlot(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #projectID:int -> ID of the project in database
        #sirnaSize:int -> siRNA size
        #missmatches:int -> Allowed mismatches (can be 0-3)
        #targetsInRegions:bool -> True to take targets separated by regions
        #maxGapSize:int -> Maximum number of gap to join 2 regions
        #queryID:int -> Query id in DB
        #queryRegionStart:int -> Start on query (interbase)
        #queryRegionEnd:int -> End on query (interbase)
        #pageSize:int -> Page number for table pagination
        #referenceIDs:list[int] -> List references ID in "reference" DB table
        #outputDir:str -> Output directory path
    ########################################################################
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    databaseFunctions.getQueryOfftargetsInformation(inputData)
    if inputData["targetsInRegions"] and not inputData["maxGapSize"]: inputData["maxGapSize"] = len(inputData["querySequence"])
    sirnaFastaFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.sirna.fasta"
    inputOutputFunctions.createSirnas(inputData, sirnaFastaFileName)
    ########################################################################
    htmlFileNames = []
    for referenceID in inputData["referenceIDs"]:
        htmlFigureFileName = None
        # Step 1: Create sirna File and dict
        referenceData = databaseFunctions.getTableData("reference", id=referenceID)[0]
        sirnaData = inputOutputFunctions.createSirnas(inputData)
        ########################################################################
        # Step 2: Run BOWTIE against DB
        allTargets = {}
        try:
            allTargets = externalSoftware.runBowtie(referenceData, inputData, sirnaData, sirnaFastaFileName)
        except:
            raise Exception(f"Error running Bowtie on reference id {referenceID}")
        databaseFunctions.insertQueryOfftargetInformation(inputData, referenceID)
        ########################################################################
        # Step 3: Create alignment figure and obtain data to table 
        if allTargets:
            randomPrefix = inputOutputFunctions.getRandomName()
            htmlFigureFileName = f"{inputData['outputDir']}/{randomPrefix}.offTargets.figure.html"
            blocksInTargets = figureFunctions.getBlocksInTargets(inputData, sirnaData)
            figureFunctions.offTargetsFigure(blocksInTargets, htmlFigureFileName)
            databaseFunctions.insertBlocksInOfftargetsInformation(inputData, blocksInTargets)
        htmlFileNames.append((htmlFigureFileName,))
    os.remove(sirnaFastaFileName)
    ########################################################################
    return tuple(htmlFileNames)
############################################################################

############################################################################
def getOfftargetsPlotFromDB(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #pageSize:int -> Number of rows by page, null for all table in one page
        #offtargetComparisonID:int -> Offtarget comparison ID in DB 
        #outputDir:str -> Output directory complete path
    ########################################################################
    htmlFigureFileName = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    blocksInTargets = databaseFunctions.getBlocksInOfftargetsInformation(inputData["offtargetComparisonID"])
    if blocksInTargets:
        htmlFigureFileName = f"{inputData['outputDir']}/{inputOutputFunctions.getRandomName()}.offTargets.figure.html"
        figureFunctions.offTargetsFigure(blocksInTargets, htmlFigureFileName)
    ########################################################################
    return (htmlFigureFileName,)
############################################################################

############################################################################
def getTargetsTable(inputJsonFile:str)->tuple:
    ########################################################################
    #inputJsonFile
        #totalTargets -> Target regions total number
        #pageNumber -> Page number for table pagination
        #pageSize -> Number of rows by page, null for all table in one page
        #maintargetComparisonID -> Maintarget_comparison_id value in DB
        #outputDir -> Output directory path
    ########################################################################
    jsonTableFileName = None
    #Parsing Input Files
    inputData = inputOutputFunctions.readJsonFile(inputJsonFile)
    ########################################################################
    # Step 1: Create data to table file
    blocksInTargets = databaseFunctions.getBlocksInMaintargetsInformation(inputData["maintargetComparisonID"], 
                                                                        inputData["pageSize"], 
                                                                        inputData["pageNumber"])
    if blocksInTargets:
        randomPrefix = inputOutputFunctions.getRandomName()
        jsonTableFileName = f"{inputData['outputDir']}/{randomPrefix}.mainTargets.table.json"
        targetsTable = figureFunctions.getTargetsTableData(blocksInTargets)
        inputOutputFunctions.createJsonFile(targetsTable, jsonTableFileName)
    ########################################################################
    return (jsonTableFileName,)
############################################################################