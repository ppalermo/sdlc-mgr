#!/usr/bin/python2.7
import MySQLdb
from datetime import datetime
import logging
import json
import commands

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
  #and return a list of tickets still opened.
  logging.basicConfig(filename=logpath,level=logging.DEBUG)
  logging.info('Attempting DB Connection now: ' + timeStamp())
  try:
    db = MySQLdb.connect(host="10.7.240.202", port=3306, user="sdlf-mgr", passwd="9.01jdksoq*", db="infosecsdlc")
    cur = db.cursor()
  except Exception, e: print repr(e)
  logging.info('DB Connection Successful: ' + timeStamp())

  results = []
  sSql = "SELECT flawid FROM flawstrack WHERE status='Open' and trackername = 'Pivotal Tracker'"
  cur.execute(sSql)
  logging.info('SQL Query complete: ' + timeStamp())
  for row in cur: #Check len(cur) ??????????????????????
    results.append(FetchOneAssoc(cur))
  logging.info('All query results stored in a list')

  tickets_list = []
  for result in results:
    tickets_list.append(results['flawid'])
  if len(tickets_list) == 0:
    #empty list - no opened tickets to query..
    logging.info('No open tickets on DB to query for status.')
  else:
    logging.info('Returning tickets list..')
    tickets_list


def checkStatus(tickets_list):
  curl_string = ''
  for ticket in tickets_list:
    curl_string = '' + ticket
    commands.getstatusoutput(curl_string)

""" PENDING... """
#...run some curl to check on Pivotal Tracker...
#...Parse json results.
#...Update DB with current status. and updated date.





