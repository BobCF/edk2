import json
import collections
from AutoGen.GenVar import VariableMgr, NvStorageHeaderSize, NvStorageHeaderSize, VariableHeaderSize
from Common.Misc import GuidStructureStringToGuidString
from struct import unpack
import re
import copy

array_re = re.compile("(?P<mType>[a-z_A-Z][a-z_A-Z0-9]*)\[(?P<mSize>[1-9][0-9]*)\]")

class VarField():
    def __init__(self):
        self.Offset = 0
        self.Value = 0
        self.Size = 0

    @property
    def Type(self):
        if self.Size == 1:
            return "UINT8"
        if self.Size == 2:
            return "UINT16"
        if self.Size == 4:
            return "UINT32"
        if self.Size == 8:
            return "UINT64"

        return "UINT8"

class CStruct():
    BASIC_TYPE = {
        "BOOLEAN":1,
        "UINT8":1,
        "UINT16":2,
        "UINT32":4,
        "UINT64":8
        }
    def __init__(self,typedefs):
        self.TypeDefs = typedefs
        self.TypeStack = copy.deepcopy(typedefs)
        self.finalDefs = {}
        
    def CalStuctSize(self, sType):
        rt = 0
        if sType in self.BASIC_TYPE:
            return self.BASIC_TYPE[sType]
        
        ma = array_re.match(sType)
        if ma:
            mType = ma.group('mType')
            mSize = ma.group('mSize')
            rt += int(mSize) * self.CalStuctSize(mType)
        else:
            for subType in self.TypeDefs[sType]:
                rt += self.CalStuctSize(subType['Type'])
            
        return rt
            
        
    def expend(self,fielditem):
        fieldname = fielditem['Name']
        fieldType = fielditem['Type']
        fieldOffset = fielditem['Offset']

        ma = array_re.match(fieldType)
        if ma:
            mType = ma.group('mType')
            mSize = ma.group('mSize')
            return [{"Name":"%s[%d]" % (fieldname,i), "Type":mType, "Offset": (fieldOffset + i*self.CalStuctSize(mType))} for i in range(int(mSize))]
        else:
            return [ {"Name":"%s.%s" % (fieldname,item['Name']), "Type":item['Type'], "Offset": (fieldOffset + item['Offset']) } for item in self.TypeDefs[fielditem['Type']] ]    
        
    def ExpandTypes(self):
        if not self.finalDefs:
            for datatype in self.TypeStack:
                result = []
                mTypeStack = self.TypeStack[datatype]
                while len(mTypeStack)>0:
                    item = mTypeStack.pop()
                    if item['Type'] in self.BASIC_TYPE:
                        result.append(item)
                    else:
                        for expand_item in self.expend(item):
                            mTypeStack.append(expand_item)
                self.finalDefs[datatype] = result
            self.finalDefs
        return self.finalDefs
        
            

class Variable():
    def __init__(self):
        self.mAlign = 1
        self.mTotalSize = 1
        self.mValue = {}  # {defaultstore: value}
        self.mBin = {}
        self.fields = {}  # {defaultstore: fileds}
        self.delta = {}
        self.attributes = 0
        self.mType = ''
        self.guid = ''
        self.mName = ''
        self.cDefs = None

    @property
    def GuidArray(self):
        Guid = GuidStructureStringToGuidString(self.guid)
        return Guid.split('-')

    def pack(self):

        for defaultid in self.mValue:
            var_value = self.mValue[defaultid]
            varname_array = "{%s,0x00,0x00}" % ",".join(
                "0x%02x,0x00" % ord(C) for C in self.mName)

            var_name_buffer = VariableMgr.PACK_VARIABLE_NAME(varname_array)

            var_header_buffer = VariableMgr.PACK_VARIABLE_HEADER(
                self.attributes, len(var_name_buffer), len(var_value), self.GuidArray)

            DataBuffer = VariableMgr.AlignData(var_name_buffer + var_value)
            self.mBin[defaultid] = var_header_buffer + DataBuffer

    def serial(self):
        for defaultstore in self.fields:
            vValue = b''
            vfields = {vf.Offset: vf for vf in self.fields[defaultstore]}
            i = 0
            while i < self.mTotalSize:
                if i in vfields:
                    vfield = vfields[i]
                    vValue += VariableMgr.PACK_VARIABLES_DATA(
                        vfield.Value, vfield.Type)
                    i += vfield.Size
                else:
                    vValue += VariableMgr.PACK_VARIABLES_DATA(0, 'UINT8')
                    i += 1

            self.mValue[defaultstore] = vValue
        standard_default = self.mValue[0]
        standard_default_data_array = ()
        for item in range(len(standard_default)):
            standard_default_data_array += unpack("B",
                                                  standard_default[item:item + 1])
        for defaultid in self.mValue:
            if defaultid == 0:
                continue
            others_default = self.mValue[defaultid]
            others_data_array = ()
            for item in range(len(others_default)):
                others_data_array += unpack("B",
                                            others_default[item:item + 1])
            data_delta = VariableMgr.calculate_delta(
                standard_default_data_array, others_data_array)
            self.delta[defaultid] = [list(item) for item in data_delta]
            
    def PrintValue(self):
        extendtypes = self.cDefs.ExpandTypes()[self.mType]
        TotalByteArray = []
        with open("%sstructurepcd.dsc" % self.mName, "w") as fd:
            for defaultstore in self.fields:
                if defaultstore >0:
                    break
                fields = {item.Offset: item for item in self.fields[defaultstore]}
                for item in extendtypes:
                    if item['Offset'] in fields:
                        fd.write("%s.%s = %s\n" % (self.mName, item['Name'], hex(fields[item['Offset']].Value)))
                        TotalByteArray.append(hex(fields[item['Offset']].Value))
                    else:
                        fd.write("%s.%s = %s\n" % (self.mName, item['Name'], 0x0))
                        TotalByteArray.append('0x00')
        with open("%sVariableValue.txt" % self.mName, "w") as fd:
            fd.write(", ".join(TotalByteArray))

