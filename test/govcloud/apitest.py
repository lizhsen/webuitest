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
# Date:   Aug 2017

import requests
import pyodbc
import operator
import unittest
import time
import xlrd
from ddt import ddt, data, file_data, unpack

registerurl = 'http://localhost:3000/v1/join'
tokenurl = 'http://localhost:3000/v1/login'


# 链接sql server，获取sql结果
def sqlop(requestdata, sql):
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0}; \
        SERVER=127.0.0.1,1433;DATABASE=citydata;UID=citydata;PWD=citydata')
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    rowdate = list(row)
    jsondata = list(requestdata.values())
    print("return sql result: %s" % row)
    print("insert data: %s" % str(jsondata))
    result = operator.eq(rowdate, jsondata)
    return result


# 读取excel数据
def readexcel(file_path):
    try:
        # 打开excel
        book = xlrd.open_workbook(file_path)
    except Exception as err:
        # 如果路径不在或者excel不正确，返回报错信息
        print('路径不存在或者excel不正确')
        print(err)
    else:
        # 取第一个sheet页
        sheet = book.sheet_by_index(0)
        # 取这个sheet页的所有行数
        rows = sheet.nrows
        case_list = []
        for i in range(rows):
            if i != 0:
                # 把每一条测试用例添加到case_list中
                case_list.append(sheet.row_values(i)[3:])
        return case_list


@ddt
class Apitest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        registerdata = {"login": "zhuzhu1356", "password": "123456"}
        registerdata["login"] = "user" + str(int(time.time()))

        # register user
        r = requests.post(registerurl, data=registerdata)
        if r.status_code == 200:
            res = eval(r.text)
            assert len(res) == 2
            assert operator.eq(list(res.keys()), ["code", "data"])
            assert str(res["code"]) == "202"
            print("register user success")
        else:
            print(r.text)
            return "register user error"

        # get token
        r = requests.post(tokenurl, data=registerdata)
        if r.status_code == 200:
            res = eval(r.text)
            assert len(res) == 2
            assert operator.eq(list(res.keys()), ["code", "data"])
            assert str(res["code"]) == "203"
            print("get token success")
            self.token = res["data"]
        else:
            print(r.text)
            return "get token error"

    @classmethod
    def tearDownClass(self):
        pass

    @data(*readexcel("testcase.xlsx"))
    @unpack
    def test_insert_data(self, url, requestbody, responsebody, sql):
        reqbody = eval(requestbody)
        resbody = eval(responsebody)
        reqbody["token"] = self.token
        r = requests.post(url, data=reqbody)
        print(r.text)
        if r.status_code == 200:
            res = eval(r.text)
            assert operator.eq(res, resbody)
            assert sqlop(eval(requestbody), sql)
            print("insert data success!")
        else:
            print("insert data fail!")
            print(r.text)
            assert False
        return r.status_code

if __name__ == '__main__':
    unittest.main()
