#!/usr/bin/python2.7
import MySQLdb
from datetime import datetime
import logging
import json
import commands
import keyring


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


def grabTickets():
  #This is gonna query DB for open tickets
  #and return a list of tickets still opened. (Tracked in corresponding defect tracker, but still open)
  logging.basicConfig(filename=logpath,level=logging.DEBUG)
  logging.info('Attempting DB Connection now: ' + timeStamp())
  try:
    db = MySQLdb.connect(host="10.7.240.202", port=3306, user="sdlf-mgr", passwd=(keyring.get_password('sdlcdb','sdlf-mgr')), db="infosecsdlc")
    cur = db.cursor()
  except Exception, e: print repr(e)
  logging.info('DB Connection Successful: ' + timeStamp())
  results = []
  sSql = "SELECT  trackingnumber, updatedat FROM flawstrack WHERE status='Open' and trackername = 'Pivotal Tracker'"
  cur.execute(sSql)
  logging.info('SQL Query complete: ' + timeStamp())
  for row in cur: #Check len(cur) ??????????????????????
    results.append(FetchOneAssoc(cur))
  logging.info('All query results stored in a list')
  tickets_dict = {}
  for result in results:
        #I am gonna use a dictionary below to return:
        #key = flawid from flawstrack table
        #value = updatedat from flawstrack table
    trknum = result['trackingnumber']
    lastupdate = result['updatedat']
    if trknum not in tickets_dict:
      tickets_dict[trknum] = lastupdate
  if len(tickets_dict) == 0:
    #empty dic - no opened tickets to query..
    logging.info('No open tickets on DB to query for status.')
    cur.close()
    return tickets_dict
  else:
    logging.info('Returning tickets list..')
    cur.close()
  return tickets_dict

def checkStatus(tickets_dict):
  try:
    db = MySQLdb.connect(host="10.7.240.202", port=3306, user="sdlf-mgr", passwd=(keyring.get_password('sdlcdb','sdlf-mgr')), db="infosecsdlc")
    cur = db.cursor()
  except Exception, e: print repr(e)
  curl_string = ''
  for ticket in tickets_dict:
    #gotta do this first: #keyring.set_password('PivotalTracker','apitoken','TOKEN')
    TOKEN = keyring.get_password('PivotalTracker','apitoken')
    PROJECT_ID='169315'
    curl_str ='curl -s -X GET -H \"X-TrackerToken: ' + TOKEN + '" ' + 'https://www.pivotaltracker.com/services/v5/projects/' + PROJECT_ID + '/stories/' + ticket
    #curl -X GET -H "X-TrackerToken: $TOKEN" "https://www.pivotaltracker.com/services/v5/projects/$PROJECT_ID/stories/555"
    s,o = commands.getstatusoutput(curl_str)
    if s != 0:
      logging.info('Error reaching Pivotal Trackers API \n')
    else:
      logging.info('Response from Pivotal Tracker API receieved.')
      decoded_json = json.loads(o)
      date_from_pt = datetime.strptime(decoded_json['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
      if date_from_pt != tickets_dict[ticket]: #if the date on Pivotal Tracker's last_update different than date on the DB. The ticket was updated:
        decoded_id = str(decoded_json['id']
        d_state = str(decoded_json['current_state'])

        logging.info('Changes found on ticket PT.Bug# %s') %decoded_id

        #Since the ticket was updated I need to reflect changes on the DB:

        sSql_u1 = "update flawstrack set updatedat='%s' where trackingnumber='%s'" %(date_from_pt, decoded_id)
        cur.execute(sSql_u1)
        sSql_u2 = "update flawstrack set status='%s' where trackingnumber='%s'" %(decoded_id, d_state)
        cur.execute(sSql_u)
      else:
        logging.info('No updates found for PT.Bug# %s') %decoded_id

#PT.Bug Sample: 83770908
#...run some curl to check on Pivotal Tracker...DONE
#...Parse json results...DONE.
#...Update DB with current status. and updated date. DONE.

def main():
  tickets_to_check = []
  tickets_to_check = grabTickets(logpath)

if __name__ == '__main__':
  main()

