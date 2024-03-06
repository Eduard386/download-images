# python download_images.py --output downloads

import argparse
import requests
from user_agent import generate_user_agent
import time
import os
from bs4 import BeautifulSoup

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output directory of images")
ap.add_argument("-c", "--category", required=True, help="category name")
ap.add_argument("-s", "--num-pages-start", type=int, default=1, help="# of pages with 100 images per each")
ap.add_argument("-f", "--num-pages-finish", type=int, default=1, help="# of pages with 100 images per each")
ap.add_argument("-a", "--amount-of-saved-images", type=int, default=0, help="# of already saved images")
args = vars(ap.parse_args())

url = "https://www.shutterstock.com/search/{category}?image_type=photo&page=".format(category=args["category"])
amount_of_saved_images = args["amount_of_saved_images"]

session = requests.session()
session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
os.system("brew services start tor")

for i in range(args["num_pages_start"], args["num_pages_finish"] + 1):
	try:
		# generate headers for User Agent, not to be blocked
		headers = {'User-Agent': generate_user_agent(device_type="desktop", navigator="firefox", os=('mac', 'linux'))}

		# Restart Tor and generate new headers
		os.system("brew services restart tor")
		time.sleep(10)
		print("TOR restarted")

		# page to work with
		print("[INFO] Will work with URL " + str(url + '{}'.format(i)))

		# Find all images on the page
		page_response = requests.get(str(url + '{}'.format(i)), headers=headers, timeout=10)
		if page_response.status_code == 200:
			print('Successfully opened {} page'.format(i))
		else:
			print('Failed to open {number} page! Status code {code}'.format(number=i, code=page_response.status_code))
		page_content = BeautifulSoup(page_response.content, "lxml")
		images = page_content.findAll('img')

		# grab every image on the page
		for image in images:
			r = session.get(image['src'], headers=headers, timeout=10)

			# save the image to disk
			p = os.path.sep.join([args["output"], "{}.jpg".format(str(amount_of_saved_images).zfill(5))])
			f = open(p, "wb")
			f.write(r.content)
			f.close()

			# update the counter
			print("[INFO] downloaded: {}".format(p))
			amount_of_saved_images += 1
			time.sleep(0.1)

	except Exception as e: print(e)

	os.system("brew services stop tor")


