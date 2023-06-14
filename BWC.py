#!/usr/bin/env python 

from datetime import datetime
from time import strftime
from shutil import copyfile
import datetime, re
import time, os.path
import os
import numpy
from PIL import Image, ImageOps
from sendagmail import sendagmail

#========================= Constants definitions
config_file = '/home/pi/dev/BWC_pyth3/config.ini'
current_timestamp = ''
image_target_collection_path = ''
image_cntr=1


#========================= Constants load from config
from configobj import ConfigObj
config = ConfigObj(config_file)

logfile_path = config['Paths']['logfile']
image_target_for_webpage = config['Paths']['image_target_for_webpage']
image_target_collection_folder = config['Paths']['image_target_collection_folder']
webpage_path = config['Paths']['webpage_path']
ROI_X_start = config['Variables']['ROI_X_start']
ROI_Y_start = config['Variables']['ROI_Y_start']
ROI_X_end = config['Variables']['ROI_X_end']
ROI_Y_end = config['Variables']['ROI_Y_end']
Detection_variance_limit = config['Variables']['Detection_variance_limit']
Check_freq = config['Variables']['Check_freq']

#========================= function definitions 
def log_to_file(func_logfile_path,func_content):
	"""This function logs the content string into a logfile in 
	Timestam,content string,<CR>
	format."""
	with open(func_logfile_path,"a") as logfile:
		logfile.write(strftime("%Y-%m-%d %H:%M:%S")+","+func_content+"\n")

#========================= Program entry point

log_to_file(logfile_path,"Application started")

while True: 
	os.system("libcamera-jpeg -o temp.jpg -n --width 800 --height 600 --nopreview")
	image_target_collection_path = image_target_collection_folder + "/" + '{0:09}'.format(image_cntr)+".jpg"
	image = Image.open("temp.jpg")
	rotated_image = image.rotate(90, expand = True)
	rotated_image.save(image_target_for_webpage)
	
	image = ImageOps.grayscale(image)
	image = image.crop((int(ROI_X_start), int(ROI_Y_start), int(ROI_X_end), int(ROI_Y_end)))
	# Convert image to array
	image_arr = numpy.array(image)
	#print(f"Variance: {int(numpy.nanvar(image_arr))}")
	postbox_variance = int(numpy.nanvar(image_arr))
	if postbox_variance > int(Detection_variance_limit): 
		postboxmessage = "\nMail is in the box!"
		list_of_senders = []
		list_of_senders.append('-----@gmail.com')
		print("Mailing notification: \nto: \t\t" + list_of_senders[0])
		rotated_image.save("image_rotated.jpg")
		sendagmail(list_of_senders[0], "image_rotated.jpg", "PostPie Notifier","Hello, \n\nA mail was recently dropped into the mailbox!\n\n")  # toaddr, attachmentpath, subject, body_text
	else:
		postboxmessage = "\nPostbox is empty!"
	
	copyfile(image_target_for_webpage,image_target_collection_path)
	image_cntr = image_cntr + 1
	with open(webpage_path,"w") as webpage:
				#logfile.write(strftime("%Y-%m-%d %H:%M:%S")+",Started!\n")
				webpage.write("<!DOCTYPE html>\n<html>\n   <head>\n <title>PieCam</title>\n\n <b>"+ (strftime("%Y-%m-%d %H:%M:%S")) +"</b><br><br> \n   </head>\n   <body>\n<img src=""image.jpg"">\n <br>\n Variance is: "+str(postbox_variance) + postboxmessage + "     </body>\n</html>\n")
	time.sleep(int(Check_freq))
