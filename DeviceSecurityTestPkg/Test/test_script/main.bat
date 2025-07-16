@echo off
REM py -3 launch_test.py
@REM py -3 launch_test_coverage.py
@REM py -3 launch_test.py
py -3 launch_test_coverage.py

SET cwd=%~dp0

echo %cwd%


SET build=Build\EmulatorX64\DEBUG_VS2019\X64\test_output
SET mainpwd=%cwd:DeviceSecurityTestPkg\Test\test_script\=%

echo %mainpwd%

SET test_output=%mainpwd%%build%

echo %test_output%

if not exist %test_output%\result mkdir %test_output%\result

echo "check the keyword in log file"
py -3 find_keyword.py %test_output%\log\TestConfig_00.log keyword\keywordTestConfig_00.txt > %test_output%\result\ResultTestConfig_00.txt
py -3 find_keyword.py %test_output%\log\TestConfig_01.log keyword\keywordTestConfig_01.txt > %test_output%\result\ResultTestConfig_01.txt
py -3 find_keyword.py %test_output%\log\TestConfig_02.log keyword\keywordTestConfig_02.txt > %test_output%\result\ResultTestConfig_02.txt
py -3 find_keyword.py %test_output%\log\TestConfig_03.log keyword\keywordTestConfig_03.txt > %test_output%\result\ResultTestConfig_03.txt
py -3 find_keyword.py %test_output%\log\TestConfig_04.log keyword\keywordTestConfig_04.txt > %test_output%\result\ResultTestConfig_04.txt
py -3 find_keyword.py %test_output%\log\TestConfig_05.log keyword\keywordTestConfig_05.txt > %test_output%\result\ResultTestConfig_05.txt
py -3 find_keyword.py %test_output%\log\TestConfig_06.log keyword\keywordTestConfig_06.txt > %test_output%\result\ResultTestConfig_06.txt
py -3 find_keyword.py %test_output%\log\TestConfig_07.log keyword\keywordTestConfig_07.txt > %test_output%\result\ResultTestConfig_07.txt
py -3 find_keyword.py %test_output%\log\TestConfig_08.log keyword\keywordTestConfig_08.txt > %test_output%\result\ResultTestConfig_08.txt
py -3 find_keyword.py %test_output%\log\TestConfig_09.log keyword\keywordTestConfig_09.txt > %test_output%\result\ResultTestConfig_09.txt
py -3 find_keyword.py %test_output%\log\TestConfig_10.log keyword\keywordTestConfig_10.txt > %test_output%\result\ResultTestConfig_10.txt
py -3 find_keyword.py %test_output%\log\TestConfig_11.log keyword\keywordTestConfig_11.txt > %test_output%\result\ResultTestConfig_11.txt
py -3 find_keyword.py %test_output%\log\TestConfig_12.log keyword\keywordTestConfig_12.txt > %test_output%\result\ResultTestConfig_12.txt
py -3 find_keyword.py %test_output%\log\TestConfig_13.log keyword\keywordTestConfig_13.txt > %test_output%\result\ResultTestConfig_13.txt
py -3 find_keyword.py %test_output%\log\TestConfig_14.log keyword\keywordTestConfig_14.txt > %test_output%\result\ResultTestConfig_14.txt
py -3 find_keyword.py %test_output%\log\TestConfig_15.log keyword\keywordTestConfig_15.txt > %test_output%\result\ResultTestConfig_15.txt
py -3 find_keyword.py %test_output%\log\TestConfig_16.log keyword\keywordTestConfig_16.txt > %test_output%\result\ResultTestConfig_16.txt
py -3 find_keyword.py %test_output%\log\TestConfig_17.log keyword\keywordTestConfig_17.txt > %test_output%\result\ResultTestConfig_17.txt
py -3 find_keyword.py %test_output%\log\TestConfig_18.log keyword\keywordTestConfig_18.txt > %test_output%\result\ResultTestConfig_18.txt
py -3 find_keyword.py %test_output%\log\TestConfig_19.log keyword\keywordTestConfig_19.txt > %test_output%\result\ResultTestConfig_19.txt
py -3 find_keyword.py %test_output%\log\TestConfig_20.log keyword\keywordTestConfig_20.txt > %test_output%\result\ResultTestConfig_20.txt
py -3 find_keyword.py %test_output%\log\TestConfig_21.log keyword\keywordTestConfig_21.txt > %test_output%\result\ResultTestConfig_21.txt
py -3 find_keyword.py %test_output%\log\TestConfig_22.log keyword\keywordTestConfig_22.txt > %test_output%\result\ResultTestConfig_22.txt
py -3 find_keyword.py %test_output%\log\TestConfig_23.log keyword\keywordTestConfig_23.txt > %test_output%\result\ResultTestConfig_23.txt
py -3 find_keyword.py %test_output%\log\TestConfig_24.log keyword\keywordTestConfig_24.txt > %test_output%\result\ResultTestConfig_24.txt
py -3 find_keyword.py %test_output%\log\TestConfig_25.log keyword\keywordTestConfig_25.txt > %test_output%\result\ResultTestConfig_25.txt

echo "Generate the Test Report"
py -3 Generate_Report.py
