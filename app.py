from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import sys
import re
import os
import time
import datetime
from config import Configuration
from db import DBConnection,Query
import uuid
from xml.etree import ElementTree as et
import requests

ERROR_FILE = '/home/ubuntu/searchstation/error.log'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def db_access():
    configuration = Configuration.get_configuration('local')
    _host = configuration['host']
    _user = configuration['user']
    _password = configuration['password']
    _database = configuration['database']
    _port = configuration['port']
    _charset = configuration['charset']

    conn = DBConnection(host=_host,
            user=_user,
            password=_password,
            database=_database,
            port=_port,
            charset=_charset)
    return conn

@app.route('/')
def main():
    return render_template('index.html')  

@app.route('/requested')
def requested():

    sess = uuid.uuid1() # or uuid.uuid4()

    api = request.args.get('api', default = '', type = str)

    session = {}

    session['sess'] = str(sess)
    session['api'] = str(api)
    
    if api == 'electric':
        return render_template('/request_electric.html',session=session)       

@app.route('/lists_electric', methods=['GET', 'POST'])
def lists_electric():

    sess = request.args.get('sess', default = '', type = str)
    api = request.args.get('api', default = '', type = str)
    address = request.args.get('address', default = '', type = str)

    if request.method == 'POST':
        requested = request.form
        for key,value in requested.items():
            sess = requested['sess']
            api = requested['api']
            address = requested['address']

        _list = 'http://openapi.kepco.co.kr/service/EvInfoServiceV2/getEvSearchList?serviceKey=SERICEKEY'         

        _addr = [] #충전소주소
        _chargeTp = [] #충전기타입
        _cpId = [] #충전기ID
        _cpNm = [] #충전기명칭
        _cpStat = [] #충전기상태
        _cpTp = [] #충전방식
        _csId = [] #충전소ID
        _csNm = [] #충전소명칭
        _lat = [] #위도
        _longi = [] #경도
        _statUpdateDatetime = [] #충전기상태 갱신 시작     

        _resultCode = ''

        _totalCount = 0
            
        addr = address
        rows = '200'

        params = {'addr': addr, 'numOfRows':rows}

        response = requests.get(_list, params=params)

        directory = '/home/ubuntu/searchstation/xml/'

        filename = '{}_list_{}.xml'.format(directory,sess)

        #list
        with open(filename,'w') as file:
            file.write(response.text)

        tree = et.parse(filename)
        root = tree.getroot()

        for response in root:
            for header in response:
                if header.tag == 'resultCode':
                    _resultCode = header.text

        for response in root:
            for body in response:
                if body.tag == 'totalCount':
                    _totalCount = body.text

        for response in root:
            for body in response:
                for items in body:
                    for item in items:
                        if item.tag == 'addr':
                            _addr.append(item.text)
                        elif item.tag == 'chargeTp':
                            _chargeTp.append(item.text)
                        elif item.tag == 'cpId':
                            _cpId.append(item.text)
                        elif item.tag == 'cpNm':
                            _cpNm.append(item.text)
                        elif item.tag == 'cpStat':
                            _cpStat.append(item.text)
                        elif item.tag == 'cpTp':
                            _cpTp.append(item.text)
                        elif item.tag == 'csId':
                            _csId.append(item.text)      
                        elif item.tag == 'csNm':
                            _csNm.append(item.text)
                        elif item.tag == 'lat':
                            _lat.append(item.text)
                        elif item.tag == 'longi':
                            _longi.append(item.text)
                        elif item.tag == 'statUpdateDatetime':
                            _statUpdateDatetime.append(item.text)
                                                       
        print(sess,_resultCode,_totalCount)

        result = _resultCode
        trace  = request.user_agent.string

        if int(_totalCount) > int(rows):
            _totalCount = rows
                       
        conn = db_access() 
        conn.exec_set_request_electric(sess,addr,result,trace)

        for i in range(0,int(_totalCount)):
            conn.exec_set_results_electric(sess,_addr[i],_chargeTp[i],_cpId[i],_cpNm[i],_cpStat[i],_cpTp[i],_csId[i],_csNm[i],_lat[i],_longi[i],_statUpdateDatetime[i])
        data = conn.exec_get_lists_electric(sess)

        session = {}

        session['sess'] = str(sess)
        session['api'] = str(api)
        session['address'] = str(address) 

        print('data:',data)
        
    elif request.method == 'GET':
        conn = db_access() 
        data = conn.exec_get_lists_electric(sess)

        session = {}

        session['sess'] = str(sess)
        session['api'] = str(api)

    if not data:
        print('none data',data)
        if api == 'electric':
            session = {}
            session['sess'] = str(sess)
            session['api'] = 'electric'
            return render_template('/request_electric.html',session=session)                    
    else:
        if api == 'electric':          
            return render_template('/lists_electric.html', data=data,session=session)    

@app.route('/detail_electric')
def detail_electric():

    sess = request.args.get('sess', default = '', type = str)
    api = request.args.get('api', default = '', type = str)
    csid = request.args.get('csid', default = '', type = str)   
        
    conn = db_access()
    data = conn.exec_get_results_electric(sess,csid)

    session = {}

    session['sess'] = str(sess)
    session['api'] = str(api)
    session['csid'] = str(csid)  

    template = render_template('/detail_electric.html',data=data,session=session)

    return template  

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