class GenNvStore():
    def __init__(self):
        self.NvVarInfo = []

    def LoadNvVariableInfo(self, VarInfoFile):
        with open(VarInfoFile, "r") as fd:
            data = json.load(fd)

        DataStruct = data.get("DataStruct", {})
        Data = data.get("Data")
        VarDefine = data.get("VarDefine")
        VarAttributes = data.get("DataStructAttribute")
        
        cStructDefs = CStruct(DataStruct)

        VarDataDict = {}
        for vardata in Data:
            VarDataDict.setdefault(
                (vardata['VendorGuid'], vardata["VarName"]), []).append(vardata)

        for guid, varname in VarDataDict:
            v = Variable()
            v.guid = guid
            vardef = VarDefine.get(varname)
            v.attributes = vardef['Attributes']
            v.mType = vardef['Type']
            v.mAlign = VarAttributes[v.mType]['Alignment']
            v.mTotalSize = VarAttributes[v.mType]['TotalSize']
            v.Struct = DataStruct[v.mType]
            v.mName = varname
            v.cDefs = cStructDefs
            for fieldinfo in VarDataDict.get((guid, varname), []):
                vf = VarField()
                vf.Offset = fieldinfo['Offset']
                vf.Value = fieldinfo['Value']
                vf.Size = fieldinfo['Size']
                v.fields.setdefault(int(fieldinfo['DefaultStore'],10), []).append(vf)
            v.serial()
            v.pack()
            self.NvVarInfo.append(v)

    def pack(self):
        NvStoreDataBufferSize = sum([v.mTotalSize for v in self.NvVarInfo])
        variable_storage_header_buffer = VariableMgr.PACK_VARIABLE_STORE_HEADER(
            NvStoreDataBufferSize + 28)

        defaultid_set = set()
        NvStoreDataBuffer = b''
        offset = NvStorageHeaderSize
        for v in self.NvVarInfo:
            NvStoreDataBuffer += v.mBin[0]
            offset += VariableHeaderSize + 2*(len(v.mName) + 1)

            for other_default in v.delta:
                if other_default == 0:
                    continue
                for delta_data in v.delta[other_default]:
                    delta_data[0] = delta_data[0] + offset
                defaultid_set.add(other_default)

        nv_default_part = VariableMgr.AlignData(VariableMgr.PACK_DEFAULT_DATA(
            0, 0, VariableMgr.unpack_data(variable_storage_header_buffer + NvStoreDataBuffer)), 8)

        data_delta_structure_buffer = bytearray()
        for defaultid in defaultid_set:
            delta_data_set = []
            for v in self.NvVarInfo:
                for item in v.delta[defaultid]:
                    delta_data_set.extend(item)
                data_delta_structure_buffer += VariableMgr.AlignData(
                    VariableMgr.PACK_DELTA_DATA(0, defaultid, v.delta[defaultid]), 8)

        size = len(nv_default_part + data_delta_structure_buffer) + 16
        NV_Store_Default_Header = VariableMgr.PACK_NV_STORE_DEFAULT_HEADER(
            size, size)

        return NV_Store_Default_Header + nv_default_part + data_delta_structure_buffer


if __name__ == "__main__":
    nvinfo = r"D:\BobEdk2\SocketSetupForms_debug.json"
    genNV = GenNvStore()
    genNV.LoadNvVariableInfo(nvinfo)
    with open("NvStore.bin", "wb") as fd:
        fd.write(genNV.pack())
        
#     for v in genNV.NvVarInfo:
#         filename = v.mName + ".bytearray"
#         with open(filename,"w") as fd:
#             fd.write(",".join(["0x%02x" % unpack("B", v.mValue[0][b:b+1])[0] for b in range(len(v.mValue[0]))]))

    for v in genNV.NvVarInfo:
        v.PrintValue()
        
if __name__ == "__main__2":
    VarInfoFile = r"D:\BobEdk2\SocketSetupForms_debug.json"
    with open(VarInfoFile, "r") as fd:
        data = json.load(fd)

    DataStruct = data.get("DataStruct", {})
    cstruct = CStruct(DataStruct)
    print (cstruct.CalStuctSize("UINT8"))
    print (cstruct.CalStuctSize("UINT8[10]"))
    print (cstruct.CalStuctSize("MEM_BOOT_HEALTH_CONFIG"))
    print (cstruct.CalStuctSize("IIO_STACK_CONF"))
    print (cstruct.CalStuctSize("IIO_SOCKET_CONF"))
    print (cstruct.CalStuctSize("SOCKET_IIO_CONFIGURATION"))
    print (cstruct.CalStuctSize("IIO_SOCKET_CONF[4]"))
    rt = cstruct.ExpandTypes()
    for item in rt['SOCKET_IIO_CONFIGURATION']:
        if "Socket" in item['Name']:
            print(item)