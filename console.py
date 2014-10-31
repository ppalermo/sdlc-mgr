#!/usr/bin/python2.7
from functions import results, showMenu

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

if __name__ == '__main__':
  main()