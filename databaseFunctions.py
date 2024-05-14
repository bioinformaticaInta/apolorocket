#!/usr/bin/python

import psycopg2
import psycopg2.sql as sql
import psycopg2.extras as psextras
import datetime

import apoloRocket.constants as constants
import apoloRocket.TargetSequence as TargetSequence

#######################################CONNECTION DATA##############################################################
####################################################################################################################
def getConnectionDict()->dict:
    return {"database" : constants.DBNAME, 
            "user" : constants.DBUSER, 
            "host" : constants.DBHOST,
            "password" : constants.DBPASSWD,
            "port" : constants.DBPORT,
            "cursor_factory" : psextras.RealDictCursor}

#######################################GET FUNCTIONS################################################################
####################################################################################################################
def getMaintargetComparisons(projectID:int)->dict:
    comparisonsData = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    maintarget_comparison.id as maintarget_comparison_id,
                    query.name as query_name,
                    reference.genus as reference_Genus, reference.specie as reference_specie, 
                    reference.version as reference_version, reference.genomic as reference_genomic  
                FROM
                    maintarget_comparison, maintarget_comparison_reference, query_region, query, reference     
                WHERE
                    maintarget_comparison.project_id = %s and
                    maintarget_comparison_reference.maintarget_comparison_id = maintarget_comparison.id and 
                    query_region.id = maintarget_comparison.query_region_id and
                    query.id = query_region.query_id and 
                    reference.id = maintarget_comparison_reference.reference_id;""",
                (projectID,))
            allComparisons = cur.fetchall()            
    conn.close()
    for comparison in allComparisons:
        maintargetComparisonID = comparison.pop("maintarget_comparison_id")
        if maintargetComparisonID not in comparisonsData: comparisonsData[maintargetComparisonID] = []
        comparisonsData[maintargetComparisonID].append(comparison)
    return comparisonsData

def getOfftargetComparisons(projectID:int)->dict:
    comparisonsData = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    offtarget_comparison.id as offtarget_comparison_id,
                    query.name as query_name, 
                    query_region.start_position as query_region_start, query_region.end_position as query_region_end, 
                    reference.genus as reference_Genus, reference.specie as reference_specie, 
                    reference.version as reference_version, reference.genomic as reference_genomic,  
                    offtarget_comparison.selected_region as query_region_selected
                FROM
                    offtarget_comparison, offtarget_comparison_reference, query_region, query, reference     
                WHERE
                    offtarget_comparison.project_id = %s and
                    offtarget_comparison_reference.offtarget_comparison_id = offtarget_comparison.id and 
                    query_region.id = offtarget_comparison.query_region_id and
                    query.id = query_region.query_id and 
                    reference.id = offtarget_comparison_reference.reference_id;""",
                (projectID,))
            allComparisons = cur.fetchall()            
    conn.close()
    for comparison in allComparisons:
        offtargetComparisonID = comparison.pop("offtarget_comparison_id")
        comparisonsData[offtargetComparisonID] = []
        comparisonsData[offtargetComparisonID].append(comparison)
    return comparisonsData

def getQueryProjectsInformation(queryID:int)->dict:
    projectsData = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    DISTINCT(project.*) 
                FROM
                    maintarget_comparison, query_region, query, project      
                WHERE
                    query.id = %s and 
                    query_region.id = query.id and 
                    maintarget_comparison.query_region_id = query_region.id and
                    project.id = maintarget_comparison.project_id;""",
                (queryID,))
            projectsData = cur.fetchall()            
    conn.close()
    return projectsData

def getReferenceProjectsInformation(referenceID:int)->dict:
    projectsData = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    DISTINCT(project.*) 
                FROM
                    maintarget_comparison, maintarget_comparison_reference, project      
                WHERE
                    maintarget_comparison_reference.reference_id = %s and 
                    maintarget_comparison.id = maintarget_comparison_reference.maintarget_comparison_id and
                    project.id = maintarget_comparison.project_id;""",
                (referenceID,))
            projectsData = cur.fetchall()            
    conn.close()
    return projectsData

