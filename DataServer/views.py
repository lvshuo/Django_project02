from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
import cx_Oracle
import json
from django.db import models
from DataServer.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework import exceptions
import datetime
from DataServer.database_login import database_login

# Create your views here.


address = '10.10.31.115:1521/orcl'
username = 'BJYJY'
password = 'abc@123'

data_effiency = {"CIRCLE_LOSS_EFFICIENCY": "CIRCLE_LOSS_EFFICIENCY",
                 "LINE_END_LOSS_EFFICIENCY": "LINE_END_LOSS_EFFICIENCY",
                 "FIRT_PRODUCT_LOSS_EFFICIENCY": "FIRT_PRODUCT_LOSS_EFFICIENCY",
                 "CHANGE_PN_LOSS_EFFICIENCY": "CHANGE_PN_LOSS_EFFICIENCY",
                 "CHANGE_WO_LOSS_EFFICIENCY": "CHANGE_WO_LOSS_EFFICIENCY",
                 "FAULT_LOSS_EFFICIENCY":  "FAULT_LOSS_EFFICIENCY",
                 "TOTAL_EFFICIENCY": "TOTAL_EFFICIENCY"}

data_to_check_final={"START_TIME":"START_TIME ",
                      "END_TIME":"END_TIME",
                     "ORG_CODE":"ORG_CODE",
                     #"PROJECT_ID":"PROJECT_ID",
                     "IS_STANDARD":"Y",
                     #"LINE_CODE":"LINE_CODE"
                   }
data_to_check_effiency={"START_TIME":"START_TIME ",
                        "END_TIME":"END_TIME",
                        "SERIES":"SERIES",
                        "AREA_NAME":"AREA_NAME",
                        "ORG_NAME":"ORG_NAME"}

class my_database_login(database_login):
    def __init__(self,address,username,password):
        database_login.__init__(self, address, username, password)
    def login(self):
        database_login.login(self)

database_temp=my_database_login(address,username,password)

conn2 = cx_Oracle.connect('BJYJY', 'abc@123', '10.10.31.115:1521/orcl')
cursor2 = conn2.cursor()

Token_list=[
    '123456',
    'abcdef',

]
def gettoken(request):
    data_to_send = {"status": "200", "msg": "No User", "data": "null"}
    token_list={"token0":Token_list[0],"token1":Token_list[1]}
    token={"token":token_list}
    data_to_send["msg"]="Token list"
    data_to_send["data"]=token_list
    return HttpResponse(json.dumps(data_to_send))

##Token 认证
class UserAuthview(BaseAuthentication):
    data_to_send = {"status": "200", "msg": "认证失败", "data": "null"}
    def authenticate(self, request):
        tk=request._request.GET.get("token")

        if tk in Token_list:
            return (tk,None)

        #return HttpResponse(json.dumps({"status": "200", "msg": "认证失败", "data": "null"}))
        raise exceptions.AuthenticationFailed({"status": "200", "msg": "Authenticate Failed", "data": "null"})
        #return HttpResponse(json.dumps(data_to_send))
    def authenticate_header(self, request):
        pass


class dbreadrest(APIView):
    authentication_classes = [UserAuthview, ]
    #permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        data_to_send = {"status": "400", "msg": "No User", "data": "null"}
        a = [1, 2, 3, 4, 5]
        data_to_send['data'] = a
        return HttpResponse(json.dumps(data_to_send))
        #return Response('POST请求，响应内容')

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

class getdata(APIView):
    authentication_classes = [UserAuthview, ]
   # authentication_classes = [TestAuthentication, ]
    #permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        print(request)
        return HttpResponse(get_efficiency_data(request))


    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

class getefficiency(APIView):
    authentication_classes = [UserAuthview, ]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        #get_project_list(request)
        #print(request)
        return HttpResponse(get_efficiency_data(request))

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

class getdatadetail(APIView):
    authentication_classes = [UserAuthview, ]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        #get_project_list(request)
        #print(request)
        return HttpResponse(get_data_detail(request))

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

