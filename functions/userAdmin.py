import xml.etree.cElementTree as ET
import commands
import os
import getpass

def UserAdminMenu():
  #Show some Users Admin Menu here:
  print "*****************************************************"
  print "*****************************************************"
  print "*******Veracode's USERS ADMINISTRATION...************"
  print "*****************************************************"
  print "*****************************************************"

  print '\n'
  print "Select the option by pressing the option number: \n"

  print "- List ALL Active Users: \"1\" \n "
  print "- ?????????????????????: \"2\" \n "

  print "\n-QUIT: \"exit\""
  opt = raw_input()
  return opt


def listAllUsers():
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  resourceURL = "https://analysiscenter.veracode.com/api/3.0/getuserlist.do"
  cmd = "curl --compressed -u " + appusr + ":" + apppass + " " + resourceURL + " -F \"login_enabled=true\""
  #print cmd
  s,o = commands.getstatusoutput(cmd)
  print o
  print "\n \n \n"
  z = raw_input()


