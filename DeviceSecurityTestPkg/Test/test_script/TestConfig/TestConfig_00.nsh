FS0:
mkdir test_output
load Tcg2Stub.efi
DeployCert.efi -T 00
load DeviceSecurityPolicyStub.efi
load PciIoStub.efi
#load PciIoPciDoeStub.efi
load SpdmStub.efi
#load SpdmPciDoeStub.efi
load SpdmDeviceSecurityDxe.efi
TestSpdm.efi
Tcg2DumpLog.efi > test_output\log\TestConfig_00.log
reset -s