def getBlocksInMaintargetsInformation(maintargetComparisonID:int, pageSize:int=None, pageNumber:int=None)->dict:
    blocksInTargets = {}
    startTargetNumber = endTargetNumber = None
    if pageNumber and pageSize:
        startTargetNumber = (pageNumber-1)*pageSize
        endTargetNumber = pageNumber*pageSize
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    maintarget_comparison_reference_region.target_number as tnumber, 
                    maintarget_comparison_reference_region.reference_region_id,
                    maintarget_comparison_reference_region.maintarget as tmaintarget,
                    maintarget_comparison.query_region_id, 
                    reference_region.sequence_name as tname, reference_region.start_position as tstart, 
                    reference_region.end_position as tend, reference_region.annotation as tannotation,
                    reference.id as refid, reference.genus as refgenus, reference.specie as refspecie, 
                    reference.version as refversion, reference.genomic as refgenomic  
                FROM 
                    reference, reference_region, maintarget_comparison, maintarget_comparison_reference, 
                    maintarget_comparison_reference_region 
                WHERE 
                    maintarget_comparison.id = %s and 
                    maintarget_comparison_reference.maintarget_comparison_id = maintarget_comparison.id and 
                    maintarget_comparison_reference_region.maintarget_comparison_reference_id = maintarget_comparison_reference.id and 
                    reference_region.id = maintarget_comparison_reference_region.reference_region_id and 
                    reference.id = reference_region.reference_id 
                ORDER BY maintarget_comparison_reference_region.target_number;""", 
                (maintargetComparisonID,))
            allTargetsData = cur.fetchall()
    blocksInTargets = getTargetBlocksAlignments(allTargetsData[startTargetNumber:endTargetNumber])
    conn.close()
    return blocksInTargets

def getBlocksInOfftargetsInformation(offtargetComparisonID:int)->dict:
    blocksInTargets = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    offtarget_comparison_reference_region.target_number as tnumber, 
                    offtarget_comparison_reference_region.reference_region_id,
                    offtarget_comparison.query_region_id, 
                    reference_region.sequence_name as tname, reference_region.start_position as tstart, 
                    reference_region.end_position as tend, reference_region.annotation as tannotation,
                    reference.id as refid, reference.genus as refgenus, reference.specie as refspecie, 
                    reference.version as refversion, reference.genomic as refgenomic  
                FROM 
                    reference, reference_region, offtarget_comparison, offtarget_comparison_reference, 
                    offtarget_comparison_reference_region 
                WHERE 
                    offtarget_comparison.id = %s and 
                    offtarget_comparison_reference.offtarget_comparison_id = offtarget_comparison.id and 
                    offtarget_comparison_reference_region.offtarget_comparison_reference_id = offtarget_comparison_reference.id and 
                    reference_region.id = offtarget_comparison_reference_region.reference_region_id and 
                    reference.id = reference_region.reference_id 
                ORDER BY offtarget_comparison_reference_region.target_number;""", 
                (offtargetComparisonID,))
            allTargetsData = cur.fetchall()
    blocksInTargets = getTargetBlocksAlignments(allTargetsData)
    conn.close()
    return blocksInTargets