def get_efficiency_data(request):

    data_json = json.loads(request.body)
    print(data_json)
    efficencys=['']
    data_to_send = {"status": "400", "msg": "No User", "data": "null"}
    data_get_orgnames_list = {"SERIES": "SERIES", "AREA_NAME": "AREA_NAME"}

    data_to_check_effiency["START_TIME"]=data_json["START_TIME"]
    data_to_check_effiency["END_TIME"]=data_json["END_TIME"]
    data_to_check_effiency["SERIES"]=data_json["SERIES"]

    data_get_orgnames_list["SERIES"]=data_json["SERIES"]
    data_get_orgnames_list["AREA_NAME"]=data_json["AREA_NAME"]

    cursor2.execute("select * from OLE_DB.RPT_LINE_DAILY_L where   WORK_DATE =TO_DATE('2018-07-06', 'YYYY-MM-DD') ")
    result = cursor2.fetchone()
    print(result)
    org_name=get_project_list(data_get_orgnames_list)
    print(org_name)
    if org_name ==0 :
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return json.dumps(res)
    else:

        for i in range(len(org_name)):

            data_to_check_effiency["ORG_NAME"]=org_name[i]
            efficencys.append(logindb(data_to_check_effiency))
        efficencys.remove('')
        print(efficencys)
        print(org_name+efficencys)
        data_to_send["status"] = "200"
        data_to_send["msg"] = "Data is ready"
        data_to_send["data"] = org_name+efficencys

        return json.dumps(data_to_send, ensure_ascii = False)

