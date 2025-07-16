import os
import sys

def get_env():
    build_date = ''
    build_time = ''    
    edk2_version = ''
    
    pkg = os.getcwd()
    pwd = pkg.split("DeviceSecurityTestPkg")[0]
    filepath =os.path.join(pwd,r'Build\EmulatorX64\DEBUG_VS2019\X64\test_output\env.txt')
    print("filepath %s " % filepath)
    if not os.path.isfile(filepath):
        print("Generate_Report: %s is not file" % filepath)
        sys.exit()

    with open(filepath, 'r') as f:
        lines = f.readlines()
        build_date = lines[0]
        build_time = lines[1]
        edk2_version = lines[2]

    return build_date, build_time, edk2_version

def read_result():
    total_passnum = 0
    total_failnum = 0
    table_head = '<br><div class = "listheadNBG"> {}: </div><table class = "zoomStyle" border="0" cellspacing="1" cellpadding="1">' \
                 '<tr><th>No.</th><th>Test Case</th><th>Result</th></tr>'
    str_row = '<tr><td>%d</td><td class = "styleLeft">%s</td><td>%s</td></tr>'
    summary_row_format = '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'
    pkg = os.getcwd()
    pwd = pkg.split("DeviceSecurityTestPkg")[0]
    
    out_SPDM_path =os.path.join(pwd,r'Build\EmulatorX64\DEBUG_VS2019\X64\test_output\result')
    SPDM_content = ''
    SPDM_content += table_head.format('Test Case List')
    SPDM_NUM = 1
    for file in os.listdir(out_SPDM_path):
        configuration_SPDM = file.split('.')[0]
        with open(os.path.join(out_SPDM_path, file), 'r') as f:
            content = f.read()
            if 'So this test case passed' in content:
                total_passnum += 1
                SPDM_content += str_row%(SPDM_NUM, configuration_SPDM, 'PASS')
            else:
                total_failnum += 1
                SPDM_content += str_row%(SPDM_NUM, configuration_SPDM, 'FAIL')
            f.close()
        SPDM_NUM += 1
    SPDM_content += '</table>'

    summary_row = summary_row_format.format('UEFI Test stub as SPDM responder', total_passnum, total_failnum, total_passnum + total_failnum)
    return summary_row, SPDM_content

# Change the row background color for tables.
def insert_bgcolor(table_content):
    ls = table_content.split('<tr')
    updated_table = ''
    for i in range(len(ls)):
        if "</th>".lower() in ls[i].lower():
            updated_table = updated_table + "<tr " + ls[i]
            continue
        elif i % 2 != 0:
            updated_table = updated_table + '''<tr style="background-color: #BDD6EE;"''' + ls[i]
        else:
            updated_table = updated_table + '<tr ' + ls[i]
    return updated_table

def main():
    test_title = '''<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            </head><div class = "pageTitle"> UEFI SPDM requester Test Report </div>'''
    build_date, build_time, edk2_version = get_env()
    time_div = "<div class='dateTag'><div class='dateHead'>Test Date: &nbsp</div><div class='dateValue'> {}</div></div>" \
               "<div classs='dateTag'><div class='dateHead'>Test Time: &nbsp</div><div class='timeValue'> {}</div></div>"
    time_div = time_div.format(build_date, build_time)
    version_table = '''<table class="zoomStyle" border="0"
                       cellspacing="1" cellpadding="1"><tr><th width="30%"> Repository</th><th width="30%">Branch</th><th width="40">Latest Commit</th></tr><tr><td width="20%" class="platBold">edk2-staging</td><td width="35%">DeviceSecurity</td><td>''' + edk2_version + '''</td></tr></table>'''
    summary_table = '''<table class="zoomStyle" border="0" cellspacing="1" cellpadding="1">
                        <tr><th>Configuration</th><th>Pass</th><th>Fail</th><th>Total</th></tr>{}</table><br>'''
    summary_row = ''
    summary_part,table_content_SPDM = read_result()
    summary_row +=summary_part
    summary_table = summary_table.format(summary_row)
    
    css_file = os.path.join(os.path.split(__file__)[0], 'Style.css')
    css_str = open(css_file, 'r').read()
    
    content = test_title+"<br>"+time_div+"<br>"+version_table+"<br>"+summary_table+table_content_SPDM+"<br>"
    update_content = insert_bgcolor(content)
    with open('SpdmTest_Report.html', 'w', encoding='utf-8') as f:
        f.write(css_str + update_content)


if __name__ == '__main__':
    main()