def getTargetBlocksAlignments(targetsData:list)->dict:
    blocksInTargets = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            for targetData in targetsData:
                cur.execute("""
                            SELECT
                                query_region_block.start_position as qbStart, query_region_block.end_position as qbEnd,
                                reference_region_block.start_position as tbStart, reference_region_block.end_position as tbEnd,
                                alignment.strand as strand, alignment.missmatches as missm, alignment.alignment_block_number as blockNumber
                            FROM 
                                query_region_block, reference_region_block, alignment
                            WHERE 
                                query_region_block.query_region_id = %s and 
                                reference_region_block.reference_region_id = %s and
                                alignment.reference_region_block_id = reference_region_block.id and 
                                alignment.query_region_block_id = query_region_block.id;""",
                                (targetData["query_region_id"], targetData["reference_region_id"]))
                targetBlocks = cur.fetchall()
                blocksData = {}
                target = TargetSequence.TargetSequence(targetData["refid"], targetData["refgenus"], targetData["refspecie"],
                                                        targetData["refgenomic"], targetData["refversion"], targetData["tname"],
                                                        targetData["tstart"],targetData["tend"],targetData["tend"]-targetData["tstart"]+1,
                                                        eval(targetData["tannotation"]))
                if "tmaintarget" in targetData: target.setMaintarget(targetData["tmaintarget"])
                for block in targetBlocks:
                    blocksData[block["blocknumber"]] = (block["qbstart"], block["qbend"], block["tbstart"], 
                                                        block["tbend"], block["missm"], block["strand"])
                blocksInTargets[(targetData["tnumber"],target)] = blocksData
    conn.close()
    return blocksInTargets

