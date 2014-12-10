"""uploadfile.do
The uploadfile.do call uploads a file to an existing build of an application.
You cannot upload to a build that is in a pre-scan state, which is the state a scan
is in after beginprescan.do calls the pre-scan.
The uploadfile.do call creates a build if one does not already exist or if
the most recent build has a published static scan, therefore, it is not necessary
to also call createbuild.do as part of the Upload API workflow.

Parameters
app_id     :  Integer. Required.
file  File : Required.
sandbox_id :  Integer. Optional. Enter the ID of the sandbox to which you want to upload the file.
save_as String : Optional. Enter the new filename you want to give the file.
Do not use slashes in the name or periods at the beginning or end of the name.

"""
#Source: https://analysiscenter.veracode.com/auth/helpCenter/api/r_uploadfile.html
#import xml.etree.cElementTree as ET
#import commands
#import os
import ConfigParser
import logging

#configpath = '/Users/martin/GitHub/sdlc-manager/functions/veracode.cfg'

def uploadbuild():
  resource_url = 'https://analysiscenter.veracode.com/api/4.0/uploadfile.do'




