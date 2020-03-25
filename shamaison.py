# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests
from time import sleep
import re

domein = "https://www.shamaison.com"
domein_html = urllib.request.urlopen(domein)

def list_whole(html):
	soup = BeautifulSoup(html, 'html.parser')
	Prefecture_search = soup.find("div", class_="topBoxInr02 clearfix")
	global Prefecture_text
	Prefecture_text = Prefecture_search.h1.text
	target = soup.find("div", class_="topBoxInr02 clearfix")
	target2 = target.find_all("li")
	global area
	area = target2[0].a.get("href")
	global line
	line = target2[1].a.get("href")

def line_area_get(target_url):
	line_area_url = domein + target_url
	html = urllib.request.urlopen(line_area_url)
	soup = BeautifulSoup(html, "html.parser")
	line_area = soup.find("div", class_="contentsBodyInr")
	station_list = []
	if target_url == area:
		line_area2 = line_area.select('ul[class="checkListA01 checkList4n searchBtn"] > li')
	elif target_url == line:
		line_area2 = line_area.select('ul[class="checkListA03 checkList3n searchBtn05"] > li')
		for result in line_area2:
			line_url = result.a.get("href")
			line_url2 = "https://www.shamaison.com" + line_url
			html2 = urllib.request.urlopen(line_url2)
			soup2 = BeautifulSoup(html2, "html.parser")
			station = soup2.find("ul", class_="clearfix heightLineParent searchBtn")
			station2 = station.find_all("li")
			for station_result in station2:
				station_name = station_result.text.strip()
				station_url = station_result.a.get("href")
				station_url_result = "https://www.shamaison.com" + station_url
				list2 = []
				list2.append(Prefecture_text)
				list2.append(station_name)
				list2.append(station_url_result)
				station_list.append(list2)
		print (station_list) 

		df_station = pd.DataFrame(station_list)
		with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
			df_station.to_excel(ew, sheet_name= Prefecture_text + "_" + '駅', header=False, index=False)

	line_area_list = []
	for result in line_area2:
		city = result.span.text
		city_count = result.find_all("span")
		city_count_result = city_count[1].text		
		line_area_url2 = result.a.get("href")
		list1 = []
		list1.append(Prefecture_text)
		list1.append(city)
		list1.append(city_count_result)
		list1.append(domein + line_area_url2)
		line_area_list.append(list1)
	print (line_area_list)
	
	df_line = pd.DataFrame(line_area_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		if target_url == area:
			df_line.to_excel(ew, sheet_name= Prefecture_text + "_" + '市町村', header=False, index=False)
		elif target_url == line:
			df_line.to_excel(ew, sheet_name= Prefecture_text + "_" +'路線', header=False, index=False)


def url_get():
	soup = BeautifulSoup(domein_html, 'html.parser')
	target = soup.find("div", class_="indexBoxLeft")
	target2 = target.select('ul[class="clearfix"] > li')
	target2.pop()
	for url in target2:
		target_href = url.a.get("href")
		if str("hokkaido") in target_href:
			global hokkaido_html
			hokkaido_html = domein + target_href
			hokkaido_html2 = urllib.request.urlopen(hokkaido_html)
			list_whole(hokkaido_html2)
			line_area_get(area)
			line_area_get(line)

		elif str("aomori") in target_href or str("iwate") in target_href or str("miyagi") in target_href or str("akita") in target_href or str("yamagata") in target_href or str("fukushima") in target_href:
			global tohoku_html
			tohoku_html = domein + target_href
			tohoku_html2 = urllib.request.urlopen(tohoku_html)
			list_whole(tohoku_html2)
			line_area_get(area)
			line_area_get(line)

		elif str("tokyo") in target_href or str("kanagawa") in target_href or str("saitama") in target_href or str("chiba") in target_href or str("ibaraki") in target_href or str("tochigi") in target_href or str("gunma") in target_href or str("yamanashi") in target_href:
			global syuto_html
			syuto_html = domein + target_href
			syuto_html2 = urllib.request.urlopen(syuto_html)
			list_whole(syuto_html2)
			line_area_get(area)
			line_area_get(line)

		elif str("niigata") in target_href or str("nagano") in target_href or str("toyama") in target_href or str("ishikawa") in target_href or str("fukui") in target_href or str("aichi") in target_href or str("gifu") in target_href or str("shizuoka") in target_href or str("mie") in target_href:
			global tyubu_html
			tyubu_html = domein + target_href
			tyubu_html2 = urllib.request.urlopen(tyubu_html)
			list_whole(tyubu_html2)
			line_area_get(area)
			line_area_get(line)

		elif str("osaka") in target_href or str("hyogo") in target_href or str("kyoto") in target_href or str("shiga") in target_href or str("nara") in target_href or str("wakayama") in target_href:
			global kansai_html
			kansai_html = domein + target_href
			kansai_html2 = urllib.request.urlopen(kansai_html)
			list_whole(kansai_html2)
			line_area_get(area)
			line_area_get(line)

		elif str("tottori") in target_href or str("shimane") in target_href or str("okayama") in target_href or str("hiroshima") in target_href or str("yamaguchi") in target_href or str("tokushima") in target_href or str("kagawa") in target_href or str("ehime") in target_href or str("kochi") in target_href:
			global tyugokushikoku_html
			tyugokushikoku_html = domein + target_href
			tyugokushikoku_html2 = urllib.request.urlopen(tyugokushikoku_html)
			list_whole(tyugokushikoku_html2)
			line_area_get(area)
			line_area_get(line)

		elif str("fukuoka") in target_href or str("saga") in target_href or str("nagasaki") in target_href or str("kumamoto") in target_href or str("oita") in target_href or str("miyazaki") in target_href or str("kagoshima") in target_href:
			global kyusyu_html
			kyusyu_html = domein + target_href
			kyusyu_html2 = urllib.request.urlopen(kyusyu_html)
			list_whole(kyusyu_html2)
			line_area_get(area)
			line_area_get(line)

if __name__ == "__main__":
	url_get()

	