def getQueryEfficiencyInformation(inputData:dict)->None:
    queryData = {}
    effData = {}
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    query.* 
                FROM
                    maintarget_comparison, query_region, query 
                WHERE
                    maintarget_comparison.id = %s and 
                    query_region.id = maintarget_comparison.query_region_id and 
                    query.id = query_region.query_id;""",
                (inputData["maintargetComparisonID"],))
            queryData = cur.fetchone()
            cur.execute("""
                SELECT
                    efficiency_data
                FROM
                    efficiency 
                WHERE
                    query_id = %s and
                    method = %s;""",
                (queryData["id"],inputData["method"]))
            effData = cur.fetchone()
    conn.close()
    inputData["queryID"] = queryData["id"]
    inputData["queryName"] = queryData["name"]
    inputData["querySequence"] = queryData["sequence"]
    inputData["efficiencyData"] = []
    if effData and "efficiency_data" in effData:
        inputData["efficiencyData"] = effData["efficiency_data"]

def getQueryOfftargetsInformation(inputData:dict)->None:
    queryData = getTableData("query", id=inputData["queryID"])[0]
    inputData["queryName"] = f"{queryData['name']}_{inputData['queryRegionStart']}_{inputData['queryRegionEnd']}"
    inputData["querySequence"] = queryData["sequence"][inputData['queryRegionStart']:inputData['queryRegionEnd']]

#######################################INSERT FUNCTIONS#############################################################
####################################################################################################################
def insertQueryMaintargetInformation(inputData:dict)->None:
    queryID = getOrInsertTableData("query", name=inputData["queryName"], sequence=inputData["querySequence"])
    queryRegionID = getOrInsertTableData("query_region", query_id=sum(queryID), start_position=1, 
                                                            end_position=len(inputData["querySequence"]))
    inputData["maintargetComparisonID"] = insertTableData("maintarget_comparison", project_id=inputData["projectID"], 
                                                                                    query_region_id=sum(queryRegionID))
    inputData["maintargetComparisonReferenceID"] = {}
    for referenceID in inputData["referenceIDs"]:
        inputData["maintargetComparisonReferenceID"][referenceID] = insertTableData("maintarget_comparison_reference", 
                                                                                    maintarget_comparison_id=inputData["maintargetComparisonID"], 
                                                                                    reference_id=referenceID)
    inputData["queryRegionID"] = sum(queryRegionID)
    updateColumnTableData("project", "last_modification_date", datetime.datetime.today(), id=inputData["projectID"])

def insertBlocksInMaintargetsInformation(inputData:dict, blocksInTargets:dict)->None:
    for targetNumber, target in sorted(tuple(blocksInTargets.keys()), key=lambda targetData: targetData[0]):
        targetRegionID = getOrInsertTableData("reference_region", reference_id=target.getRefID(), 
                                                                    sequence_name=target.getSeqName(), 
                                                                    start_position=target.getStartRegion(), 
                                                                    end_position=target.getEndRegion(),
                                                                    annotation=str(target.getAnnotation()))
        insertTableData("maintarget_comparison_reference_region", 
                                    maintarget_comparison_reference_id=inputData["maintargetComparisonReferenceID"][target.getRefID()], 
                                    target_number=targetNumber,
                                    reference_region_id=sum(targetRegionID),
                                    maintarget=False)
        insertTargetBlockAlignments(inputData, blocksInTargets[(targetNumber,target)], targetRegionID)

def insertQueryOfftargetInformation(inputData:dict, referenceID:int)->None:
    queryID = getOrInsertTableData("query", name=inputData["queryName"], sequence=inputData["querySequence"])
    queryRegionID = getOrInsertTableData("query_region", query_id=sum(queryID), 
                                                        start_position=inputData["queryRegionStart"], 
                                                        end_position=inputData["queryRegionEnd"])
    inputData["offtargetComparisonID"] = insertTableData("offtarget_comparison", project_id=inputData["projectID"], 
                                                                                query_region_id=sum(queryRegionID))
    inputData["offtargetComparisonReferenceID"] = insertTableData("offtarget_comparison_reference", 
                                                            offtarget_comparison_id=inputData["offtargetComparisonID"], 
                                                            reference_id=referenceID)
    inputData["queryRegionID"] = sum(queryRegionID)
    updateColumnTableData("project", "last_modification_date", datetime.datetime.today(), id=inputData["projectID"])

def insertBlocksInOfftargetsInformation(inputData:dict, blocksInTargets:dict)->None:
    for targetNumber, target in sorted(tuple(blocksInTargets.keys()), key=lambda targetData: targetData[0]):
        targetRegionID = getOrInsertTableData("reference_region", reference_id=target.getRefID(), 
                                                                    sequence_name=target.getSeqName(), 
                                                                    start_position=target.getStartRegion(), 
                                                                    end_position=target.getEndRegion(),
                                                                    annotation=str(target.getAnnotation()))
        insertTableData("offtarget_comparison_reference_region", 
                                    offtarget_comparison_reference_id=inputData["offtargetComparisonReferenceID"], 
                                    target_number=targetNumber,
                                    reference_region_id=sum(targetRegionID))
        insertTargetBlockAlignments(inputData, blocksInTargets[(targetNumber,target)], targetRegionID)

def insertTargetBlockAlignments(inputData:dict, targetBlocks:dict, targetRegionID:tuple)->None: 
    for blockNumber in targetBlocks:
        qstart,qend,tstart,tend,missm,strand = targetBlocks[blockNumber]
        queryBlockID = getOrInsertTableData("query_region_block", query_region_id=inputData["queryRegionID"], 
                                                                    start_position=qstart, end_position=qend)
        targetBlockID = getOrInsertTableData("reference_region_block", reference_region_id=sum(targetRegionID), 
                                                                        start_position=tstart, end_position=tend)
        getOrInsertTableData("alignment", reference_region_block_id=sum(targetBlockID), 
                                            query_region_block_id=sum(queryBlockID),
                                            strand=strand, missmatches=missm, alignment_block_number=blockNumber)

def insertQueryEfficiencyInformation(inputData:dict)->None:
    insertTableData("efficiency",query_id=inputData["queryID"],method=inputData["method"],
                                            efficiency_data=inputData["efficiencyData"])
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            for maintargetNumber in inputData["maintargetNumbers"]:
                cur.execute("""
                            UPDATE 
                                maintarget_comparison_reference_region 
                            SET 
                                maintarget=%s 
                            FROM
                                maintarget_comparison_reference
                            WHERE 
                                maintarget_comparison_reference.maintarget_comparison_id = %s and
                                maintarget_comparison_reference_region.maintarget_comparison_reference_id = maintarget_comparison_reference.id and
                                target_number = %s;""",
                            (True, inputData["maintargetComparisonID"], maintargetNumber))
                cur.execute("""
                            SELECT 
                                project_id 
                            FROM
                                maintarget_comparison
                            WHERE 
                                id = %s;""",
                            (inputData["maintargetComparisonID"],))
                projectID = cur.fetchone()["project_id"]
    conn.close()
    updateColumnTableData("project", "last_modification_date", datetime.datetime.today(), id=projectID)

#######################################GENERAL FUNCTIONS############################################################
####################################################################################################################
def insertTableData(tableName:str,**data)->tuple[int,int]:
    insertedID = 0
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            sqlQuery = sql.SQL("INSERT INTO {table} ({columnNames}) VALUES ({columnValues}) RETURNING *").format(
                                table = sql.Identifier(tableName),
                                columnNames = sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                                columnValues = sql.SQL(', ').join(sql.Placeholder() * len(data))
                                )
            cur.execute(sqlQuery, tuple(data.values()))
            insertedID = cur.fetchone()["id"]
    conn.close()
    return insertedID

def getOrInsertTableData(tableName:str,**data)->tuple[int,int]:
    insertedID = 0
    obtainedID = getTableData(tableName, "id", **data)
    if obtainedID:
        obtainedID = obtainedID[0]["id"]
    else:
        obtainedID = 0
        with psycopg2.connect(**getConnectionDict()) as conn:
            with conn.cursor() as cur:
                sqlQuery = sql.SQL("INSERT INTO {table} ({columnNames}) VALUES ({columnValues}) RETURNING *").format(
                                    table = sql.Identifier(tableName),
                                    columnNames = sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                                    columnValues = sql.SQL(', ').join(sql.Placeholder() * len(data))
                                    )
                cur.execute(sqlQuery, tuple(data.values()))
                insertedID = cur.fetchone()["id"]
        conn.close()
    return obtainedID, insertedID

def updateColumnTableData(tableName:str, columnName:str, columnValue:str, **constraints)->tuple:
    updatedID = None
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            sqlQuery = sql.SQL("UPDATE {table} SET {cName}=%s WHERE {columnConstraints}=%s RETURNING *").format(
                                table = sql.Identifier(tableName),
                                cName = sql.Identifier(columnName),
                                columnConstraints=sql.SQL('=%s AND ').join(map(sql.Identifier,constraints.keys()))
                                )
            cur.execute(sqlQuery, (columnValue, *constraints.values()))
            updatedID = tuple(map(lambda x: x["id"], cur.fetchall()))
    conn.close()
    return updatedID

def getTableData(tableName:str, *columnNames, **constraints)->list:
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            if columnNames:
                if constraints:
                    sqlQuery = sql.SQL("SELECT {column} FROM {table} WHERE {columnConstraints}=%s").format(
                                        column=sql.SQL(',').join(map(sql.Identifier,columnNames)), 
                                        table=sql.Identifier(tableName),
                                        columnConstraints=sql.SQL('=%s AND ').join(map(sql.Identifier,constraints.keys()))
                                        )
                else:
                    sqlQuery = sql.SQL("SELECT {column} FROM {table}").format(
                                        column=sql.SQL(',').join(map(sql.Identifier,columnNames)),
                                        table=sql.Identifier(tableName)
                                        )
            else:
                if constraints:
                    sqlQuery = sql.SQL("SELECT * FROM {table} WHERE {columnConstraints}=%s").format(
                                        table=sql.Identifier(tableName),
                                        columnConstraints=sql.SQL('=%s AND ').join(map(sql.Identifier,constraints.keys()))
                                        )
                else:
                    sqlQuery = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(tableName))
            cur.execute(sqlQuery, tuple(constraints.values()))
            rows = cur.fetchall()
    conn.close()
    return rows

def deleteTableData(tableName:str, **constraints)->None:
    with psycopg2.connect(**getConnectionDict()) as conn:
        with conn.cursor() as cur:
            sqlQuery = sql.SQL("DELETE FROM {table} WHERE {columnConstraints}=%s").format(
                                table=sql.Identifier(tableName),
                                columnConstraints=sql.SQL('=%s AND ').join(map(sql.Identifier,constraints.keys()))
                                )
            cur.execute(sqlQuery, tuple(constraints.values()))
    conn.close()