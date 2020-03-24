## @file
# classes represent data in FDF
#
#  Copyright (c) 2007 - 2018, Intel Corporation. All rights reserved.<BR>
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#
from uuid import UUID
EFI_CERT_TYPE_PKCS7_GUID = UUID('{4aafd29d-68df-49ee-8aa9-347d375665a7}')
EFI_CERT_TYPE_RSA2048_SHA256_GUID = UUID('{a7717414-c616-4977-9420-844712a735bf}')

## FD data in FDF
#
#
class FDClassObject:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.type 
        self.FdUiName = ''
        self.CreateFileName = None
        self.BaseAddress = None
        self.BaseAddressPcd = None
        self.Size = None
        self.SizePcd = None
        self.ErasePolarity = None
        # 3-tuple list (blockSize, numBlocks, pcd)
        self.BlockSizeList = []
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        self.RegionList = []

## Region data in FDF
#
#
class RegionData():
    def __init__(self):
        self.Offset = None       # The begin position of the Region
        self.Size = None         # The Size of the Region
        self.PcdOffset = None
        self.PcdSize = None
        self.SetVarDict = {}
        self.RegionType = None
        self.RegionDataList = []

## FV data in FDF
class FvData():
    def __init__(self, Name=None):
        self.UiFvName = Name
        self.CreateFileName = None
        self.BlockSizeList = []
        self.DefineVarDict = {}
        self.SetVarDict = {}
        self.FvAlignment = None
        self.FvAttributeDict = {}
        self.FvNameGuid = None
        self.FvNameString = None
        self.AprioriSectionList = []
        self.FfsList = []
        self.BsBaseAddress = None
        self.RtBaseAddress = None
        self.FvInfFile = None
        self.FvAddressFile = None
        self.BaseAddress = None
        self.InfFileName = None
        self.FvAddressFileName = None
        self.CapsuleName = None
        self.FvBaseAddress = None
        self.FvForceRebase = None
        self.FvRegionInFD = None
        self.UsedSizeEnable = False
        self.FvExtEntryTypeValue = []
        self.FvExtEntryType = []
        self.FvExtEntryData = []

## APRIORI file data in FDF file
#
#
class AprioriSectionData():
    def __init__(self):
        self.DefineVarDict = {}
        self.FfsList = []
        self.AprioriType = ""

## FFS data in FDF
#
#
class FfsClassObject:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.NameGuid = None
        self.Fixed = False
        self.CheckSum = False
        self.Alignment = None
        self.SectionList = []

## FILE statement data in FDF
#
#
class FileStatementClassObject (FfsClassObject) :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FfsClassObject.__init__(self)
        self.FvFileType = None
        self.FileName = None
        self.KeyStringList = []
        self.FvName = None
        self.FdName = None
        self.DefineVarDict = {}
        self.KeepReloc = None

