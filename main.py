import pymongo
from pymongo import MongoClient
# import gridfs
# from gridfs import GridFS

import urllib
import requests
from bs4 import BeautifulSoup

import numpy as np
from PIL import Image 
from io import BytesIO, StringIO

import pickle
import bson

import time 


test_image_url = "https://media.gettyimages.com/photos/teenager-with-afro-hair-style-picture-id1042424400?k=6&amp;m=1042424400&amp;s=612x612&amp;w=0&amp;h=E6YMIj4RFZyaOdUM8c07ef6APoqTDKTzjysNak_iOP0="

user = ""
pswd = ""

client = pymongo.MongoClient("mongodb+srv://{}:{}@cluster0.ihx5p.mongodb.net/<dbname>?retryWrites=true&w=majority".format(user, pswd))
db = client["DATA_603"]
collection = db["test_images"]
# fs = GridFS(database=db, collection=collection)


def gather_images_old(query="African American", num_pages=1):
	image_num = 0
	for page in range(1,num_pages+1):
		# url = "https://www.gettyimages.com/photos/african-american-portrait?mediatype=photography&page={}&phrase={}%20portrait&sort=mostpopular".format(page, query)
		url = "https://www.gettyimages.com/search/2/image?phrase={}+portrait".format(query)

		img_list = []

		while len(img_list) == 0:

			r = requests.get(url)
			print("status_code", r.status_code)
			soup = BeautifulSoup(r.text, "html.parser")

			img_list = [x.get("src") for x in soup.find_all("img", {"ng-class":"thumbClassNames"}) if x.get("alt")!=""]

			if len(img_list) == 0:
				continue

			for i in range(len(img_list)):
				# print(i)
				# r_ = requests.get(img_list[i]) # Needed a read() funciton, so couldnt use this approach
				# image_bytes = BytesIO(r_.content)
				# image = Image.open(image_bytes)

				image_bytes = urllib.request.urlopen(img_list[i]).read() # type = bytes
				image = Image.open(BytesIO(image_bytes)) # type = PIL.JpegImagePlugin.JpegImageFile'
				# image.show() 
				
				# https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
				image_np = np.array(image) # Good for Sklearn
				# Image.fromarray(image_np, 'RGB').show() # How to display images from np arr
			
				# How to handle np arrays in mongoDB
				# https://stackoverflow.com/questions/6367589/saving-numpy-array-in-mongodb
				temp = {
					"_id": "{}_{}".format(query, image_num).replace(" ", "_"),
					# "photo_in_bytes": image_bytes,
					"source_url": img_list[i],
					"numpy_arr": bson.binary.Binary( pickle.dumps( image_np, protocol=2) ),
					"race": query
				}

				try:
					collection.insert_one(temp)
				except:
					collection.find_one_and_replace({"_id": temp["_id"]}, temp)
					# if temp["_id"] in collection.find({"_id" : temp["_id"]}): 
					# del doc['_id'] 
					# collection.insert_one(temp)

				image_num += 1

				# fs.put(temp)
				
				# gridfs.grid_file.GridIn(root_collection=collection,
				# 	_id=i, content_type=r_.headers["Content-Type"]).write(image)

				# with cv.imread(img_list[i]) as img:
				# 	b = fs.put(img, filename="foo")

def gather_images(query="African American", num_pages=1):
	image_num = 0
	for page in range(1,num_pages+1):
		# url = "https://www.gettyimages.com/photos/african-american-portrait?mediatype=photography&page={}&phrase={}%20portrait&sort=mostpopular".format(page, query)
		# url = "https://www.gettyimages.com/search/2/image?phrase={}+portrait".format(query)

		img_list = get_from_shutterfly(query, page)

		for i in range(len(img_list)):

			image_bytes = urllib.request.urlopen(img_list[i]).read() # type = bytes
			image = Image.open(BytesIO(image_bytes)) # type = PIL.JpegImagePlugin.JpegImageFile'
			# image.show() 
			
			# https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
			image_np = np.array(image) # Good for Sklearn
			# Image.fromarray(image_np, 'RGB').show() # How to display images from np arr
		
			# How to handle np arrays in mongoDB
			# https://stackoverflow.com/questions/6367589/saving-numpy-array-in-mongodb
			temp = {
				"_id": "{}_{}".format(query, image_num).replace(" ", "_"),
				# "photo_in_bytes": image_bytes,
				"source_url": img_list[i],
				"numpy_arr": bson.binary.Binary( pickle.dumps( image_np, protocol=2) ),
				"race": query
			}

			try:
				collection.insert_one(temp)
			except:
				collection.find_one_and_replace({"_id": temp["_id"]}, temp)

			image_num += 1

def get_from_getty(query="African American", page_num=1):

	# url = "https://www.gettyimages.com/search/2/image?phrase={}+portrait".format(query)
	url = "https://www.gettyimages.com/photos/african-american-portrait?mediatype=photography&page={}&phrase={}%20portrait&sort=mostpopular".format(page_num, query)
	img_list = []

	while len(img_list) == 0:

		header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" } 
		r = requests.get(url, headers=header)
		print("status_code", r.status_code)
		# print("headers", r.headers)
		soup = BeautifulSoup(r.text, "html.parser")

		img_list = [x.get("src") for x in soup.find_all("img", {"ng-class":"thumbClassNames"}) if x.get("alt")!=""]
		# for img in soup.find_all("img", {"class":"z_h_9d80b z_h_2f2f0", "data-automation":"mosaic-grid-cell-image"}):
		# 	img_list.append(img.get("src"))

		if len(img_list) == 0:
			continue

		print("Number of Images", len(img_list))
		return img_list


