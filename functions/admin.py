import commands
import getpass

def adminMenu():
  #Show some Admin Menu here:
  print "*****************************************************"
  print "*****************************************************"
  print "***********Veracode's API Mgmt ADMIN...**************"
  print "*****************************************************"
  print "*****************************************************"

  print '\n'
  print "Select the option by pressing the option number: \n"

  print "- Mark Flaw as False Positive: \"1\" \n "
  print "- Accept a Flaw list: \"2\" \n "

  print "\n-QUIT: \"exit\""
  opt = raw_input()
  return opt

def setFalsePositive():
  """curl --compressed -u [username]
  https://analysiscenter.veracode.com/api/updatemitigationinfo.do -F
  "build_id=[your build ID] -F
  "action=fp" -F "comment=[your comment text]" -F "flaw_id_list=[your flaw ID(s)]".
  """
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  buildID = raw_input("Please enter Build ID: \n")
  flawID = raw_input("Please enter flaws separated by comma: \n")
  comment = raw_input("Please enter appropriate comment: \n")

  cmd = "curl -s --compressed -u " + appusr + ":" + apppass + \
  " https://analysiscenter.veracode.com/api/updatemitigationinfo.do -F\
  \"build_id=" + buildID  + '"' + " -F \"action=fp\""  + \
  " -F \"comment=" + comment + '"' + " -F \"flaw_id_list=" + flawID + '"'
  #print cmd
  s,o = commands.getstatusoutput(cmd)
  #if o.split(',')[1] == 'OK':
  #  print "Flaw id %s has been marked as a False Positive.\n"
  z = raw_input()


def acceptFlaw():
  """curl --compressed -u [username] https://analysiscenter.veracode.com/
  api/updatemitigationinfo.do
   -F "build_id=[your build ID] -F "action=accepted" -F
   "comment=[your comment text]" -F "flaw_id_list=[your flaw IDs]".
   """
  appusr = raw_input("Please enter API User: \n")
  apppass = getpass.getpass("Please enter API Password: \n")
  buildID = raw_input("Please enter Build ID: \n")
  flawID = raw_input("Please enter flaws separated by comma: \n")
  comment = raw_input("Please enter appropriate comment: \n")
  cmd = "curl -s --compressed -u " + appusr + ":" + apppass + \
  " https://analysiscenter.veracode.com/api/updatemitigationinfo.do -F\
  \"build_id=" + buildID  + '"' + " -F \"action=accepted\""  + \
  " -F \"comment=" + comment + '"' + " -F \"flaw_id_list=" + flawID + '"'
  #print cmd
  s,o = commands.getstatusoutput(cmd)
  #if o.split(',')[1] == 'OK':
  #  print "Flaw id %s has been accepted.\n"
  z = raw_input()

























