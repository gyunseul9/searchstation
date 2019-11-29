import pymysql

class DBConnection:
    def __init__(self,host,user,password,database,charset,port):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            charset=charset,
            port=port,
            cursorclass=pymysql.cursors.DictCursor)

    def exec_get_lists_electric(self,sess):
        with self.connection.cursor() as cursor:
            query = Query().get_lists_electric(sess)
            cursor.execute(query)
            data = cursor.fetchall()
            return data               

    def exec_get_results_electric(self,sess,csId):
        with self.connection.cursor() as cursor:
            query = Query().get_results_electric(sess,csId)
            cursor.execute(query)
            data = cursor.fetchall()
            return data 

    def exec_set_request_electric(self,sess,addr,result,trace): 
        query = Query().set_request_electric(sess,addr,result,trace) 
        with self.connection as cur:
            cur.execute(query)                  

    def exec_set_results_electric(self,sess,addr,chargeTp,cpId,cpNm,cpStat,cpTp,csId,csNm,lat,longi,statUpdateDatetime): 
        query = Query().set_results_electric(sess,addr,chargeTp,cpId,cpNm,cpStat,cpTp,csId,csNm,lat,longi,statUpdateDatetime) 
        with self.connection as cur:
            cur.execute(query)          


    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

class Query:

    def get_lists_electric(self,sess):
        query = 'select * from detail_electric where sess= \'{}\''.format(sess)
        print('query:',query)
        return query          

    def get_results_electric(self,sess,csId):
        query = 'select * from detail_electric where sess=\'{}\' and csId=\'{}\''.format(sess,csId)       
        print(query)
        return query 

    def set_request_electric(self,sess,addr,result,trace):
        query = 'insert into request_electric (sess,addr,result,trace) \
        values (\'{}\',\'{}\',\'{}\',\'{}\')'.format(sess,addr,result,trace)
        #print('qery:',query)
        return query  

    def set_results_electric(self,sess,addr,chargeTp,cpId,cpNm,cpStat,cpTp,csId,csNm,lat,longi,statUpdateDatetime):
        query = 'insert into detail_electric (sess,addr,chargeTp,cpId,cpNm,cpStat,cpTp,csId,csNm,lat,longi,statUpdateDatetime) \
        values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(sess,addr,chargeTp,cpId,cpNm,cpStat,cpTp,csId,csNm,lat,longi,statUpdateDatetime)
        #print('qery:',query)
        return query     

