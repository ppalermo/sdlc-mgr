#!/usr/bin/python2.7
"""YOU NEED TO PASS THE LOGGING PATH TO THIS FUNCTION OTHERWISE IT WILL NOT WORK!"""
"""YOU NEED TO PASS THE LOGGING PATH TO THIS FUNCTION OTHERWISE IT WILL NOT WORK!"""
"""YOU NEED TO PASS THE LOGGING PATH TO THIS FUNCTION OTHERWISE IT WILL NOT WORK!"""
import xml.etree.cElementTree as ET
import commands
import os
import getpass
import MySQLdb
from datetime import datetime

def FetchOneAssoc(cursor) :
  data = cursor.fetchone()
  if data == None :
    return None
  desc = cursor.description
  dict = {}
  for (name, value) in zip(desc, data) :
    dict[name[0]] = value
  return dict

class Flaw(object):
  def __init__(self,flawid):
    self.flawid              = flawid
    self.cweid               = 0
    self.pcirelated          = False
    self.datefo              = ''
    self.remediation         = ''
    self.mitigation          = ''
    self.severity            = ''
    self.catname             = ''
    self.module              = ''
    self.sourcepath          = ''
    self.sourcefile          = ''
    self.linenum             = ''                 #Get this value too!
    self.affects_pol_comp    = False
    self.gp_expires          = '' #Date
    self.app_name            = ''
    self.istracked           = False
    self.created             = ''


def returnSev4(xmlpath, appname):
  """This function is going to take a path where the
  xml detailed report resides and it will parse the results,
  and then store the values required to fill up the DB
  within a flaw class"""
  #f = open(confpath, 'rU')
  #conf = [] #list to save DB config.
  #for line in f:
  #  conf.append(line.rstrip('\n'))
  #datetime.now().strftime("%H:%M:%S") ==> Hour  Minutes  Seconds '11:22:32'
  now = datetime.now()
  #now.strftime("%m-%d-%Y") Date format ==> Month Day Year.
  #Date time in a string, format: '11-18-2014 11:27:02':
  DATETIME = now.strftime("%Y-%m-%d") + ' ' + datetime.now().strftime("%H:%M:%S")
  pos = 0
  sev4_list = []
  document = ET.parse(xmlpath)
  root = document.getroot()
  sev4flaws = root.findall("./{https://www.veracode.com/schema/reports/export/1.0}severity/[@level='4']/*/{https://www.veracode.com/schema/reports/export/1.0}cwe/*/{https://www.veracode.com/schema/reports/export/1.0}flaw")
  #COnnect to the DB:
  try:
    db = MySQLdb.connect(host="10.7.240.202", port=3306, user="sdlf-mgr", passwd="", db="infosecsdlc")
    cur = db.cursor()
  except Exception, e: print repr(e)

  comstr = "commit"

  pol_comp = ['1','0'] #This is used for the list comprehension down below within the for loop. (sev4_list[pos].affects_pol_comp)

  for sev4 in sev4flaws:
    sev4_list.append (Flaw(sev4.attrib['issueid']))
    sev4_list[pos].cweid              = sev4.attrib['cweid']
    sev4_list[pos].pcirelated         = sev4.attrib['pcirelated']
    sev4_list[pos].datefo             = sev4.attrib['date_first_occurrence']
    sev4_list[pos].remediation        = sev4.attrib['remediation_status']
    sev4_list[pos].mitigation         = sev4.attrib['mitigation_status']
    sev4_list[pos].severity           = sev4.attrib['severity']
    sev4_list[pos].catname            = sev4.attrib['categoryname'].replace("'","")
    sev4_list[pos].module             = sev4.attrib['module']
    sev4_list[pos].sourcepath         = sev4.attrib['sourcefilepath']
    sev4_list[pos].sourcefile         = sev4.attrib['sourcefile']
    sev4_list[pos].linenum            = sev4.attrib['line']
    sev4_list[pos].affects_pol_comp   = [ pol_comp[0] if  sev4.attrib['affects_policy_compliance'] in 'true' else pol_comp[1] ][0]
    sev4_list[pos].gp_expires         = sev4.attrib['grace_period_expires']
    sev4_list[pos].app_name           = appname
    sev4_list[pos].istracked          = False
    sev4_list[pos].created            = DATETIME
    sSql="insert into flaws (issueid,cweid,pcirelated,date_first_occurrence,remediation,mitigation,severity,categoryname,module,sourcepath,sourcefile,linenumber,affects_pol_comp,gp_expires,app_name,istracked,created) \
    VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s')"  %(sev4_list[pos].flawid, sev4_list[pos].cweid, sev4_list[pos].pcirelated, sev4_list[pos].datefo, sev4_list[pos].remediation, sev4_list[pos].mitigation, sev4_list[pos].severity, sev4_list[pos].catname, sev4_list[pos].module, sev4_list[pos].sourcepath, sev4_list[pos].sourcefile, sev4_list[pos].linenum, sev4_list[pos].affects_pol_comp, sev4_list[pos].gp_expires, sev4_list[pos].app_name, sev4_list[pos].istracked, sev4_list[pos].created)
    #print sSql, '\n\n'
    pos += 1
    try:
      cur.execute(sSql)
    except Exception, e: print repr(e)
    cur.execute(comstr)
  #for flaw in sev4_list:
  #  print flaw.app_name

def main():
  application_name = raw_input("Please enter Application Name: \n")
  path = raw_input("Please enter PATH: \n")
  returnSev4(path,application_name)

if __name__ == '__main__':
  main()
