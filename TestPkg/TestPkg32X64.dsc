## @file
#  EFI/Framework Open Virtual Machine Firmware (OVMF) platform
#
#  Copyright (c) 2006 - 2019, Intel Corporation. All rights reserved.<BR>
#  (C) Copyright 2016 Hewlett Packard Enterprise Development LP<BR>
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#
##

################################################################################
#
# Defines Section - statements that will be processed to create a Makefile.
#
################################################################################
[Defines]
  PLATFORM_NAME                  = Ovmf
  PLATFORM_GUID                  = 5a9e7754-d81b-49ea-85ad-69eaa7b1539b
  PLATFORM_VERSION               = 0.1
  DSC_SPECIFICATION              = 0x00010005
  OUTPUT_DIRECTORY               = Build/TestPkg3264
  SUPPORTED_ARCHITECTURES        = IA32|X64
  BUILD_TARGETS                  = NOOPT|DEBUG|RELEASE
  SKUID_IDENTIFIER               = DEFAULT
  FLASH_DEFINITION               = TestPkg/TestIa32X64.fdf

  #
  # Defines for default states.  These can be changed on the command line.
  # -D FLAG=VALUE
  #
  DEFINE SECURE_BOOT_ENABLE      = FALSE
  DEFINE SMM_REQUIRE             = FALSE
  DEFINE SOURCE_DEBUG_ENABLE     = FALSE
  DEFINE TPM_ENABLE              = FALSE
  DEFINE TPM_CONFIG_ENABLE       = FALSE

  #
  # Network definition
  #
  DEFINE NETWORK_TLS_ENABLE             = FALSE
  DEFINE NETWORK_IP6_ENABLE             = FALSE
  DEFINE NETWORK_HTTP_BOOT_ENABLE       = FALSE
  DEFINE NETWORK_ALLOW_HTTP_CONNECTIONS = TRUE

!include NetworkPkg/NetworkDefines.dsc.inc

  #
  # Device drivers
  #
  DEFINE PVSCSI_ENABLE           = TRUE
  DEFINE MPT_SCSI_ENABLE         = TRUE

  #
  # Flash size selection. Setting FD_SIZE_IN_KB on the command line directly to
  # one of the supported values, in place of any of the convenience macros, is
  # permitted.
  #
!ifdef $(FD_SIZE_1MB)
  DEFINE FD_SIZE_IN_KB           = 1024
!else
!ifdef $(FD_SIZE_2MB)
  DEFINE FD_SIZE_IN_KB           = 2048
!else
!ifdef $(FD_SIZE_4MB)
  DEFINE FD_SIZE_IN_KB           = 4096
!else
  DEFINE FD_SIZE_IN_KB           = 4096
!endif
!endif
!endif

!include buildoptions.dsc

################################################################################
#
# SKU Identification section - list of all SKU IDs supported by this Platform.
#
################################################################################
[SkuIds]
  0|DEFAULT

!include LibraryClass.dsc

[PcdsDynamicDefault]
  gEfiMdeModulePkgTokenSpaceGuid.PcdSmbiosVersion|0x0208
  gEfiMdeModulePkgTokenSpaceGuid.PcdSmbiosDocRev|0x0
  gUefiOvmfPkgTokenSpaceGuid.PcdQemuSmbiosValidated|FALSE
  gEfiMdePkgTokenSpaceGuid.PcdPlatformBootTimeOut|0
  # Set memory encryption mask
  gEfiMdeModulePkgTokenSpaceGuid.PcdPteMemoryEncryptionAddressOrMask|0x0

  # Noexec settings for DXE.
  gEfiMdeModulePkgTokenSpaceGuid.PcdSetNxForStack|FALSE
  gEfiMdeModulePkgTokenSpaceGuid.PcdEmuVariableNvStoreReserved|0
  gUefiCpuPkgTokenSpaceGuid.PcdCpuBootLogicalProcessorNumber|0
  gUefiCpuPkgTokenSpaceGuid.PcdCpuMaxLogicalProcessorNumber|64
  gEfiMdeModulePkgTokenSpaceGuid.PcdAcpiS3Enable|FALSE
  gEfiMdeModulePkgTokenSpaceGuid.PcdPciDisableBusEnumeration|FALSE
!if $(SMM_REQUIRE) == FALSE
  gEfiMdeModulePkgTokenSpaceGuid.PcdFlashNvStorageVariableBase64|0
  gEfiMdeModulePkgTokenSpaceGuid.PcdFlashNvStorageFtwWorkingBase|0
  gEfiMdeModulePkgTokenSpaceGuid.PcdFlashNvStorageFtwSpareBase|0
!endif

################################################################################
#
# Components Section - list of all EDK II Modules needed by this Platform.
#
################################################################################
[Components.IA32]
  TestPkg/ResetVector/ResetVector.inf

  #
  # SEC Phase modules
  #
  TestPkg/Sec/SecMain.inf {
    <LibraryClasses>
    NULL|MdeModulePkg/Library/LzmaCustomDecompressLib/LzmaCustomDecompressLib.inf
  }

  #
  # PEI Phase modules
  #
  MdeModulePkg/Core/Pei/PeiMain.inf
  MdeModulePkg/Universal/PCD/Pei/Pcd.inf  {
    <LibraryClasses>
      PcdLib|MdePkg/Library/BasePcdLibNull/BasePcdLibNull.inf
  }

  MdeModulePkg/Core/DxeIplPeim/DxeIpl.inf
  UefiCpuPkg\CpuMpPei\CpuMpPei.inf
#  TestPkg/PlatformPei/PlatformPei.inf


[Components.X64]
  #
  # DXE Phase modules
  #
  MdeModulePkg/Core/Dxe/DxeMain.inf {
    <LibraryClasses>
      NULL|MdeModulePkg/Library/LzmaCustomDecompressLib/LzmaCustomDecompressLib.inf
      DevicePathLib|MdePkg/Library/UefiDevicePathLib/UefiDevicePathLib.inf
  }
  UefiCpuPkg\CpuDxe\CpuDxe.inf
   
  MdeModulePkg/Universal/PCD/Dxe/Pcd.inf  {
   <LibraryClasses>
      PcdLib|MdePkg/Library/BasePcdLibNull/BasePcdLibNull.inf
  }

  MdeModulePkg/Core/RuntimeDxe/RuntimeDxe.inf

  MdeModulePkg/Logo/LogoDxe.inf
  MdeModulePkg/Application/UiApp/UiApp.inf {
    <LibraryClasses>
      NULL|MdeModulePkg/Library/DeviceManagerUiLib/DeviceManagerUiLib.inf
      NULL|MdeModulePkg/Library/BootManagerUiLib/BootManagerUiLib.inf
      NULL|MdeModulePkg/Library/BootMaintenanceManagerUiLib/BootMaintenanceManagerUiLib.inf
!ifdef $(CSM_ENABLE)
      NULL|TestPkg/Csm/LegacyBootManagerLib/LegacyBootManagerLib.inf
      NULL|TestPkg/Csm/LegacyBootMaintUiLib/LegacyBootMaintUiLib.inf
!endif
  }
  FatPkg/EnhancedFatDxe/Fat.inf
  TestPkg/AcpiTables/AcpiTables.inf
