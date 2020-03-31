## @file
# parse FDF file
#
#  Copyright (c) 2020, Intel Corporation. All rights reserved.<BR>
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#
from CommonDataClass.FdfClass import FDClassObject
from CommonDataClass.FdfClass import RegionData
from CommonDataClass.FdfClass import FvData
from CommonDataClass.FdfClass import AprioriSectionData
from CommonDataClass.FdfClass import FfsInfStatementClassObject
from CommonDataClass.FdfClass import FfsInfStatementData
from CommonDataClass.FdfClass import FileStatementData
from CommonDataClass.FdfClass import FileStatementClassObject
from CommonDataClass.FdfClass import VerSectionClassObject
from CommonDataClass.FdfClass import UiSectionClassObject
from CommonDataClass.FdfClass import FvImageSectionClassObject
from CommonDataClass.FdfClass import DataSectionClassObject
from CommonDataClass.FdfClass import DepexSectionClassObject
from CommonDataClass.FdfClass import CompressSectionClassObject
from CommonDataClass.FdfClass import GuidSectionClassObject
from CommonDataClass.FdfClass import CapsuleClassObject
from CommonDataClass.FdfClass import CapsuleData
from CommonDataClass.FdfClass import CapsulePayloadData
from CommonDataClass.FdfClass import RuleComplexFileClassObject
from CommonDataClass.FdfClass import RuleSimpleFileClassObject
from CommonDataClass.FdfClass import EfiSectionClassObject
from CommonDataClass.FdfClass import OptionRomClassObject
from CommonDataClass.FdfClass import OptRomInfStatementData
from CommonDataClass.FdfClass import OptRomInfStatementOverrideAttribs
from CommonDataClass.FdfClass import OptRomFileStatementData

from .Fd import FD
from .Region import Region
from .Fv import FV
from .AprioriSection import AprioriSection
from .FfsInfStatement import FfsInfStatement
from .FfsFileStatement import FileStatement
from .VerSection import VerSection
from .UiSection import UiSection
from .FvImageSection import FvImageSection
from .DataSection import DataSection
from .DepexSection import DepexSection
from .CompressSection import CompressSection
from .GuidSection import GuidSection
from .CapsuleData import CapsuleFfs, CapsulePayload, CapsuleFv, CapsuleFd, CapsuleAnyFile, CapsuleAfile
from .EfiSection import EfiSection
from .OptionRom import OPTIONROM
from .OptRomInfStatement import OptRomInfStatement
from .OptRomFileStatement import OptRomFileStatement
from .GenFdsGlobalVariable import GenFdsGlobalVariable

class FdfInfoOperator():
    def __init__(self,fdf_profile):
        self.fdf_profile = fdf_profile
        self.PcdDict = self.fdf_profile.PcdDict
        self.PcdLocalDict = self.fdf_profile.PcdLocalDict
        self.InfList = self.fdf_profile.InfList
        self.InfDict = self.fdf_profile.InfDict
        # ECC will use this Dict and List information
        self.PcdFileLineDict = self.fdf_profile.PcdFileLineDict
        self.InfFileLineList = self.fdf_profile.InfFileLineList

        self.FdDict = FdDict(self.fdf_profile.FdDict)
        self.FdNameNotSet = self.fdf_profile.FdNameNotSet
        self.FvDict = FvDict(self.fdf_profile.FvDict)
        self.CapsuleDict = CapsuleDict(self.fdf_profile.CapsuleDict)
        self.RuleDict = RuleDict(self.fdf_profile.RuleDict)
        self.OptRomDict = OptRomDict(self.fdf_profile.OptRomDict)
        self.FmpPayloadDict = FmpPayloadDict(self.fdf_profile.FmpPayloadDict)

def WrappSection(sec):
    if isinstance(sec,VerSectionClassObject):
        sec = VerSection(sec)
    if isinstance(sec,UiSectionClassObject):
        sec = UiSection(sec)
    if isinstance(sec, FvImageSectionClassObject):
        sec = FvImageSection(sec)
    if isinstance(sec, DepexSectionClassObject):
        sec = DepexSection(sec)
    if isinstance(sec, DataSectionClassObject):
        sec = DataSection(sec)
    if isinstance(sec, CompressSectionClassObject):
        sec = CompressSection(sec)
    if isinstance(sec, GuidSectionClassObject):
        sec = GuidSection(sec)
    if isinstance(sec, EfiSectionClassObject):
        sec = EfiSection(sec)
    if sec.SectionList:
        for subsec in sec.SectionList:
            WrappSection(subsec)
    #else:
    #    print(sec.__class__.__name__)
