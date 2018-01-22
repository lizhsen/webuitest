# coding:utf-8

# Copyright 2017 INESA (Group) Co., Ltd. R&D Center
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Author: zhounh@rc.dddd.com
# Date:   Oct 2017

"""
@file get_js.py
"""

##
# @addtogroup webui
# @brief This is webui component
# @{
# @addtogroup webui
# @brief This is webui module
# @{
##

from exescript import ExeJs
import sys
import json
import os
import re
import time
from logger import logger
from get_config import getconfig
reload(sys)
sys.setdefaultencoding('utf-8')
wait_time = int(getconfig("webui", "wait_time"))


class GetJs(object):
    """
    @class GetJs
    """
    def __init__(self, selenium_driver):
        self.driver = selenium_driver

    #decorator for cyclic to find element
    def circulation(wait_time):
        def decorator(func):
            def wrapper(*args, **kw):
                for i in range(wait_time):
                    time.sleep(1)
                    logger("DEBUG", "consume %d seconds already" %i)
                    res = func(*args, **kw)
                    if res != "" and res != "0":
                        return res
                return "null"
            logger("WARN", "failed to get value by js function")
            return wrapper
        return decorator

    @circulation(wait_time)
    def get_promptinfo(self, elementname):
        logger("DEBUG", "start to get prompt for %s" %elementname)
        path = os.path.split(os.path.realpath(__file__))[0]
        id_file = open(os.path.join(path, "element_id.json"))
        id_dict = json.load(id_file)
        res = ""
        if elementname in id_dict.keys():
            elementid = id_dict[elementname]
        else:
            logger("WARN", "element is not exist")
            assert False, "element is not exist"
        jssrc = "$('#elementid').next().text()"
        dictcont = {"elementid":elementid}
        exejs=ExeJs(driver=self.driver)
        exejs.exeWrap(jssrc,**dictcont)
        res = exejs.getMsg()
        logger("DEBUG", "get prompt finished, %s" %res)
        return res 
    
    # get value some row and some column
    @circulation(wait_time)
    def get_tdtext(self, elementstr):
        row_text = elementstr.split(u"行中")[0]
        col_text = elementstr.split(u"行中")[1].split(u"列")[0]
        logger("DEBUG", "row is %s, col is %s" %(row_text, col_text))
        jssrc = """(function(){
        var colindex = 0;
        var destval = "";
        var trs = document.getElementsByTagName("tr");
        var ths = trs[1].getElementsByTagName("th");
        for(var i=0; i<ths.length; i++) {
            var coltext1 = ths[i].childNodes[0].innerHTML
            var coltext2 = ths[i].innerHTML
            if($.trim(coltext1) == "colname" || $.trim(coltext2) == "colname"){
                    colindex = i;
                    break;
                }
            }
        for(var i=0; i<trs.length; i++) {
            var tds = trs[i].getElementsByTagName("td");
            for(var j=0; j<tds.length; j++){
                var rowtext = $.trim(tds[j].innerHTML)
                aindex = rowtext.indexOf("<a href")
                if(aindex != -1){
                    rowtext = tds[j].childNodes[0].innerHTML
                }
                if($.trim(rowtext) == "rowname"){
                    destval = $.trim(tds[colindex].innerHTML);
                    break;
                }
            }
            if(destval != ""){
                break;
            }
        }
        return destval;
        })()
        """
        dictcont = {"rowname": row_text, "colname": col_text}
        exejs=ExeJs(driver=self.driver)
        exejs.exeWrap(jssrc,**dictcont)
        res = exejs.getMsg()
        logger("DEBUG", "get tdtext finished, %s" %res)
        return res

    # get hint info of system
    @circulation(wait_time)
    def get_hintinfo(self):
        jssrc = """(function(){
        var arrinfo = new Array();
        var alerts = $(".messages").find("p");
        for(var i=0; i<alerts.length; i++){
            var pinfo = alerts[i].innerHTML;
            arrinfo.push(pinfo);
        }
        if(arrinfo.length != 0){
            return arrinfo;
        }
        var text = ''
        text = $("#update_project__update_quotas").children().find("li").first().text()
        if(text == ''){
           text = $(".errorlist").find("li").text()
        }
        return text;
        })()"""
        exejs=ExeJs(driver=self.driver)
        exejs.exeWrap(jssrc)
        res = exejs.getMsg()
        res = res.replace("<strong>", "")
        res = res.replace("</strong>", "")
        logger("DEBUG", "get hintinfo finished, %s" %res)
        return res

    # get element number on page
    @circulation(wait_time)
    def get_number(self, tabname):
        jssrc = """(function(){
        var num = 0;
        var trs = document.getElementsByTagName("tr");
        for(var i=0; i<trs.length; i++) {
            var tds = trs[i].getElementsByTagName("td");
            for(var j=1; j<tds.length; j++){
                var rowtext = tds[j].innerHTML
                aindex = rowtext.indexOf("<a href")
                if(aindex != -1){
                    rowtext = tds[j].childNodes[0].innerHTML
                }
                if($.trim(rowtext) == "rowname"){
                    num = num + 1;
                    break;
                }
            }
        }
        return num;
        })()
        """
        dictcont = {"rowname": tabname}
        exejs=ExeJs(driver=self.driver)
        exejs.exeWrap(jssrc,**dictcont)
        res = exejs.getMsg()
        logger("DEBUG", "get row number finished, %s" %res)
        return res

    # get text of tabname on detail page
    @circulation(wait_time)
    def get_details(self, tabname):
        jssrc = """(function(){
        var num = 0;
        var ddtext = '';
        var dts = document.getElementsByTagName("dt");
        for(var i=0; i<dts.length; i++) {
            var dtext = dts[i].innerHTML
            if(dtext == "tabname"){
                ddtext = dts[i].nextElementSibling.innerHTML;
                if(ddtext.indexOf("<a href") != -1){
                    ddtext = dts[i].nextElementSibling.childNodes[1].innerHTML;
                }
            }
        }
        return $.trim(ddtext);
        })()
        """
        dictcont = {"tabname": tabname}
        exejs=ExeJs(driver=self.driver)
        exejs.exeWrap(jssrc,**dictcont)
        res = exejs.getMsg()
        if tabname == 'Internal':
            res = res.split(';')
            get_ip = res[0]
            reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
            for ip in reip.findall(get_ip):
                res = ip
        logger("DEBUG", "get text of tabname on detail page finished, %s" %res)
        return res

    # 创建实例时，点击增加内网
    #@circulation(wait_time)
    def add_net(self, netname, check):
        # check arg is selected_network, available_network
        jssrc = """(function(){
                var net = "";
                var checknet = "check_network";
                lis = document.getElementById("check_network").getElementsByTagName("li")
                for(var i=0; i<lis.length; i++) {
                    lindex = lis[i].innerHTML.indexOf("netname")
                    if(lindex != -1){
                        if(checknet == "selected_network"){
                            net = "success";
                            break;
                        }
                        else if(checknet == "available_network"){
                            var element = lis[i].childNodes[2];
                            element.click();
                            net = "success";
                            break;
                        }
                        else{
                            return "check arg is error"
                        }
                    }
                }
                return net;
                })()
                """
        dictcont = {"netname": netname, "check_network": check}
        exejs = ExeJs(driver=self.driver)
        exejs.exeWrap(jssrc, **dictcont)
        res = exejs.getMsg()
        logger("INFO", "add network %s result is %s" % (netname, res))
        return res
##
# @}
# @}
##
