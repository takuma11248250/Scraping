# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests
from time import sleep
import re
import openpyxl

hukuoka = "https://s.shamaison.com/search/area?PRF=40&MD=1"
saga = "https://s.shamaison.com/search/area?PRF=41&MD=1"
nagasaki = "https://s.shamaison.com/search/area?PRF=42&MD=1"
kumamoto = "https://s.shamaison.com/search/area?PRF=43&MD=1"
ooita = "https://s.shamaison.com/search/area?PRF=44&MD=1"
miyazaki = "https://s.shamaison.com/search/area?PRF=45&MD=1"
kagosima = "https://s.shamaison.com/search/area?PRF=46&MD=1"

def get_area_url():
	for get_url in url_list:
		get_html = urllib.request.urlopen(get_url)
		soup = BeautifulSoup(get_html, 'html.parser')
		Prefecture_text = soup.find("div", class_="listBoxinner02").text
		area = soup.find_all("ul", class_="ulLinkBox")
		area_whole_list = []
		for result in area:
			area_list = result.select('ul[class="ulLinkBox"] > li')
			for target_url_list in area_list:
				target_text = target_url_list.text 
				target_url = target_url_list.a.get("href")
				target_url_result = "https://s.shamaison.com" + target_url
				raw_list = []
				raw_list.append(target_text)
				raw_list.append(target_url_result)
				area_whole_list.append(raw_list)
		print (area_whole_list)

		
		area_df = pd.DataFrame(area_whole_list)
		with pd.ExcelWriter("area_get_url.xlsx", engine="openpyxl", mode="a") as ew:
			area_df.to_excel(ew, sheet_name= Prefecture_text, header=False, index=False)
		
if __name__ == "__main__":
	url_list = [hukuoka, saga, nagasaki, kumamoto, ooita, miyazaki, kagosima]
	#wb = openpyxl.Workbook()
	#wb.save("area_get_url.xlsx")
	get_area_url()


	
