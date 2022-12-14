# -*- coding: UTF-8 -*-

import os
import re

from common.KFLog import kfLog

htmlHead = """
<html5>
    <head>
        <meta charset="GBK">
        <title>Automation Report</title>
        <style type="text/css">
            body {
                font-family: Monaco, 'Lucida Console', monospace;
                font-size: 14px;
                line-height: 28px;
            }
            xmp {
                font-family: 'Comic Sans MS', cursive;
                font-size: 12px
            }
            .failed {
                color: red;
                font-weight: bold;
            }    
            .succeeded {
                color: green;
                font-weight: bold;
            }     
            .testcase {
                font-size: 16px;
                // color: blue;
                font-weight: bold;
                cursor: pointer;                
            }
            .teststep {
                color: #660000;
                font-weight: bold;
                cursor: pointer;                
                // font-style: italic;
            }
            .request {
                color: #FF9900;
                cursor: pointer;                
            }
            .clear {
                font-weight: bold;
                font-style: italic;
                cursor: pointer;                
            }
        </style>
        <script>
            function changeColor(index) {
                var x = document.getElementById(index);
                if (document.getElementById('collapse_'+index).style.display === 'none') {
                    // x.style.color = '#FF3399';
                    // x.style.backgroundColor = '#FFFF99';
                    x.style.textShadow = '-1px -1px 1px #000, 1px 1px 1px #fff';
                } else {
                    // x.style.color = '#FF9900';
                    // x.style.backgroundColor = '';
                    x.style.textShadow = '';
                }
            }

            function displayToggle(index) {
                var x = document.getElementById(index)
                if (document.getElementById(index).style.display === 'none') {
                    x.style.display = '';
                } else {
                    x.style.display = 'none';
                }
            }

        </script>
    </head>
<body>
"""
htmlTail = """
    </body>
</html5>
"""


