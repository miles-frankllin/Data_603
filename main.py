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


def gather_images(query="African American", num_pages=1):
	for page in range(1,num_pages+1):
		url = "https://www.gettyimages.com/photos/african-american-portrait?mediatype=photography&page={}&phrase={}%20portrait&sort=mostpopular".format(page, query)

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
					"_id": "{}_{}".format(query, i).replace(" ", "_"),
					# "photo_in_bytes": image_bytes,
					"source_url": img_list[i],
					"numpy_arr": bson.binary.Binary( pickle.dumps( image_np, protocol=2) ),
					"race": query
				}
				try:
					collection.insert_one(temp)
				except:
					collection.updateOne({"_id": temp["_id"]}, {"numpy_arr": bson.binary.Binary( pickle.dumps( image_np, protocol=2) )})
				# fs.put(temp)
				
				# gridfs.grid_file.GridIn(root_collection=collection,
				# 	_id=i, content_type=r_.headers["Content-Type"]).write(image)

				# with cv.imread(img_list[i]) as img:
				# 	b = fs.put(img, filename="foo")

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
	num_pages = 1

	for race in race_categories:
		print("{:=^100}".format(race))
		#gather_images(race)

		check_db_collection(race)

	# for i in range(60):
	# 	collection.delete_one({"_id": i})	

start_time = time.time()
main()
print("--- %s seconds ---" % round(time.time() - start_time, 2))

	