def get_data_detail(request):
    data_json = json.loads(request.body)
    print(data_json)
    data_to_check_org_code = {"ORG_NAME": "ORG_NAME"}
    data_to_check_org_code["ORG_NAME"] = data_json["ORG_NAME"]
    print(data_json["ORG_NAME"])

    data_to_send = {"status": "400", "msg": "No User", "data": "null"}
    try:
        cursor2.execute(
            "select ORG_CODE  from OLE_DB.SYS_ORG where  "
            "ORG_NAME=:ORG_NAME", data_to_check_org_code
        )

    except cx_Oracle.DatabaseError as e:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))

    result_org_code = cursor2.fetchall()

    ##数据的查询条件设置
    data_to_check_final["ORG_CODE"] = result_org_code[0][0]
    data_to_check_final["START_TIME"] = data_json["START_TIME"]
    data_to_check_final["END_TIME"] = data_json["END_TIME"]
    print(data_to_check_final["ORG_CODE"])

    try:
        cursor2.execute(
            "select *  from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE  between TO_DATE(:START_TIME, 'YYYY-MM-DD') and TO_DATE(:END_TIME, 'YYYY-MM-DD') "
            "AND ORG_CODE = :ORG_CODE"
            # " AND PROJECT_ID = :PROJECT_ID"                  
            " AND IS_STANDARD = :IS_STANDARD "
            # " AND LINE_CODE = :LINE_CODE"
            , data_to_check_final
            )

    except cx_Oracle.DatabaseError as e:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))

    result = cursor2.fetchall()
    print(cursor2.rowcount)

    ##need to know whether the data exist,if no return No Data
    if cursor2.rowcount == 0:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))

    start_time = datetime.datetime.now()

    CIRCLE_LOSS_SUM = 0
    LINE_END_LOSS_SUM = 0
    FIRT_PRODUCT_LOSS_SUM = 0
    CHANGE_PN_LOSS_SUM = 0
    CHANGE_WO_LOSS_SUM = 0
    FAULT_LOSS_SUM = 0
    SUM_CT_SUM = 0

    print(result)

    for i in range(cursor2.rowcount):
        CIRCLE_LOSS_SUM += result[i][15]  # 节怕损失
        LINE_END_LOSS_SUM += result[i][16]  # 收线损失
        FIRT_PRODUCT_LOSS_SUM += result[i][17]  # 首件损失
        CHANGE_PN_LOSS_SUM += result[i][18]  # 切线损失
        CHANGE_WO_LOSS_SUM += result[i][19]  # 换工单损失
        FAULT_LOSS_SUM += result[i][20]  # 故障损失
        SUM_CT_SUM += result[i][28]  # 总时间
    # print(CIRCLE_LOSS_SUM,LINE_END_LOSS_SUM,FIRT_PRODUCT_LOSS_SUM,CHANGE_PN_LOSS_SUM,CHANGE_WO_LOSS_SUM,FAULT_LOSS_SUM,SUM_CT_SUM)

    ####  计算效率

    CIRCLE_LOSS_EFFICIENCY = round((CIRCLE_LOSS_SUM / SUM_CT_SUM) * 100, 2)
    LINE_END_LOSS_EFFICIENCY = round((LINE_END_LOSS_SUM / SUM_CT_SUM) * 100, 2)
    FIRT_PRODUCT_LOSS_EFFICIENCY = round((FIRT_PRODUCT_LOSS_SUM / SUM_CT_SUM) * 100, 2)
    CHANGE_PN_LOSS_EFFICIENCY = round((CHANGE_PN_LOSS_SUM / SUM_CT_SUM) * 100, 2)
    CHANGE_WO_LOSS_EFFICIENCY = round((CHANGE_WO_LOSS_SUM / SUM_CT_SUM) * 100, 2)
    FAULT_LOSS_EFFICIENCY = round((FAULT_LOSS_SUM / SUM_CT_SUM) * 100, 2)

    TOTAL_EFFICIENCY = round(100 - (CIRCLE_LOSS_EFFICIENCY +
                                    LINE_END_LOSS_EFFICIENCY +
                                    FIRT_PRODUCT_LOSS_EFFICIENCY +
                                    CHANGE_PN_LOSS_EFFICIENCY +
                                    CHANGE_WO_LOSS_EFFICIENCY +
                                    FAULT_LOSS_EFFICIENCY), 2)

    print(CIRCLE_LOSS_EFFICIENCY,
          LINE_END_LOSS_EFFICIENCY,
          FIRT_PRODUCT_LOSS_EFFICIENCY,
          CHANGE_PN_LOSS_EFFICIENCY,
          CHANGE_WO_LOSS_EFFICIENCY,
          FAULT_LOSS_EFFICIENCY,
          TOTAL_EFFICIENCY)

    data_effiency = {"CIRCLE_LOSS_EFFICIENCY": CIRCLE_LOSS_EFFICIENCY,
                     "LINE_END_LOSS_EFFICIENCY": LINE_END_LOSS_EFFICIENCY,
                     "FIRT_PRODUCT_LOSS_EFFICIENCY": FIRT_PRODUCT_LOSS_EFFICIENCY,
                     "CHANGE_PN_LOSS_EFFICIENCY": CHANGE_PN_LOSS_EFFICIENCY,
                     "CHANGE_WO_LOSS_EFFICIENCY": CHANGE_WO_LOSS_EFFICIENCY,
                     "FAULT_LOSS_EFFICIENCY": FAULT_LOSS_EFFICIENCY,
                     "TOTAL_EFFICIENCY": TOTAL_EFFICIENCY}

    end_time = datetime.datetime.now()
    print(end_time - start_time)
    # print(result)
    res = {"status": "400", "msg": "No Data", "data": "null"}
    data_to_send["status"] = "200"
    data_to_send["msg"] = "Data is ready"
    data_to_send["data"] = data_effiency

    return json.dumps(data_to_send)

def get_project_list(request):

    #data_json=json.loads(request.body)
    data=request
    print(data)
    try:
        cursor2.execute(
            'select ORG_CODE from OLE_DB.BASE_PROJECT  where SERIES=:SERIES'
            ' AND AREA_NAME = :AREA_NAME  ',data
            )
    except cx_Oracle.DatabaseError as e:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return json.dumps(res)

    #print(cursor2.fetchall())
    result=cursor2.fetchall()
    print(result)
    num_range=cursor2.rowcount

    if cursor2.rowcount == 0:
        #res = {"status": "400", "msg": "No Data", "data": "null"}
        return 0  # 当相应项目没有对应的园区的时候 返回0

    print(num_range)
    orglist=['']
    for i in range(num_range):
        orglist.append(result[i][0])
    orglist.remove('')
    print(orglist)
    orglist_not_repeat=list(set(orglist))  ## 去重
    orglist_not_repeat.sort()
    print(orglist_not_repeat)
    orgname_num=len(orglist_not_repeat)
    print(orgname_num)

    org_name_check={"ORG_CODE": " "}
    #global org_name
    org_name=['']
    for i in range(orgname_num):
        org_name_check["ORG_CODE"]=orglist_not_repeat[i]
        print(org_name_check["ORG_CODE"])
        try:
            cursor2.execute(
                'select ORG_NAME from OLE_DB.SYS_ORG  where ORG_CODE=:ORG_CODE'
                , org_name_check
            )
        except cx_Oracle.DatabaseError as e:
            res = {"status": "400", "msg": "No Data", "data": "null"}
            return json.dumps(res)
        result=cursor2.fetchall()
        org_name.append(str(result[0][0]))
    org_name.remove('')
    #print(org_name)

    data_to_send = {"status": "400", "msg": "No User", "data": "null"}
    data_to_send["status"]="200"
    data_to_send["msg"]="ORG names"
    data_to_send["data"]=org_name
    return org_name #json.dumps(data_to_send,ensure_ascii=False)

