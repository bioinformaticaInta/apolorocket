#!/usr/bin/python

import plotly
import plotly.express
import pandas

def getBlocksInTargets(inputData:dict, sirnaData:dict)->dict:
    allBlocks = {}
    blocksInTargets = {}
    for sirnaName in sorted(sirnaData.keys()):
        startQueryPos = sirnaName-1
        endQueryPos = startQueryPos + (inputData["sirnaSize"]-1)
        sirna = sirnaData[sirnaName]
        allTargets = sirna.bowtieHits()
        for target,startInTarget,strandInTarget,missmInTarget in allTargets:
            startQuery = startQueryPos
            endQuery = endQueryPos
            endInTarget = startInTarget + (inputData["sirnaSize"]-1)
            missm = missmInTarget
            #Identify the block where the alignment from in the off Target sequence
            if target in allBlocks:
                pos = 0
                found = False
                while pos < len(allBlocks[target]) and not found:
                    #The alingment belongs to this block, then extend the extremes
                    #start extreme in negative strand or end extreme in positive strand 
                    block = allBlocks[target][pos]
                    if strandInTarget == "+":
                        if block[0] <= startQueryPos <= block[1] and block[2] <= startInTarget <= block[3] and strandInTarget == block[5]:
                            found = True
                            startInTarget = block[2]
                    else:
                        if block[0] <= endQueryPos <= block[1] and block[2] <= endInTarget <= block[3] and strandInTarget == block[5]:
                            found = True
                            endInTarget = block[3]
                    if found:
                        block = allBlocks[target].pop(pos)
                        startQuery = block[0]-1
                        missm = block[4]+missmInTarget
                    pos += 1
            else:
                allBlocks[target] = []
            allBlocks[target].append((startQuery+1 , endQuery+1, startInTarget, endInTarget, missm, strandInTarget))
    targetNumber = 1
    for target in allBlocks:
        blocksInTargets[(targetNumber,target)] = {}
        blockNumber = 1
        for blockData in sorted(allBlocks[target], key=lambda block: block[0]):
            blocksInTargets[(targetNumber,target)][blockNumber] = blockData
            blockNumber += 1
        targetNumber += 1
    return blocksInTargets

def mainTargetsFigure(blocksInTargets:dict, figureFileName:str)->None:
    mainTargetsFigure = None
    mainTargetsFigure = paintRegionsMainTargetsFigure(blocksInTargets)
    mainTargetsFigure.update_layout(
        title='Alignment regions per target position', # Title
        xaxis_title='Query position', # x-axis name
        yaxis_title='Database target', # y-axis name
        xaxis_tickangle=45,  # Set the x-axis label angle
        showlegend=True,     # Display the legend
    )
    mainTargetsFigure.write_html(figureFileName)

def offTargetsFigure(blocksInTargets:dict, figureFileName:str)->None:
    offTargetsFigure = None
    offTargetsFigure = paintRegionsMainTargetsFigure(blocksInTargets)
    offTargetsFigure.update_layout(
        title='Alignment regions per target position', # Title
        xaxis_title='Query position', # x-axis name
        yaxis_title='Database target', # y-axis name
        xaxis_tickangle=45,  # Set the x-axis label angle
        showlegend=True,     # Display the legend
    )
    offTargetsFigure.write_html(figureFileName)

def efficiencyFigure(efficiencyData:list, blocksInTargets:dict, figureFileName:str)->None:
    efficiencyFigure = None
    posX = [int(i) for i in range(len(efficiencyData))]
    if blocksInTargets:
        efficiencyFigure = paintRegionsEfficiencyFigure(blocksInTargets)
        efficiencyFigure.add_scatter(x=posX, y=efficiencyData, line_shape='hv', name="Efficient siRNAs", 
                                    hovertemplate='Query position: %{x}<br>Number of efficient siRNAs: %{y}')
    else:
        df = pandas.DataFrame({"Query position":posX , "Number of efficient siRNAs":efficiencyData})
        efficiencyFigure = plotly.express.line(df, x="Query position", y="Number of efficient siRNAs", line_shape='hv')
    efficiencyFigure.update_layout(
        title='siRNAs efficients per target position', # Title
        xaxis_title='Query position', # x-axis name
        yaxis_title='Number of efficient siRNAs', # y-axis name
        xaxis_tickangle=45,  # Set the x-axis label angle
        hovermode="x unified",
        showlegend = True,
        legend_title_text=''
    )
    efficiencyFigure.write_html(figureFileName)