def logToHtml():
    """
    ???txt???????????????????????????html??????
    """

    # ??? .log ??????????????? .html
    logfile = os.path.join("logs", kfLog.datetime, "report.log")
    htmlfile = os.path.join("logs", kfLog.datetime, "report.html")

    newfile = open(htmlfile, 'w+')
    newfile.write(htmlHead)

    # ?????????????????? (????????????????????????)
    prefixLenght = 26

    testcaseIndex = 1
    teststepIndex = 1
    requestIndex = 1
    clearEnvIndex = 1

    succeededNum = 0
    failedNum = 0

    with open(logfile, 'r', encoding='gbk') as f:

        # ???????????????????????????display:none
        isXmlPdu = False
        isRequest = False
        isTestCase = False
        isTestStep = False
        isClearEnviroment = False

        for line in f:
            # ????????? XML ?????? XML ??????
            ### start of XML
            if line.find("<SetRequest>") > -1 or line.find("<SetResponse>") > -1 or line.find(
                    "<GetRequest>") > -1 or line.find("<GetResponse>") > -1 or line.find(
                    "<ActionRequest") > -1 or line.find("<ActionResponse") > -1:
                line = "<xmp>" + line

            ### end of XML
            elif line.find("</SetRequest>") > -1 or line.find("</SetResponse>") > -1 or line.find(
                    "</GetRequest>") > -1 or line.find("</GetResponse>") > -1 or line.find(
                    "</ActionRequest") > -1 or line.find("</ActionResponse") > -1:
                line = line + "</xmp>"


            # elif not re.match('\s*<', line):
            elif line.find("<") == -1 or line.find(">") == -1:

                # ??????????????????????????????????????????
                # if not re.match('\d{4}-\d{2}-\d{2}', line):
                if not re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', line):
                    if re.match('\s*[{|}]', line):
                        line = '&nbsp;' * prefixLenght + line
                    else:
                        # ???????????????????????????4???
                        if len(line.strip()) > 0:
                            line = '&nbsp;' * (int(prefixLenght) + 4) + line

                else:
                    # ???XML????????????????????????"<" ??? ">"????????????????????????????????????
                    line = re.sub('<', '&lt;', line)
                    line = re.sub('>', '&gt;', line)

                # testcase name
                if re.search('TestCase', line):

                    # failed testcase
                    if re.search('TestCase:.*\\*\\*\\* failed! \\*\\*\\*', line, re.I):
                        line = line[:prefixLenght] + "<span class='failed'>" + line[
                                                                               prefixLenght:] + '</span>' + '</div>'
                        if isClearEnviroment:
                            line = '</div><br />' + line
                            isClearEnviroment = False

                        if isTestCase:
                            # line += '</div>'
                            line = '</div><br />' + line
                            isTestCase = False

                        # ??????????????????????????????
                        if not re.search('TestCase:\s+setup', line, re.I) and not re.search('TestCase:\s+teardown',
                                                                                            line, re.I):
                            failedNum += 1

                    # succeeded testcase
                    elif re.search('TestCase:.*\\*\\*\\* succeeded! \\*\\*\\*', line, re.I):
                        line = line[:prefixLenght] + "<span class='succeeded'>" + line[
                                                                                  prefixLenght:] + '</span>' + '</div>'
                        if isClearEnviroment:
                            line = '</div><br />' + line
                            isClearEnviroment = False

                        if isTestCase:
                            # line += '</div>'
                            line = '</div><br />' + line
                            isTestCase = False

                        # ??????????????????????????????
                        if not re.search('TestCase:\s+setup', line, re.I) and not re.search('TestCase:\s+teardown',
                                                                                            line, re.I):
                            succeededNum += 1


                    # testcase info
                    else:
                        line = line[
                               :prefixLenght] + f"<span class='testcase' id='testcase{testcaseIndex}' onclick='changeColor(\"testcase{testcaseIndex}\"); displayToggle(\"collapse_testcase{testcaseIndex}\")'>" + line[
                                                                                                                                                                                                                  prefixLenght:] + '</span>'
                        line += f'<div id="collapse_testcase{testcaseIndex}" style="display:none">'
                        testcaseIndex += 1
                        isTestCase = True

                # teststep
                if re.search("step\d+", line, re.I):
                    if re.search('\\*Succeeded!\\*', line, re.I):
                        line = line[:prefixLenght] + f"<span class='succeeded'>" + line[prefixLenght:] + '</span>'
                    if re.search('\\*Failed!\\*', line, re.I):
                        line = line[:prefixLenght] + f"<span class='failed'>" + line[prefixLenght:] + '</span>'

                    # ???????????????`Succeeded`???`Failed`???, ????????????`teststep title`
                    if not re.search('\\*Succeeded!\\*', line, re.I) and not re.search('\\*Failed!\\*', line, re.I):
                        line = line[
                               :prefixLenght] + f"<span class='teststep' id='teststep{teststepIndex}' onclick='changeColor(\"teststep{teststepIndex}\"); displayToggle(\"collapse_teststep{teststepIndex}\")'>" + line[
                                                                                                                                                                                                                  prefixLenght:] + '</span><br/>'
                        line += f'<div id="collapse_teststep{teststepIndex}" style="display:none">'
                        isTestStep = True
                        teststepIndex += 1

                    if re.search('\\*Succeeded!\\*', line, re.I) or re.search('\\*Failed!\\*', line, re.I):
                        if isTestStep:
                            line = '</div>' + line
                            isTestStep = False

                # PDU & XML (start)
                if re.search('## Request  ##', line):
                    line = re.sub('## Request  ##', '##&nbsp;Request&nbsp;&nbsp;##', line)
                    line = line[
                           :prefixLenght] + f"<span class='request' id='request{requestIndex}' onclick='changeColor(\"request{requestIndex}\"); displayToggle(\"collapse_request{requestIndex}\")'>" + line[
                                                                                                                                                                                                       prefixLenght:] + '</span>'
                    isXmlPdu = True
                    isRequest = True

                # ??????  ## Request ##  Data ???????????????????????????
                if isXmlPdu and re.match('\d{4}-\d{2}-\d{2}', line):
                    line += f'<div id="collapse_request{requestIndex}" style="display:none">'
                    requestIndex += 1
                    isXmlPdu = False

                # PDU & XML (end)
                if re.search('## Response ##', line):
                    if isRequest:
                        line = '</div><br />' + line
                        isRequest = False

                # Clear enviroment
                if re.search('\*\*\s+Clear Environment\s+\*\*', line, re.I):

                    indentation = 0
                    if isRequest:
                        line = '<br/></div>' + line
                        isRequest = False
                        indentation += 11

                    if isTestStep:
                        line = '<br/></div>' + line
                        isTestStep = False
                        indentation += 11

                    line = line[:(
                                prefixLenght + indentation)] + f"<span class='clear' id='clear{clearEnvIndex}' onclick='changeColor(\"clear{clearEnvIndex}\"); displayToggle(\"collapse_clear{clearEnvIndex}\")'>" + line[
                                                                                                                                                                                                                     (
                                                                                                                                                                                                                                 prefixLenght + indentation):] + '</span>'
                    line += f'<div id="collapse_clear{clearEnvIndex}" style="display:none">'
                    clearEnvIndex += 1
                    isClearEnviroment = True

                # ??????log????????????????????????
                if re.search('Test Result', line, re.I) or re.search('Final Result', line, re.I):
                    break

                # ?????????????????????????????????
                line = line.strip() + "<br />"
            newfile.write(line)

    # ??????HTML?????????????????????
    newfile.write('<br/>--------------------------------------- Statistic ---------------------------------------<br/>')
    statistic = '&nbsp;' * 28
    statistic += f'Total: {failedNum + succeededNum}, Succeeded: {succeededNum}, Failed: <span style="color: red; font-weight: bold;">{failedNum}</span>'
    statistic += '<br/><br/><br/>'
    newfile.write(statistic)

    newfile.write(htmlTail)
    newfile.close()


if __name__ == '__main__':
    logToHtml()
