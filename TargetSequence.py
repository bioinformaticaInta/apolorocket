#!/usr/bin/python

class Reference:
    def __init__(self, refID:int, refGenus:str, refSpecie:str, refGenomic:str, refVersion:str):
        self.refID = refID
        self.refGenus = refGenus
        self.refSpecie = refSpecie
        self.refGenomic = refGenomic
        self.refVersion = refVersion
    
    def __repr__(self) -> str:
        refType = "genome" if self.refGenomic else "transcriptome"
        return f"{self.refGenus}_{self.refSpecie}_{refType}_{self.refVersion}"

    def completeName(self)->str:
        refType = "genome" if self.refGenomic else "transcriptome"
        return f"{self.refGenus[0]}. {self.refSpecie} {refType} {self.refVersion}"
    
    def __eq__(ref1, ref2)->bool:
        return ref1.refGenus==ref2.refGenus and ref1.refSpecie==ref2.refSpecie and ref1.refGenomic==ref2.refGenomic and ref1.refVersion==ref2.refVersion
    
    def __hash__(self)->int:
        return(hash(self.refGenus+self.refSpecie+str(self.refGenomic)+self.refVersion))
    
    def toDict(self)->dict:
        return {"refGenus":self.refGenus,
                "refSpecie":self.refSpecie, 
                "refGenomic":self.refGenomic, 
                "refVersion":self.refVersion
                }

    def getInformation(self)->dict:
        return {"genus":self.refGenus,
                "specie":self.refSpecie, 
                "genomic":self.refGenomic, 
                "version":self.refVersion
                }

    def getReferenceID(self)->int:
        return self.refID
    
class TargetSequence:
    def __init__(self, refID:int, refGenus:str, refSpecie:str, refGenomic:str, refVersion:str, seqName:str, 
                startRegion:int=None, endRegion:int=None, length:int=None, annotation:list=None, maintarget:bool=False):
        self.reference = Reference(refID, refGenus, refSpecie, refGenomic, refVersion)
        self.seqName = seqName
        self.startRegion = startRegion
        self.endRegion = endRegion
        self.length = length
        self.annotation = annotation if annotation else []
        self.maintarget = maintarget
   
    def __repr__(self)->str:
        return '< ' + ' | '.join(["refName="+self.reference.completeName(),"ID="+self.seqName,
                                "Region="+str(self.startRegion)+"-"+str(self.endRegion),
                                "Length="+str(self.length),"Annotation="+str(self.annotation)]) + ' >'
    
    def __eq__(ts1, ts2)->bool:
        return ts1.reference==ts2.reference and ts1.seqName==ts2.seqName and ts1.startRegion==ts2.startRegion and ts1.endRegion==ts2.endRegion

    def __hash__(self)->int:
        return(hash(str(self.reference)+self.seqName+str(self.startRegion)+str(self.startRegion)))

    def toDict(self)->dict:
        return {"reference":self.reference.toDict(),
                "seqName":self.seqName, 
                "startRegion":self.startRegion, 
                "endRegion":self.endRegion, 
                "length":self.length,
                "annotation":self.annotation
                }

    def getName(self)->str:
        return f"{self.seqName} ({self.reference.completeName()})"

    def getRefInformation(self)->dict:
        return self.reference.getInformation()

    def getRefID(self)->dict:
        return self.reference.getReferenceID()

    def getRefName(self)->str:
        return str(self.reference)

    def getSeqName(self)->str:
        return self.seqName

    def getStartRegion(self)->int:
        return self.startRegion

    def getEndRegion(self)->int:
        return self.endRegion

    def getRegion(self)->tuple[int,int]:
        return self.startRegion,self.endRegion
    
    def getNameWithRegion(self)->str:
        name = self.getRefName()+"_"+self.seqName
        if self.startRegion and self.endRegion:
            name += "_"+str(self.startRegion)+"-"+str(self.endRegion)
        return name
    
    def getSeqNameWithRegion(self)->str:
        name = self.seqName
        if self.startRegion and self.endRegion:
            name += "_"+str(self.startRegion)+"-"+str(self.endRegion)
        return name
    
    def getAnnotation(self)->list:
        return self.annotation

    def getLength(self)->int:
        return self.length

    def setRegion(self, startRegion:int, endRegion:int)->None:
        self.startRegion = startRegion
        self.endRegion = endRegion
        self.length = endRegion-startRegion+1

    def setLength(self, length:int)->None:
        if not self.startRegion and not self.endRegion:
            self.length = length

    def addAnnotation(self, annotation:str)->None:
        self.annotation.append(annotation)

    def isRegion(self, start:int, end:int)->bool:
        return start==self.startRegion and end==self.endRegion
    
    def isMaintarget(self)->bool:
        return self.maintarget
    
    def setMaintarget(self, maintarget:bool)->None:
        self.maintarget = maintarget