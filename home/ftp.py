import time,os
from ftplib import FTP
fall_file=''
ir_file=''
def ftp_upload(filepath):
	IP = '127.0.0.1'
	user = 'johnlin'
	password = 'i5230303'
	filename = os.path.basename(filepath)
	ftp=FTP()
	#ftp.set_debuglevel(2) 
	ftp.connect(IP) 
	ftp.login(user,password)
	ftp.cwd("/home/johnlin/ftp")
	ftp.storbinary('STOR %s'%filename, open(filepath, 'rb',8192)) 
	print('success')

if __name__ == '__main__':
	while True:
		b=os.listdir('flask/static/ir_cam/20200807/AD-HF048-P-192.168.1.20')
		a=sorted(b)
		ir_path='flask/static/ir_cam/20200807/AD-HF048-P-192.168.1.20/'+a[len(a)-1]
		if not ir_path==ir_file:
			ftp_upload(ir_path)
			ir_file=ir_path

		b= os.listdir('flask/static/ir_cam/fall/') 
		for s in b:
			if s.endswith('.jpg')==False:
				print('del ',s)
				b.remove(s)
				
		a=sorted(b)
		fall_path='flask/static/ir_cam/fall/'+a[len(a)-1]
		print(fall_path)
		if not fall_path==fall_file:
			ftp_upload(fall_path)
			fall_file=fall_path	

		time.sleep(5)