def get_from_shutterfly(query="African American", page_num=1):

	# url = "https://www.shutterstock.com/search/{}?page={}".format(query.replace(" ", "+"), page_num)
	url = "https://www.shutterstock.com/search/{}+portrait?&mreleased=true&number_of_people=1&exclude_keywords=group%2C+couple%2C+family%2C+married%2C+and&page={}".format(query.replace(" ", "+"), page_num)
	img_list = []

	while len(img_list) == 0:

		header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" } 
		r = requests.get(url, headers=header)
		print("status_code", r.status_code)
		# print("headers", r.headers)
		soup = BeautifulSoup(r.text, "html.parser")

		# img_list = [x.get("src") for x in soup.find_all("img", {"class":"z_h_9d80b z_h_2f2f0", "data-automation"="mosaic-grid-cell-image"}) if x.get("alt")!=""]
		for img in soup.find_all("img", {"class":"z_h_9d80b z_h_2f2f0", "data-automation":"mosaic-grid-cell-image"}):
			img_list.append(img.get("src"))

		if len(img_list) == 0:
			# print("update soup query")
			# break
			continue

		print("Number of Images", len(img_list))
		return img_list

def test_unsplash():
	"""
	<img class="_2VWD4 _2zEKz" 
	 alt="smiling man standing on sand shore during day" 
	 sizes="(min-width: 1335px) 416px, (min-width: 992px) calc(calc(100vw - 72px) / 3), (min-width: 768px) calc(calc(100vw - 48px) / 2), 100vw" 
	 srcset="https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60 100w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60 200w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=300&amp;q=60 300w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=400&amp;q=60 400w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=60 500w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=600&amp;q=60 600w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=700&amp;q=60 700w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=800&amp;q=60 800w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=900&amp;q=60 900w,
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1000&amp;q=60 1000w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1100&amp;q=60 1100w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1200&amp;q=60 1200w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1296&amp;q=60 1296w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1400&amp;q=60 1400w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1600&amp;q=60 1600w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=1800&amp;q=60 1800w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=2000&amp;q=60 2000w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=2200&amp;q=60 2200w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=2400&amp;q=60 2400w, 
	         https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=2592&amp;q=60 2592w" 
	 src="https://images.unsplash.com/photo-1541614636992-adddbcf47eaa?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;w=1000&amp;q=80" 
	 itemprop="thumbnailUrl" data-test="photo-grid-multi-col-img" 
	 style="background-color: rgb(15, 13, 14);">
	"""
	url = "https://unsplash.com/s/photos/african-american-portrait" # 200
	img_list = []

	while len(img_list) == 0:

		r = requests.get(url)
		print("status_code", r.status_code)
		# print("headers", r.headers)
		soup = BeautifulSoup(r.text, "html.parser")
		print(soup.prettify())

		# img_list = [x.get("src") for x in soup.find_all("img", {"class":"z_h_9d80b z_h_2f2f0", "data-automation"="mosaic-grid-cell-image"}) if x.get("alt")!=""]
		for img in soup.find_all("img"):
			if "srcset" in img.attrs.keys():
				img_list.append(img["srcset"].split(", ")[-1])
			else:
				img_list.append(img.get("src"))

		if len(img_list) == 0:
			# print("update soup query")
			# break
			continue

		print("Number of Images", len(img_list))
		return img_list

def test_google():
	# you can change the query for the image  here  
	query = "dog"
	query= query.split()
	query='+'.join(query)


	url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	# header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'} 
	
	header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" } 
	r = requests.get(url, headers=header)
	soup = BeautifulSoup(r.text, "html.parser")

	img_list = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
	print(len(img_list))

	#print images
	for img in img_list:
		image_bytes = urllib.request.urlopen(img_list[i]).read() # type = bytes
		image = Image.open(BytesIO(image_bytes)) # type = PIL.JpegImagePlugin.JpegImageFile'
		image.show() 

def check_db_collection(race="African American"):
	count = 0
	cursor = collection.find({"race": race})
	for document in cursor:
		# num = document["_id"]
		# print(num)
		# num = num.split("_")[-1]
		# print(num)
		# if int(num) % 10 == 0:
		print(document["_id"])
		img = pickle.loads( document["numpy_arr"] )
		Image.fromarray(img, 'RGB').show(title=document["_id"])
		count += 1 
		if count == 10:
			return 

def main():
	race_categories = ["African American", "White", "American Indian", "Asian", "Latino", "Native Hawaiian", ]
	num_pages = 5

	for race in race_categories:
		for page in range(1, num_pages+1):
			print("{:=^100}".format("{} pg. {}".format(race, page)))
			gather_images(race, page)

		check_db_collection(race)

	# for i in range(60):
	# 	collection.delete_one({"_id": i})	

start_time = time.time()
main()
print("--- %s seconds ---" % round(time.time() - start_time, 2))

	
