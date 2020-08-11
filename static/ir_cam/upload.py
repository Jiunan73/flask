#encoding:utf-8
from ftplib import FTP
import os
import fileinput
import time
# 该条件永远为true，循环将无限执行下去

def ftp_upload(localfile, remotefile):
    fp = open(localfile, 'rb')
    ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
    fp.close()
#print ("after upload " + localfile + " to " + remotefile)
print('1')

localdir = "/home/thomaslee/Desktop/Fall_detect/fall/image/"

def upload_img(file):
    ftp_upload(localdir +"/"+ file, file)

while(True):
    time.sleep(10)
    ftp = FTP()
    ftp.set_debuglevel(2)
    try:
        ftp.connect('192.168.0.122', 21)
        ftp.login('pi','Auo+1231')
        ftp.cwd('/home/pi/tmp')
    except Exception as e:
        print(e)
        continue
    lastlist = []

    newfiles = os.listdir(localdir)
    #newfiles = list(set(currentlist) - set(lastlist))
    if len(newfiles) == 0:
        print ('No files need to upload')
    else:
        print(len(newfiles))
        for needupload in newfiles:
            
            print( "uploading " + localdir + '/'+ needupload)
            upload_img(needupload)
    ftp.quit()

    

