## @file
# generate capsule
#
#  Copyright (c) 2007-2018, Intel Corporation. All rights reserved.<BR>
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#

##
# Import Modules
#
from __future__ import absolute_import
from .GenFdsGlobalVariable import GenFdsGlobalVariable
from io import BytesIO
from struct import pack
import os
from Common.Misc import SaveFileOnChange
import uuid
from CommonDataClass.FdfClass import CapsuleData,CapsulePayloadData


## FFS class for capsule data
#
#
class CapsuleFfs:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self,data):
        self.data = data
    
    def __getattr__(self,item):
        return self.data.__dict__get(item)

    ## generate FFS capsule data
    #
    #   @param  self        The object pointer
    #   @retval string      Generated file name
    #
    def GenCapsuleSubItem(self):
        FfsFile = self.Ffs.GenFfs()
        return FfsFile

## FV class for capsule data
#
#
class CapsuleFv:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self,data):
        self.data = data
    
    def __getattr__(self,item):
        return self.data.__dict__.get(item)

    ## generate FV capsule data
    #
    #   @param  self        The object pointer
    #   @retval string      Generated file name
    #
    def GenCapsuleSubItem(self):
        if self.FvName.find('.fv') == -1:
            if self.FvName.upper() in GenFdsGlobalVariable.FdfParser.Profile.FvDict:
                FvObj = GenFdsGlobalVariable.FdfParser.Profile.FvDict[self.FvName.upper()]
                FdBuffer = BytesIO()
                FvObj.CapsuleName = self.CapsuleName
                FvFile = FvObj.AddToBuffer(FdBuffer)
                FvObj.CapsuleName = None
                FdBuffer.close()
                return FvFile
        else:
            FvFile = GenFdsGlobalVariable.ReplaceWorkspaceMacro(self.FvName)
            return FvFile

## FD class for capsule data
#
#
class CapsuleFd:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self,data):
        self.data = data
    
    def __getattr__(self,item):
        return self.data.__dict__.get(item)

    ## generate FD capsule data
    #
    #   @param  self        The object pointer
    #   @retval string      Generated file name
    #
    def GenCapsuleSubItem(self):
        if self.FdName.find('.fd') == -1:
            if self.FdName.upper() in GenFdsGlobalVariable.FdfParser.Profile.FdDict:
                FdObj = GenFdsGlobalVariable.FdfParser.Profile.FdDict[self.FdName.upper()]
                FdFile = FdObj.GenFd()
                return FdFile
        else:
            FdFile = GenFdsGlobalVariable.ReplaceWorkspaceMacro(self.FdName)
            return FdFile

## AnyFile class for capsule data
#
#
class CapsuleAnyFile:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self,data):
        self.data = data
    
    def __getattr__(self,item):
        return self.data.__dict__.get(item)

    ## generate AnyFile capsule data
    #
    #   @param  self        The object pointer
    #   @retval string      Generated file name
    #
    def GenCapsuleSubItem(self):
        return self.FileName

## Afile class for capsule data
#
#
class CapsuleAfile:
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self,data):
        self.data = data
    
    def __getattr__(self,item):
        return self.data.__dict__.get(item)

    ## generate Afile capsule data
    #
    #   @param  self        The object pointer
    #   @retval string      Generated file name
    #
    def GenCapsuleSubItem(self):
        return self.FileName

class CapsulePayload:
    
    def __init__(self,data):
        self.data = data
    
    def __getattr__(self,item):
        return self.data.__dict__.get(item)

    def GenCapsuleSubItem(self, AuthData=[]):
        if not self.Version:
            self.Version = '0x00000002'
        if not self.ImageIndex:
            self.ImageIndex = '0x1'
        if not self.HardwareInstance:
            self.HardwareInstance = '0x0'
        ImageFileSize = os.path.getsize(self.ImageFile)
        if AuthData:
            # the ImageFileSize need include the full authenticated info size. From first bytes of MonotonicCount to last bytes of certificate.
            # the 32 bit is the MonotonicCount, dwLength, wRevision, wCertificateType and CertType
            ImageFileSize += 32
        VendorFileSize = 0
        if self.VendorCodeFile:
            VendorFileSize = os.path.getsize(self.VendorCodeFile)

        #
        # Fill structure
        #
        Guid = self.ImageTypeId.split('-')
        Buffer = pack('=ILHHBBBBBBBBBBBBIIQ',
                       int(self.Version, 16),
                       int(Guid[0], 16),
                       int(Guid[1], 16),
                       int(Guid[2], 16),
                       int(Guid[3][-4:-2], 16),
                       int(Guid[3][-2:], 16),
                       int(Guid[4][-12:-10], 16),
                       int(Guid[4][-10:-8], 16),
                       int(Guid[4][-8:-6], 16),
                       int(Guid[4][-6:-4], 16),
                       int(Guid[4][-4:-2], 16),
                       int(Guid[4][-2:], 16),
                       int(self.ImageIndex, 16),
                       0,
                       0,
                       0,
                       ImageFileSize,
                       VendorFileSize,
                       int(self.HardwareInstance, 16)
                       )
        if AuthData:
            Buffer += pack('QIHH', AuthData[0], AuthData[1], AuthData[2], AuthData[3])
            Buffer += uuid.UUID(AuthData[4]).bytes_le

        #
        # Append file content to the structure
        #
        ImageFile = open(self.ImageFile, 'rb')
        Buffer += ImageFile.read()
        ImageFile.close()
        if self.VendorCodeFile:
            VendorFile = open(self.VendorCodeFile, 'rb')
            Buffer += VendorFile.read()
            VendorFile.close()
        self.Existed = True
        return Buffer
