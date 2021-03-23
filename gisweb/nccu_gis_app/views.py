from django.shortcuts import render
from django.contrib import messages
from nccu_gis_app.models import imgData
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import logging
from PIL import Image
import exifread

imgWidthId = 256
imgLengthId = 257
pixelDix = 40962
pixelDiy = 40963
imgTimeId = 306
orientationId = 274
gpsTagId = 34853

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




def index(request):
	return render(request, "index.html")

def add(request):
	# all=maplist.objects.all()  #取得所有景點
	if('title' in request.POST):
		aTitle = request.POST['title']
		aContent = request.POST['content']
		aType = request.POST['type']
		apurl = request.FILES.get('purl', False)
		logger.debug(apurl)		
		fs = FileSystemStorage()
		filename = fs.save(apurl.name , apurl)
		path_name = "media/{}".format(apurl)
		basename = apurl.name
		exif = get_exif(path_name)	
		try:
			width = exif[imgWidthId]
			height = exif[imgLengthId]          
		except:
			width = exif[pixelDix]
			height = exif[pixelDiy]
		
		new_w = int(width / 10)
		new_h = int(height / 10)
		img = Image.open(path_name)
		rsize_img = img.resize((new_w, new_h))
		orientation = exif[orientationId]
		if(orientation == 6):
			ori_img = rsize_img.transpose(Image.ROTATE_270)
			ori_img.save('media/reImg/re_{}'.format(basename), 'JPEG')
			new_h , new_w = new_w, new_h
			print('90')
		elif(orientation == 8):
			ori_img = rsize_img.transpose(Image.ROTATE_90)
			ori_img.save('media/reImg/re_{}'.format(basename), 'JPEG')
			new_h , new_w = new_w, new_h
			print('270')
		elif(orientation == 2):
			ori_img = rsize_img.transpose(Image.FLIP_LEFT_RIGHT)
			ori_img.save('media/reImg/re_{}'.format(basename), 'JPEG')
			print('180')
		elif(orientation == 4):
			ori_img = rsize_img.transpose(Image.FLIP_TOP_BOTTOM)
			ori_img.save('media/reImg/re_{}'.format(basename), 'JPEG')
			print('180')
		elif(orientation == 5):
			ori_img = rsize_img.transpose(Image.FLIP_LEFT_RIGHT)
			ori_img_f = rsize_img.transpose(Image.ROTATE_90)
			ori_img_f.save('media/reImg/re_{}'.format(basename), 'JPEG')
			print('180')
		elif(orientation == 7):
			ori_img = rsize_img.transpose(Image.FLIP_LEFT_RIGHT)
			ori_img_f = rsize_img.transpose(Image.ROTATE_270)
			ori_img_f.save('media/reImg/re_{}'.format(basename), 'JPEG')
			print('180')
		elif(orientation == 3):
			ori_img = rsize_img.transpose(Image.ROTATE_180)
			ori_img.save('media/reImg/re_{}'.format(basename), 'JPEG')
			print('180')		
		else:
			rsize_img.save('media/reImg/re_{}'.format(basename), 'JPEG')
			print('else')
		gpsInfo = exif[gpsTagId]
		lat_str = gpsInfo[2]
		lat = format_lat_lon(lat_str)
		lon_str = gpsInfo[4]
		lon = format_lat_lon(lon_str)   
		rec = imgData(title = aTitle, content = aContent, type = aType, purl = apurl, lon = lon, lat = lat)
		rec.save()
		return render(request, "index.html")
	else:
	    return render(request, "add.html")

def map(request):		
	if request.method == "POST":
		getTitle = request.POST['title']
		getType = request.POST['type']
		all = imgData.objects.filter(title__contains = "{}".format(getTitle), type = "{}".format(getType))
		return render(request, "map.html", locals())
	else:
	    all = imgData.objects.all()  #取得所有景點
	    return render(request, "map.html", locals())


def login(request):
	return render(request, "login.html")	

# Create your views here.
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def format_lat_lon(data):
    dd = float(data[0])
    mm = float(data[1]) / 60
    ss = float(data[2]) / 3600
    
    result = dd + mm + ss
    return result