## INF statement data in FDF
#
#
class FfsInfStatementClassObject(FfsClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FfsClassObject.__init__(self)
        self.Rule = None
        self.Version = None
        self.Ui = None
        self.InfFileName = None
        self.BuildNum = ''
        self.KeyStringList = []
        self.KeepReloc = None
        self.UseArch = None
        
class FfsInfStatementData(FfsInfStatementClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FfsInfStatementClassObject.__init__(self)
        self.TargetOverrideList = []
        self.ShadowFromInfFile = None
        self.KeepRelocFromRule = None
        self.InDsc = True
        self.OptRomDefs = {}
        self.PiSpecVersion = '0x00000000'
        self.InfModule = None
        self.FinalTargetSuffixMap = {}
        self.CurrentLineNum = None
        self.CurrentLineContent = None
        self.FileName = None
        self.InfFileName = None
        self.OverrideGuid = None
        self.PatchedBinFile = ''
        self.MacroDict = {}
        self.Depex = False

class FileStatementData (FileStatementClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FileStatementClassObject.__init__(self)
        self.CurrentLineNum = None
        self.CurrentLineContent = None
        self.FileName = None
        self.InfFileName = None
        self.SubAlignment = None
## section data in FDF
#
#
class SectionClassObject:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.Alignment = None

## Depex expression section in FDF
#
#
class DepexSectionClassObject (SectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.DepexType = None
        self.Expression = None
        self.ExpressionProcessed = False

## Compress section data in FDF
#
#
class CompressSectionClassObject (SectionClassObject) :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.CompType = None
        self.SectionList = []

## Data section data in FDF
#
#
class DataSectionClassObject (SectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.SecType = None
        self.SectFileName = None
        self.SectionList = []
        self.KeepReloc = True

## Rule section data in FDF
#
#
class EfiSectionClassObject (SectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.SectionType = None
        self.Optional = False
        self.FileType = None
        self.StringData = None
        self.FileName = None
        self.FileExtension = None
        self.BuildNum = None
        self.KeepReloc = None

## FV image section data in FDF
#
#
class FvImageSectionClassObject (SectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.Fv = None
        self.FvName = None
        self.FvFileType = None
        self.FvFileName = None
        self.FvFileExtension = None
        self.FvAddr = None

## GUIDed section data in FDF
#
#
class GuidSectionClassObject (SectionClassObject) :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.NameGuid = None
        self.SectionList = []
        self.SectionType = None
        self.ProcessRequired = False
        self.AuthStatusValid = False
        self.ExtraHeaderSize = -1
        self.FvAddr = []
        self.FvParentAddr = None
        self.IncludeFvSection = False

## UI section data in FDF
#
#
class UiSectionClassObject (SectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.StringData = None
        self.FileName = None

## Version section data in FDF
#
#
class VerSectionClassObject (SectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        self.BuildNum = None
        self.StringData = None
        self.FileName = None

## Rule data in FDF
#
#
class RuleClassObject :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.Arch = None
        self.ModuleType = None    # For Module Type
        self.TemplateName = None
        self.NameGuid = None
        self.Fixed = False
        self.Alignment = None
        self.SectAlignment = None
        self.CheckSum = False
        self.FvFileType = None       # for Ffs File Type
        self.KeyStringList = []
        self.KeepReloc = None

## Complex rule data in FDF
#
#
class RuleComplexFileClassObject(RuleClassObject) :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        RuleClassObject.__init__(self)
        self.SectionList = []

## Simple rule data in FDF
#
#
class RuleSimpleFileClassObject(RuleClassObject) :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        RuleClassObject.__init__(self)
        self.FileName = None
        self.SectionType = ''
        self.FileExtension = None

## File extension rule data in FDF
#
#
class RuleFileExtensionClassObject(RuleClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        RuleClassObject.__init__(self)
        self.FileExtension = None

## Capsule data in FDF
#
#
class CapsuleClassObject :
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.SpecName = None
        self.UiCapsuleName = None
        self.CreateFile = None
        self.GroupIdNumber = None
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        # TokensDict[var] = value
        self.TokensDict = {}
        self.CapsuleDataList = []
        self.FmpPayloadList = []
        # For GenFv
        self.BlockSize = None
        # For GenFv
        self.BlockNum = None
        self.CapsuleName = None

## OptionROM data in FDF
#
#
class OptionRomClassObject:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self,Name = ""):
        self.DriverName = None
        self.FfsList = []
        self.DriverName = Name

class OptRomInfStatementData (FfsInfStatementData):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FfsInfStatementData.__init__(self)
        self.OverrideAttribs = None

class OptRomFileStatementData:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        self.FileName = None
        self.FileType = None
        self.OverrideAttribs = None

class OptRomInfStatementOverrideAttribs:

    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):

        self.PciVendorId = None
        self.PciClassCode = None
        self.PciDeviceId = None
        self.PciRevision = None
        self.NeedCompress = None

## base class for capsule data
#
#
class CapsuleData:
    ## The constructor
    #
    #   @param  self        The object pointer
    def __init__(self):
        self.Ffs = None
        self.FvName = None
        self.CapsuleName = None
        self.Type = ''

class CapsulePayloadData:
    '''Generate payload file, the header is defined below:
    #pragma pack(1)
    typedef struct {
        UINT32 Version;
        EFI_GUID UpdateImageTypeId;
        UINT8 UpdateImageIndex;
        UINT8 reserved_bytes[3];
        UINT32 UpdateImageSize;
        UINT32 UpdateVendorCodeSize;
        UINT64 UpdateHardwareInstance; //Introduced in v2
    } EFI_FIRMWARE_MANAGEMENT_CAPSULE_IMAGE_HEADER;
    '''
    def __init__(self):
        self.UiName = None
        self.Version = None
        self.ImageTypeId = None
        self.ImageIndex = None
        self.HardwareInstance = None
        self.ImageFile = []
        self.VendorCodeFile = []
        self.Certificate_Guid = None
        self.MonotonicCount = None
        self.Existed = False
        self.Buffer = None