def logindb(request):

    #data_json =json.loads(request.body)
    #print(data_json)
    data_json=request
    data_to_check_org_code={"ORG_NAME":"ORG_NAME"}
    data_to_check_org_code["ORG_NAME"]=data_json["ORG_NAME"]
    print(data_json["ORG_NAME"])

    data_to_send={"status": "400", "msg": "No User", "data": "null" }
    try:
        cursor2.execute(
            "select ORG_CODE  from OLE_DB.SYS_ORG where  "
            "ORG_NAME=:ORG_NAME", data_to_check_org_code
            )

    except cx_Oracle.DatabaseError as e:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))

    result_org_code=cursor2.fetchall()

    ##数据的查询条件设置
    data_to_check_final["ORG_CODE"]=result_org_code[0][0]
    data_to_check_final["START_TIME"]=data_json["START_TIME"]
    data_to_check_final["END_TIME"]=data_json["END_TIME"]
    print(data_to_check_final["ORG_CODE"])

    try:
        cursor2.execute("select *  from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE  between TO_DATE(:START_TIME, 'YYYY-MM-DD') and TO_DATE(:END_TIME, 'YYYY-MM-DD') "
                     "AND ORG_CODE = :ORG_CODE"
                     #" AND PROJECT_ID = :PROJECT_ID"                  
                     " AND IS_STANDARD = :IS_STANDARD "
                     #" AND LINE_CODE = :LINE_CODE"
                        , data_to_check_final
                     )

    except cx_Oracle.DatabaseError as e:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))

    result = cursor2.fetchall()
    print(cursor2.rowcount)


    ##need to know whether the data exist,if no return No Data
    if cursor2.rowcount==0:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))

    start_time =datetime.datetime.now()

    CIRCLE_LOSS_SUM = 0
    LINE_END_LOSS_SUM =0
    FIRT_PRODUCT_LOSS_SUM =0
    CHANGE_PN_LOSS_SUM =0
    CHANGE_WO_LOSS_SUM =0
    FAULT_LOSS_SUM =0
    SUM_CT_SUM=0

    #print(result[0][28])
    for i in range(cursor2.rowcount):
        CIRCLE_LOSS_SUM       +=result[i][15]  #节怕损失
        LINE_END_LOSS_SUM     +=result[i][16]  #收线损失
        FIRT_PRODUCT_LOSS_SUM +=result[i][17]  #首件损失
        CHANGE_PN_LOSS_SUM    +=result[i][18]  #切线损失
        CHANGE_WO_LOSS_SUM    +=result[i][19]  #换工单损失
        FAULT_LOSS_SUM        +=result[i][20]  #故障损失
        SUM_CT_SUM            +=result[i][28]  #总时间
    #print(CIRCLE_LOSS_SUM,LINE_END_LOSS_SUM,FIRT_PRODUCT_LOSS_SUM,CHANGE_PN_LOSS_SUM,CHANGE_WO_LOSS_SUM,FAULT_LOSS_SUM,SUM_CT_SUM)

    ####  计算效率

    CIRCLE_LOSS_EFFICIENCY = round((CIRCLE_LOSS_SUM/SUM_CT_SUM)*100,2)
    LINE_END_LOSS_EFFICIENCY = round((LINE_END_LOSS_SUM/SUM_CT_SUM)*100,2)
    FIRT_PRODUCT_LOSS_EFFICIENCY = round((FIRT_PRODUCT_LOSS_SUM/SUM_CT_SUM)*100,2)
    CHANGE_PN_LOSS_EFFICIENCY = round((CHANGE_PN_LOSS_SUM/SUM_CT_SUM)*100,2)
    CHANGE_WO_LOSS_EFFICIENCY = round((CHANGE_WO_LOSS_SUM/SUM_CT_SUM)*100,2)
    FAULT_LOSS_EFFICIENCY =round((FAULT_LOSS_SUM/SUM_CT_SUM)*100,2)
    
    TOTAL_EFFICIENCY=round(100-(CIRCLE_LOSS_EFFICIENCY + 
                          LINE_END_LOSS_EFFICIENCY+
                          FIRT_PRODUCT_LOSS_EFFICIENCY+
                          CHANGE_PN_LOSS_EFFICIENCY+
                          CHANGE_WO_LOSS_EFFICIENCY+
                          FAULT_LOSS_EFFICIENCY),2)
    
    print(CIRCLE_LOSS_EFFICIENCY,
          LINE_END_LOSS_EFFICIENCY,
          FIRT_PRODUCT_LOSS_EFFICIENCY,
          CHANGE_PN_LOSS_EFFICIENCY,
          CHANGE_WO_LOSS_EFFICIENCY,
          FAULT_LOSS_EFFICIENCY,
          TOTAL_EFFICIENCY)
    
    data_effiency={"CIRCLE_LOSS_EFFICIENCY":CIRCLE_LOSS_EFFICIENCY,
                   "LINE_END_LOSS_EFFICIENCY":LINE_END_LOSS_EFFICIENCY,
                   "FIRT_PRODUCT_LOSS_EFFICIENCY":FIRT_PRODUCT_LOSS_EFFICIENCY,
                   "CHANGE_PN_LOSS_EFFICIENCY":CHANGE_PN_LOSS_EFFICIENCY,
                   "CHANGE_WO_LOSS_EFFICIENCY":CHANGE_WO_LOSS_EFFICIENCY,
                   "FAULT_LOSS_EFFICIENCY":FAULT_LOSS_EFFICIENCY,
                   "TOTAL_EFFICIENCY":TOTAL_EFFICIENCY}
    
    #"AND PN_CODE ='TRACKERX' "  PRODUCT_OUT_QTY  (condition_project["PROJECT_ID"], condition_project["SHIFT_TYPE"], condition_project["IS_STANDARD"]
    #cursor2.execute("select * from OLE_DB.RPT_LINE_DAILY_L where  date_format(WORK_DATE ,'%Y-%m-%d') ='2018-07-06'")    " AND SHIFT_TYPE = :SHIFT_TYPE "
    #result = cursor2.fetchall()
    #result = cursor2.fetchmany(10)
    #
    # print(result.rowcount)
    #
    end_time = datetime.datetime.now()
    print(end_time-start_time)
    #print(result)
    res = {"status": "400", "msg": "No Data", "data": "null"}
    data_to_send["status"]="200"
    data_to_send["msg"] ="Data is ready"
    data_to_send["data"]=data_effiency

    #
    #cursor2.close()
    #
    #conn2.close()

   # return HttpResponse(json.dumps(data_to_send))
    return TOTAL_EFFICIENCY
    #return HttpResponse(json.dumps(data_test))

def login(req):
    Method = req.method
    if Method == 'POST':
        data=json.loads(req.body)
        print(data)

        username = req.POST.get('username')
        username = data['username']

        print(username)

        password = req.POST.get('password')
        password = data['password']
        print(password)
        if username and password :
             username = username.strip()
             try:
                 user = User.objects.get(username=username)  # 判断用户名是否存在
             except:
                 res={"status": "400", "msg": "No User", "data": "null" }
                 #return HttpResponse(json.dumps(res), content_type="application/json")
                 return HttpResponse(json.dumps(res))
                 #return HttpResponse('用户名不存在')

             #if user.username == username:
             if user.password == password:
                 res = {"status": "200", "msg": "Success", "data": "null"}
                 return HttpResponse(json.dumps(res))
                 #return HttpResponse('登录成功')
             else:
                 res = {"status": "400", "msg": "Wrong Password", "data": "null"}
                 return HttpResponse(json.dumps(res))

   # return HttpResponse(' HELLO')