def paintRegionsMainTargetsFigure(blocksInTargets:list)->plotly.graph_objs.Figure:
    blocksInTargetsData = []
    deltaBlocksInTargetsData = {}
    for targetNumber,target in blocksInTargets:
        deltaBlocksInTargetsData["Target number: "+str(targetNumber)] = []
        targetBlocks = blocksInTargets[(targetNumber,target)]
        for blockNumber in sorted(tuple(targetBlocks.keys())):
            qstart,qend,tstart,tend,missm,strand = targetBlocks[blockNumber]
            blocksInTargetsData.append({"Target number": "Target number: "+str(targetNumber),
                                        "Target ID":target.getName(),
                                        "Block number":blockNumber,
                                        "Start block position in query":qstart, "End block position in query":qend})
            deltaBlocksInTargetsData["Target number: "+str(targetNumber)].append(qend-qstart)
    df = pandas.DataFrame(blocksInTargetsData) 
    hoverName = None
    hoverData = {"Target number":False, "Target ID":False, "Block number":True, "Start block position in query":False, 
                "End block position in query":False}
    mainTargetsFigure = plotly.express.timeline(df, x_start="Start block position in query", 
                                                    x_end="End block position in query", 
                                                    y="Target number", color="Target ID", 
                                                    hover_name=hoverName, hover_data=hoverData)
    mainTargetsFigure.layout.xaxis.type = 'linear'
    xlabelToLinear(mainTargetsFigure, deltaBlocksInTargetsData)
    #mainTargetsFigure.update_layout(yaxis_showticklabels=False)
    return mainTargetsFigure

def paintRegionsEfficiencyFigure(blocksInTargets:dict)->plotly.graph_objs.Figure:
    blocksInTargetsData = []
    deltaBlocksInTargetsData = {}
    for targetNumber,target in blocksInTargets:
        deltaBlocksInTargetsData["Target number: "+str(targetNumber)] = []
        targetBlocks = blocksInTargets[(targetNumber,target)]
        for blockNumber in sorted(tuple(targetBlocks.keys())):
            qstart,qend,tstart,tend,missm,strand = targetBlocks[blockNumber]
            blocksInTargetsData.append({"Target number":"Target number: "+str(targetNumber),
                                        "Target ID":target.getName(),
                                        "Start block position in query":qstart, "End block position in query":qend,
                                        "Main target": target.isMaintarget()})
            deltaBlocksInTargetsData["Target number: "+str(targetNumber)].append(qend-qstart)
    hoverData = {"Target number":False, "Target ID":False, "Main target":True}
    efficiencyFigure = plotly.express.timeline(pandas.DataFrame(blocksInTargetsData), x_start="Start block position in query", 
                                                                                    x_end="End block position in query", 
                                                                                    y="Target number", color="Target ID", 
                                                                                    hover_name=None, hover_data=hoverData)
    efficiencyFigure.layout.xaxis.type = 'linear'
    xlabelToLinear(efficiencyFigure, deltaBlocksInTargetsData)
    return efficiencyFigure

def xlabelToLinear(figure:plotly.graph_objs.Figure, deltaBlocksInTargetsData:dict)->None:
    for figData in figure.data:
        xData = []
        yNamePre = None
        pos = 0
        for yName in figData.y:
            if yName != yNamePre:
                yNamePre = yName
                pos = 0
            xData.append(deltaBlocksInTargetsData[yName][pos])
            pos += 1
        figData.x = xData

def efficiencyDataForFigure(inputData:dict, sirnaData:dict)->list:
    queryLen = len(inputData["querySequence"])
    effCount = [0]*queryLen
    for sirnaName in sorted(sirnaData.keys()):
        startQueryPos = sirnaName-1
        endQueryPos = startQueryPos + (inputData["sirnaSize"]-1)
        sirna = sirnaData[sirnaName]
        if sirna.getEfficiency():
            for sirnaPos in range(startQueryPos, endQueryPos):
                effCount[sirnaPos]+=1
    return [0]+effCount 

def getTargetsTableData(blocksInTargets:list)->list:
    tableData = []
    for targetNumber,target in sorted(tuple(blocksInTargets.keys()), key=lambda targetData: targetData[0]):
        targetBlocks = blocksInTargets[(targetNumber,target)]
        blocksData = []
        for blockNumber in sorted(tuple(targetBlocks.keys())):
            qstart,qend,tstart,tend,missm,strand = targetBlocks[blockNumber]
            blocksData.append({"Block number":blockNumber,
                            "Start block position in target":tstart, "End block position in target":tend,
                            "Start block position in query":qstart, "End block position in query":qend,
                            "Missmatches in block":missm,
                            "Alignment strand":strand})
        tableRow = {"Target number":targetNumber, "Reference": target.getRefInformation(), "Target ID":target.getSeqName(),
                    "Target region":"-".join(map(str,target.getRegion())), "Target region length":target.getLength(),
                    "Annotation":target.getAnnotation(), "Blocks in target region":len(targetBlocks),
                    "Blocks data":blocksData}
        tableData.append(tableRow)
    return tableData
