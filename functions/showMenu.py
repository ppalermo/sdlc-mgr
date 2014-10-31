def MainMenu():
  #Show some Menu here:
  print "*****************************************************"
  print "*****************************************************"
  print "*************Veracode's API Mgmt...******************"
  print "*****************************************************"
  print "*****************************************************"

  print '\n'
  print "Select the option by pressing the number you want: \n"

  print "- List all applications on Veracode: \"1\" \n "
  print "- Get list of builds by Application ID: \"2\" \n "
  print "- List modules with SEV4 and SEV5 Flaws: \"3\" \n "
  print "- List details of \"High Severity\" Flaws by buildID: \"4\" \n "
  print "- List details of \"VERY High Severity\" Flaws by buildID: \"5\" \n "
  print "- Go To Admin Menu: \"6\" \n "

  print "\n-QUIT: \"exit\""
  opt = raw_input()
  return opt