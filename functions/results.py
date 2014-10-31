import xml.etree.ElementTree as ET
import commands
import os
import getpass

def listApps():
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  cmd = "curl -s --compressed -u " + appusr + ":" + apppass +" https://analysiscenter.veracode.com/api/4.0/getapplist.do"
  #print cmd
  s,o = commands.getstatusoutput(cmd)
  #print o
  document = ET.ElementTree(ET.fromstring(o))
  root = document.getroot()
  print "Available applications are the following...\n"
  for child in root:
    print "Application Name: %s || Application ID: %s" % (child.attrib['app_name'], child.attrib['app_id'])
  print "\n"
  z = raw_input()


def getBuild():
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  appID = raw_input("Please enter Application ID: \n")
  cmd = "curl -s --compressed -u " + appusr + ":" + apppass + " https://analysiscenter.veracode.com/api/4.0/getbuildlist.do -F \"app_id=\"" + appID
  s,o = commands.getstatusoutput(cmd)
  document = ET.ElementTree(ET.fromstring(o))
  root = document.getroot()
  print "Your build IDs are the following:...\n"
  for child in root:
    print "Build ID: %s" % child.attrib['build_id']
  print "\n"
  z = raw_input()


def getHighFlaws():
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  buildID = raw_input("Please enter Build ID: \n")
  cmd = "curl -s --compressed -u " + appusr + ":" + apppass + " https://analysiscenter.veracode.com/api/2.0/detailedreport.do?build_id=" + buildID
  #cmd = "curl -s --compressed -u " + username + ":" + password + " https://analysiscenter.veracode.com/api/2.0/detailedreport.do?build_id=" + buildID
  s,o = commands.getstatusoutput(cmd)
  #outfile = open ('/Users/martin/Dropbox/Python/SCRIPTS/Python/scripts/2014/RSide/output.txt', 'w')
  #outfile.write(o)
  #outfile.close()
  #print "File saved to disk!"
  document = ET.ElementTree(ET.fromstring(o))
  root = document.getroot()
  modules = root.findall("./{https://www.veracode.com/schema/reports/export/1.0}static-analysis/*/")
  for module in modules:
    sev4 = int(module.attrib['numflawssev4'])
    sev5 = int(module.attrib['numflawssev5'])
    if sev4 > 0 or sev5 > 0:
      print "The module named: \"%s\" contains %i Very High Flaws and %i High Flaws" %(module.attrib['name'], sev5, sev4 )
  z = raw_input()



def getSev4Flaws():
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  buildID = raw_input("Please enter Build ID: \n")
  cmd = "curl -s --compressed -u " + appusr + ":" + apppass + " https://analysiscenter.veracode.com/api/2.0/detailedreport.do?build_id=" + buildID
  s,o = commands.getstatusoutput(cmd)
  document = ET.ElementTree(ET.fromstring(o))
  root = document.getroot()
  sev4flaws = root.findall("./{https://www.veracode.com/schema/reports/export/1.0}severity/[@level='4']/*/{https://www.veracode.com/schema/reports/export/1.0}cwe/*/{https://www.veracode.com/schema/reports/export/1.0}flaw")
  for sev4 in sev4flaws:
    print "\n\n"
    print "Issue ID: %s \n" %sev4.attrib['issueid']
    print "Category Name: %s \n" %sev4.attrib['categoryname']
    print "Module Name: %s \n" %sev4.attrib['module']
    print "SourceFile Name: %s \n" %sev4.attrib['sourcefile']
    print "Line Number: %s \n" %sev4.attrib['line']
  z = raw_input()


def getSev5Flaws():
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  buildID = raw_input("Please enter Build ID: \n")
  cmd = "curl -s --compressed -u " + appusr + ":" + apppass + " https://analysiscenter.veracode.com/api/2.0/detailedreport.do?build_id=" + buildID
  s,o = commands.getstatusoutput(cmd)
  document = ET.ElementTree(ET.fromstring(o))
  root = document.getroot()
  sev5flaws = root.findall("./{https://www.veracode.com/schema/reports/export/1.0}severity/[@level='5']/*/{https://www.veracode.com/schema/reports/export/1.0}cwe/*/{https://www.veracode.com/schema/reports/export/1.0}flaw")
  for sev5 in sev5flaws:
    print "\n\n"
    print "Issue ID: %s \n" %sev5.attrib['issueid']
    print "Category Name: %s \n" %sev5.attrib['categoryname']
    print "Module Name: %s \n" %sev5.attrib['module']
    print "SourceFile Name: %s \n" %sev5.attrib['sourcefile']
    print "Line Number: %s \n" %sev5.attrib['line']
  z = raw_input()


