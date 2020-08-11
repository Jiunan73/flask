import time,os,datetime
from ftplib import FTP
fall_file=''
ir_file=''
def ftp_upload(filepath,dirpath):
	IP = '192.168.31.102'
	user = 'johnlin'
	password = 'FA$admin01'
	filename = os.path.basename(filepath)
	ftp=FTP()
	#ftp.set_debuglevel(2)
	ftp.connect(IP)
	ftp.login(user,password)
	ftp.cwd("/home/johnlin/ftp/"+dirpath)
	ftp.storbinary('STOR %s'%filename, open(filepath, 'rb',8192)) 
	print('success')


if __name__ == '__main__':
	while True:
		try:
			datestr=datetime.datetime.now().strftime('%Y%m%d')
			b=os.listdir('static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20')
			a=sorted(b)
			ir_path='static/ir_cam/'+datestr+'/AD-HF048-P-192.168.1.20/'+a[len(a)-1]
			print(ir_path)
			if not ir_path==ir_file:
				print('ftp upload')
				ftp_upload(ir_path,'ir')
				ir_file=ir_path
		except:
			print('ir error')
		try:
			b= os.listdir('static/ir_cam/fall/') 
			for s in b:
				if s.endswith('.jpg')==False:
					#print('del ',s)
					b.remove(s)

			a=sorted(b)
			fall_path='static/ir_cam/fall/'+a[len(a)-1]
			print(fall_path)
			if not fall_path==fall_file:
				print('ftp upload')
				ftp_upload(fall_path,'fall')
				fall_file=fall_path
		except:
			print('fall error')
		time.sleep(5)