class FvDict():
    def __init__(self,fv_dict):
        self._fv_dict = fv_dict
    def __getitem__(self,key):
        value = self._fv_dict.get(key)
        if value is None:
            return None
        FvObj = FV(value)
        FvObj.FfsList = []
        for item in value.FfsList:
            if isinstance(item, FileStatementClassObject):
                ffsfileobj = FileStatement(item)
                seclist = ffsfileobj.SectionList
                for sec in seclist:
                    WrappSection(sec)
            if isinstance(item, FfsInfStatementClassObject):
                FvObj.FfsList.append(FfsInfStatement(item))
        FvObj.AprioriSectionList = [AprioriSection(item) for item in value.AprioriSectionList]
        return FvObj
    def __iter__(self):
        for key in self._fv_dict.keys():
            yield key
    def values(self):
        for key in self._fv_dict:
            yield self[key]
    def get(self,key):
        return self[key]
class FdDict():
    def __init__(self,fd_dict):
        self._fd_dict = fd_dict
    def __getitem__(self,key):
        value = self._fd_dict.get(key)
        if not value:
            return None
        FdObj = FD(value)
        FdObj.RegionList = [Region(item) for item in value.RegionList]
        for region in FdObj.RegionList:
            if region.RegionType == "INF":
                region.RegionDataList = [FfsInfStatement(item) for item in region.RegionDataList]
        return FdObj
    def __iter__(self):
        for key in self._fd_dict.keys():
            yield key
    def values(self):
        for key in self._fd_dict:
            yield self[key]
    def get(self,key):
        return self[key]

class CapsuleDict():
    def __init__(self,cap_dict):
        self._cap_dict = cap_dict        
    def __getitem__(self,key):
        value = self._cap_dict.get(key)
        if not value:
            return None
        CapObj = Capsule(value)
        CapObj.CapsuleDataList = []
        for cap_data in value.CapsuleDataList:
            if cap_data.Type == "CapsuleFfs":
                CapObj.CapsuleDataList.append(CapsuleFfs(cap_data))
            if cap_data.Type == "CapsuleFv":
                CapObj.CapsuleDataList.append(CapsuleFv(cap_data))
            if cap_data.Type == "CapsuleFd":
                CapObj.CapsuleDataList.append(CapsuleFd(cap_data))
            if cap_data.Type == "CapsuleAnyFile":
                CapObj.CapsuleDataList.append(CapsuleAnyFile(cap_data))
            if cap_data.Type == "CapsuleAfile":
                CapObj.CapsuleDataList.append(CapsuleAfile(cap_data))
        return CapObj
    def __iter__(self):
        for key in self._cap_dict.keys():
            yield key
    def values(self):
        return self._cap_dict.values()
    def get(self,key):
        return self[key]
class FmpPayloadDict():
    def __init__(self, payload_dict):
        self._payload_dict = payload_dict
    def __getitem__(self,key):
        value = self._payload_dict.get(key)
        if not value:
            return None
        PayLoadObj = CapsulePayloadData(value)
        return PayLoadObj
    def __iter__(self):
        for key in self._payload_dict.keys():
            yield key
    def values(self):
        return self._payload_dict.values()
    def get(self,key):
        return self[key]

class RuleDict():
    def __init__(self, rule_dict):
        self._rule_dict = rule_dict
    def __getitem__(self,key):
        value = self._rule_dict.get(key)
        if not value:
            return None
        if isinstance(value, RuleComplexFileClassObject):
            RuleObj = value
            for sec in RuleObj.SectionList:
                WrappSection(sec)
        elif isinstance(value, RuleSimpleFileClassObject):
            RuleObj = value
        else:
            RuleObj = Rule(value)
        return RuleObj
    def __iter__(self):
        for key in self._rule_dict.keys():
            yield key
    def values(self):
        return self._rule_dict.values()
    def get(self,key):
        return self[key]

class OptRomDict():
    def __init__(self,opt_dict):
        self._opt_dict = opt_dict
    def __getitem__(self,key):
        value = self._opt_dict.get(key)
        if not value:
            return None
        OptRomObj = OPTIONROM(value)
        for ffs in OptRomObj.FfsList:
            if isinstance(ffs,OptRomInfStatementData):
                ffs = OptRomInfStatement(ffs)
                for sec in ffs.SectionList:
                    WrappSection(sec)
            if isinstance(ffs, OptRomFileStatementData):
                ffs = OptRomFileStatement(ffs)

        return OptRomObj
    def __iter__(self):
        for key in self._opt_dict.keys():
            yield key
    def values(self):
        return self._opt_dict.values()
    def get(self,key):
        return self[key]