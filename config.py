'''
CREATE TABLE request_electric (
  num int(11) NOT NULL AUTO_INCREMENT,
  sess varchar (100) NOT NULL,
  addr varchar(255) DEFAULT '-',
  result varchar(100) DEFAULT '-',
  trace varchar(255) DEFAULT '-',
  rdate datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

CREATE TABLE detail_electric (
  num int(11) NOT NULL AUTO_INCREMENT,
  sess varchar (100) NOT NULL,
  addr varchar(255) DEFAULT '-',
  chargeTp char(1) DEFAULT '0',
  cpId varchar(12) DEFAULT '0',
  cpNm varchar(20) DEFAULT '-',
  cpStat varchar(2) DEFAULT '-',
  cpTp varchar(2) DEFAULT '0',
  csId varchar(12) DEFAULT '-',
  csNm varchar(20) DEFAULT '-',   
  lat varchar(50) DEFAULT '-', 
  longi varchar(20) DEFAULT '-',  
  statUpdateDatetime varchar(20) DEFAULT '-',   
  rdate datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
END'''

class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='HOSTNAME',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')
      
    elif(choose == 'ubuntu'):
      connect_value = dict(host='HOSTNAME',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value
  