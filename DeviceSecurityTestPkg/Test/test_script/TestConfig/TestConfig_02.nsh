FS0:
mkdir test_output
load Tcg2Stub.efi
DeployCert.efi -T 02
load DeviceSecurityPolicyStub.efi
load PciIoStub.efi
load SpdmStub.efi
load SpdmDeviceSecurityDxe.efi
TestSpdm.efi
Tcg2DumpLog.efi > test_output\log\TestConfig_02.log
reset -s