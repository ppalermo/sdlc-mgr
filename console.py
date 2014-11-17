#!/usr/bin/python2.7
from functions import results, showMenu, admin, userAdmin
#Comment
def main():
  option = ''
  while option != 'exit':
    option = showMenu.MainMenu()
    if option == '1':
      results.listApps()
    elif option == '2':
      results.getBuild()
    elif option == '3':
      results.getHighFlaws()
    elif option == '4':
      results.getSev4Flaws()
    elif option == '5':
      results.getSev5Flaws()
    elif option == '6':
      results.getFlawsSummary()
    #Below starts the Admin Menu stuff...
    elif option == '7':
      option = admin.adminMenu()
      if option == '1':
        admin.setFalsePositive()
      elif option == '2':
        admin.acceptFlaw()
    elif option == '8':
      option = userAdmin.UserAdminMenu()
      if option == '1':
        userAdmin.listAllUsers()

if __name__ == '__main__':
  main()