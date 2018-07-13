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
'''
  ORG_CODE:
  
    63878A393AA041CBB34F30DEDFE2619B  ## 科技园  SMT制造一部
  
  PROJECT_ID:
  
    ALMOND 

'''
address = '10.10.31.115:1521/orcl'
username = 'BJYJY'
password = 'abc@123'

class my_database_login(database_login):
    def __init__(self,address,username,password):
        database_login.__init__(self, address, username, password)
    def login(self):
        database_login.login(self)

database_temp=my_database_login(address,username,password)

conn2 = cx_Oracle.connect('BJYJY', 'abc@123', '10.10.31.115:1521/orcl')
cursor2 = conn2.cursor()

class dbreadrest(APIView):
   # authentication_classes = [TestAuthentication, ]
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
   # authentication_classes = [TestAuthentication, ]
    #permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        return HttpResponse(logindb(request))


    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')
def logindb(request):

    data =json.loads(request.body)
    print(data)
    #condition=data["condition"]
    #print(condition)
    data_test= {"data1": " ",
                "data2": {"data": []
                         }
                }
    data_to_send={"status": "400", "msg": "No User", "data": "null" }
    #print(data)
    start_time=datetime.datetime.now()
    #conn2 = cx_Oracle.connect('BJYJY', 'abc@123', '10.10.31.115:1521/orcl')
    #
    #cursor2 = conn2.cursor()
    end_time = datetime.datetime.now()
    print(end_time-start_time)
    #
    # cursor2.execute('select * from OLE_DB.CT_STANDARD_BEST')
    # result=cursor2.fetchone()
    # data1=result[3]
    # date_test=datetime.datetime.now()
    # print(date_test)
    # print(date_test.month)
    # print(data1)
    #cursor2.execute('select * from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE =')  WORK_DATE AND
    # cursor2.execute("select *   from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE  between TO_DATE('2018-07-04', 'YYYY-MM-DD') and TO_DATE('2018-07-06', 'YYYY-MM-DD')"
    #                 "AND  PROJECT_ID = 'ALMOND'"
    #                 "AND SHIFT_TYPE ='DAY' "
    #                 "AND IS_STANDARD = 'Y' "
    #               )
    start_time = datetime.datetime.now()
    try:
        cursor2.execute("select *  from OLE_DB.RPT_LINE_DAILY_L where WORK_DATE  between TO_DATE(:START_TIME, 'YYYY-MM-DD') and TO_DATE(:END_TIME, 'YYYY-MM-DD') "
                     "AND ORG_CODE = :ORG_CODE"
                     " AND PROJECT_ID = :PROJECT_ID"                  
                     " AND IS_STANDARD = :IS_STANDARD "
                     " AND LINE_CODE = :LINE_CODE" , data
                     )

    except cx_Oracle.DatabaseError as e:
        res = {"status": "400", "msg": "No Data", "data": "null"}
        return HttpResponse(json.dumps(res))
    #print(cursor2.fetchall())
    result = cursor2.fetchall()
    print(cursor2.rowcount)
    #print(result)
    end_time = datetime.datetime.now()
    print(end_time-start_time)

    start_time =datetime.datetime.now()
    #print(result1[0][15],result1[1][15])
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
    TOTAL_EFFICIENCY=100-(CIRCLE_LOSS_EFFICIENCY + LINE_END_LOSS_EFFICIENCY+FIRT_PRODUCT_LOSS_EFFICIENCY+CHANGE_PN_LOSS_EFFICIENCY+CHANGE_WO_LOSS_EFFICIENCY+FAULT_LOSS_EFFICIENCY)
    print(CIRCLE_LOSS_EFFICIENCY,LINE_END_LOSS_EFFICIENCY,FIRT_PRODUCT_LOSS_EFFICIENCY,CHANGE_PN_LOSS_EFFICIENCY,CHANGE_WO_LOSS_EFFICIENCY,FAULT_LOSS_EFFICIENCY,TOTAL_EFFICIENCY)
    data_effiency={"CIRCLE_LOSS_EFFICIENCY":CIRCLE_LOSS_EFFICIENCY,"LINE_END_LOSS_EFFICIENCY":LINE_END_LOSS_EFFICIENCY,"FIRT_PRODUCT_LOSS_EFFICIENCY":FIRT_PRODUCT_LOSS_EFFICIENCY,
                   "CHANGE_PN_LOSS_EFFICIENCY":CHANGE_PN_LOSS_EFFICIENCY,"CHANGE_WO_LOSS_EFFICIENCY":CHANGE_WO_LOSS_EFFICIENCY,"FAULT_LOSS_EFFICIENCY":FAULT_LOSS_EFFICIENCY,
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
    return json.dumps(data_to_send)
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

