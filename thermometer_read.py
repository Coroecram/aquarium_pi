#!/usr/bin/python

def get_temp(id):
  try:
    mytemp = ''
    filename = 'w1_slave'
    f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      mytemp = 9999
    f.close()

    return int(mytemp[1])

  except:
    return 9999

def read_temp():
  id = '28-0000066efc16'
  return '{:.3f}'.format(get_temp(id)/float(1000))
