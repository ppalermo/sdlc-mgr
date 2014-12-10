#!/usr/bin/python2.7
#/Users/martin/Desktop/log.txt
"""YOU NEED TO PASS THE LOGGING PATH TO THIS FUNCTION OTHERWISE IT WILL NOT WORK!"""
"""Need to add Pivotal Tracker's TOKEN too"""
import MySQLdb
from datetime import datetime
import logging
import json
import commands
import keyring

#Below function can be used to either fecth one only row, or ALL rows from
#a select statement.
def FetchOneAssoc(cursor) :
  data = cursor.fetchone()
  if data == None :
    return None
  desc = cursor.description
  dict = {}
  for (name, value) in zip(desc, data):
    dict[name[0]] = value
  return dict


def timeStamp():
  now = datetime.now()
  DATETIME = now.strftime("%Y-%m-%d") + '_' + datetime.now().strftime("%H:%M:%S")
  return DATETIME


"""YOU NEED TO PASS THE LOGGING PATH TO THIS FUNCTION OTHERWISE IT WILL NOT WORK!"""
def reedFlawsFromDB(logpath):
  """YOU NEED TO PASS THE LOGGING PATH TO THIS FUNCTION OTHERWISE IT WILL NOT WORK!"""
  comstr = "commit"
  now = datetime.now()
  logging.basicConfig(filename=logpath,level=logging.DEBUG)
  #Conexion a la DB:
  logging.info('Attempting DB Connection now: ' + timeStamp())
  try:
    db = MySQLdb.connect(host="10.7.240.202", port=3306, user="sdlf-mgr", passwd=(keyring.get_password('sdlcdb','sdlf-mgr')), db="infosecsdlc")
    cur = db.cursor()
  except Exception, e: print repr(e)
  logging.info('DB Connection Successful: ' + timeStamp())
  #store query results in a list:
  results = []
  """GOTTA update these QUERY BELOW!!!!!!!!!!!!!!!!!!!!"""
  """GOTTA update these QUERY BELOW!!!!!!!!!!!!!!!!!!!!"""
  """GOTTA update these QUERY BELOW!!!!!!!!!!!!!!!!!!!!"""
  """GOTTA update these QUERY BELOW!!!!!!!!!!!!!!!!!!!!"""

  sSql = "SELECT * FROM flaws WHERE istracked='0' and issueid = '4'"
  logging.info('Running SQL Queries now: ' + timeStamp())
  cur.execute(sSql)
  logging.info('SQL Query complete: ' + timeStamp())
  for row in cur:
    results.append(FetchOneAssoc(cur))
  logging.info('All query results stored in a list')
  #at this point I have a list of dictionaries where all my queries' results are stored.

  #Below all the fixed values (always the same).
  CURL_BASE = 'curl -s -X POST -H "X-TrackerToken:54ea5485696ab1958eaf3e76ae6d8ca1" -H "Content-Type: application/json" -d'
  CURL_TAIL = '"https://www.pivotaltracker.com/services/v5/projects/169315/stories"'
  CWE_BASE_URL = 'http://cwe.mitre.org/data/definitions/'

  sevs = ['High', 'Very High']
  #Here I start creating the curl strings to push into Pivotal Tracker.
  for f in results:
    v1_NAME     = 'Veracode Issue ID: ' + str(f['issueid'])
    v4_DESC     = f['categoryname']
    v5_ID       = str(f['issueid'])
    s           = [ sevs[0] if  f['severity'] in '4' else sevs[1] ] #Pretty awesome list comprehension.
    v6_SEV      = s[0]
    v7_CATNAME  = f['categoryname']
    v8_MODULE   = f['module']
    v9_SRCPATH  = f['sourcepath']
    v10_SRCFILE = f['sourcefile']
    v11_LNUM    = f['linenumber']
    v12_CWE     = CWE_BASE_URL + str(f['cweid']) + '.html'
    v13_PCI     = f['pcirelated']
    v14_RSTS    = f['remediation']
    v15_MSTS    = f['mitigation']
    v16_POLCOMP = f['affects_pol_comp']
    v17_GPEXP   = f['gp_expires']
    v18_OPEN    = f['created']

    curl_string = CURL_BASE + ' ' + '\'{' + "\"name\":" + '"' +  v1_NAME + '\", ' \
    + "\"story_type\":\"bug\"" + ', ' + "\"label_ids\":[10000976]" + ', ' \
    + "\"description\":" + '"' \
    + v1_NAME + "\\n "\
    + "SEVERITY: " + str(v6_SEV) + "\\n " \
    + "CATEGORY NAME: " + v7_CATNAME + "\\n " \
    + "MODULE: " + v8_MODULE + "\\n " \
    + "SOURCEFILEPATH: " + v9_SRCPATH + "\\n " \
    + "SOURCEFILE: " + v10_SRCFILE + "\\n " \
    + "LINE NUMBER: " + str(v11_LNUM) + "\\n " \
    + "CWE_REFERENCE: " + str(v12_CWE) + "\\n " \
    + "PCI_RELATED: " + str(v13_PCI) + "\\n " \
    + "REMEDIATION_STATUS: " + v14_RSTS + "\\n " \
    + "MITIGATION_STATUS: " + v15_MSTS + "\\n " \
    + "AFFECTS_POL_COMPLIANCE: " + str(v16_POLCOMP) + "\\n " \
    + "GP_EXPIRES: " + str(v17_GPEXP) + "\\n " \
    + "OPEN_DATE: " + str(v18_OPEN) + "\\n\"" \
    + '}\' ' + CURL_TAIL
    print curl_string
    s,o = commands.getstatusoutput(curl_string)
    decoded_json = json.loads(o)

    if s == 0:                  #CURL SUCCESSFUL.
      logging.info("Bug created successfuly...Updating DB...")
      #HERE UPDATING THE DB.......
      logging.info(timeStamp())
      bugid = decoded_json['id']
      createdat = decoded_json['created_at']
      current_state = decoded_json['current_state']
      updated_at    = decoded_json['updated_at']
      #Now is time to update the DB:
      sSql_i = "insert into flawstrack (flawid, appname, trackername, openeddate, status, updatedat, trackingnumber) VALUES('%s','%s','%s','%s','%s','%s','%s')" %(v5_ID,'name.com', 'Pivotal Tracker', createdat, 'Open',createdat, bugid)
      cur.execute(sSql_i)
      cur.execute(comstr)
      sSql_u = "update flaws set istracked='1' where issueid='%s'" %v5_ID
      cur.execute(sSql_u)
      cur.execute(comstr)
      #"update ossec_info set last_update='%s' where hostname='%s' and last_update='%s'" % (fecha_lastupdate, host, t1)
      #sSql="insert into ossec_info (hostname,up_date,ag_status,last_update) VALUES('%s','%s','%s','%s')" %(host,dic1['up_date'],sts,fecha_lastupdate)
    else:
      logging.error("There was a problem creating the Bug...error following:")
      logging.error(o)
      cur.close()

"""
for key in decoded_json.keys():
...   print key
...
story_type
kind
description
url
created_at
labels
current_state
updated_at
requested_by_id
owner_ids
project_id
id
name
>>>
"""
def main():
  log = raw_input("Please enter a path for the log file: \n")
  reedFlawsFromDB(log)

if __name__ == '__main__':
  main()