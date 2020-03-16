# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import requests
from time import sleep
import re

#対象URL
hokkaido = "https://www.mast-net.jp/hokkaido/"
tohoku ="https://www.skwf.net/tohoku/condition/"
syuto = "https://www.mast-net.jp/"
chubu = "http://chintai.sekiwachubu.co.jp/"
kansai = "https://www.skwf.net/kansai/"
chugoku = "https://www.skwf.net/chugoku/"
kyusyu = "https://www.skwf.net/ky/condition/"

#北海道
hokkaido_html = urllib.request.urlopen(hokkaido)

#東北
tohoku_html = urllib.request.urlopen(tohoku)
#九州
kyusyu_html = urllib.request.urlopen(kyusyu)

#首都
syuto_html = urllib.request.urlopen(syuto)

#中部
chubu_html = urllib.request.urlopen(chubu)

#関西
kansai_html = urllib.request.urlopen(kansai)
#中国
chugoku_html = urllib.request.urlopen(chugoku)

def kansai_chugoku(html):
#一覧情報取得取得
	soup = BeautifulSoup(html, 'html.parser')
	target = soup.find("div", class_="areaInner")
	target2 = target.find_all("li")
	line_list = []
	area_list = []
	station_list = []
	for first_url in target2:
		if first_url.a in first_url:
			if str("route") in first_url.a.get("href"):
				line = first_url.a.get("href")
				line_area_url = "https://www.skwf.net" + line
				html = urllib.request.urlopen(line_area_url)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				line_ = soup.find("section", class_="routeSelectArea")
				line_2 = line_.find_all("li")

				for result in line_2:
					if result.a in result:
						line_url2 = result.a.get("href")
						line_url3 = "https://www.skwf.net" + line_url2
						html2 = urllib.request.urlopen(line_url3)
						soup2 = BeautifulSoup(html2, "html.parser")
						station = soup2.find("div", class_="staListBox checkAllWrap_01")
						station2 = station.find_all("li")
						for station_result in station2:
							if station_result.a in station_result:
								station_name = station_result.text.strip()
								station_url = station_result.a.get("href")
								station_url_result = "https://www.skwf.net" + station_url
								list2 = []
								list2.append(Prefecture)
								list2.append(station_name)
								list2.append(station_url_result)
								station_list.append(list2)
				#リスト化
				for result in line_2:
					if result.a in result:
						city = result.span.text
						line_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.skwf.net" + line_url2)
						line_list.append(list1)

			elif str("area") in first_url.a.get("href"):
				area = first_url.a.get("href")
				line_area_url = "https://www.skwf.net" + area
				html = urllib.request.urlopen(line_area_url)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				area_ = soup.find("section", class_="routeSelectArea")
				area_2 = area_.find_all("li")

				#リスト化
				for result in area_2:
					if result.a in result:
						city = result.span.text
						area_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.skwf.net" + area_url2)
						area_list.append(list1)
	print (line_list)
	print (area_list)
	print (station_list)						
	df_line = pd.DataFrame(line_list)
	df_area = pd.DataFrame(area_list)
	df_station = pd.DataFrame(station_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		df_line.to_excel(ew, sheet_name='沿線', header=False, index=False)
		df_area.to_excel(ew, sheet_name='市町村', header=False, index=False)
		df_station.to_excel(ew, sheet_name='駅', header=False, index=False)

def chubu(html):
#一覧情報取得取得
	soup = BeautifulSoup(html, 'html.parser')
	target = soup.find("section", class_="area")
	target2 = target.find_all("dd")
	line_list = []
	area_list = []
	station_list = []
	for first_url in target2:
		if first_url.a in first_url:
			if str("route") in first_url.a.get("href"):
				line = first_url.a.get("href")
				html = urllib.request.urlopen(line)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				line_ = soup.find("section", class_="routeSelectArea")
				line_2 = line_.find_all("li")

				for result in line_2:
					if result.a in result:
						line_url2 = result.a.get("href")
						line_url3 = "https://www.skwf.net" + line_url2
						html2 = urllib.request.urlopen(line_url3)
						soup2 = BeautifulSoup(html2, "html.parser")
						station = soup2.find("div", class_="staListBox checkAllWrap_01")
						station2 = station.find_all("li")
						for station_result in station2:
							if station_result.a in station_result:
								station_name = station_result.text.strip()
								station_url = station_result.a.get("href")
								station_url_result = "https://www.skwf.net" + station_url
								list2 = []
								list2.append(Prefecture)
								list2.append(station_name)
								list2.append(station_url_result)
								station_list.append(list2)
				#リスト化
				for result in line_2:
					if result.a in result:
						city = result.span.text
						line_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.skwf.net" + line_url2)
						line_list.append(list1)

			elif str("area") in first_url.a.get("href"):
				area = first_url.a.get("href")
				#line_area_url = "https://www.skwf.net" + area
				html = urllib.request.urlopen(area)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				area_ = soup.find("section", class_="routeSelectArea")
				area_2 = area_.find_all("li")

				#リスト化
				for result in area_2:
					if result.a in result:
						city = result.span.text
						area_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.skwf.net" + area_url2)
						area_list.append(list1)
	print (line_list)
	print (area_list)
	print (station_list)						
	df_line = pd.DataFrame(line_list)
	df_area = pd.DataFrame(area_list)
	df_station = pd.DataFrame(station_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		df_line.to_excel(ew, sheet_name='沿線', header=False, index=False)
		df_area.to_excel(ew, sheet_name='市町村', header=False, index=False)
		df_station.to_excel(ew, sheet_name='駅', header=False, index=False)

def syuto(html):
#一覧情報取得取得
	soup = BeautifulSoup(html, 'html.parser')
	target = soup.find("div", class_="areaInner")
	target2 = target.find_all("li")
	line_list = []
	area_list = []
	station_list = []
	for first_url in target2:
		if first_url.a in first_url:
			if str("route") in first_url.a.get("href"):
				line = first_url.a.get("href")
				line_area_url = "https://www.mast-net.jp" + line
				html = urllib.request.urlopen(line_area_url)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				line_ = soup.find("section", class_="routeSelectArea")
				line_2 = line_.find_all("li")

				for result in line_2:
					if result.a in result:
						line_url2 = result.a.get("href")
						line_url3 = "https://www.mast-net.jp" + line_url2
						html2 = urllib.request.urlopen(line_url3)
						soup2 = BeautifulSoup(html2, "html.parser")
						station = soup2.find("div", class_="staListBox checkAllWrap_01")
						station2 = station.find_all("li")
						for station_result in station2:
							if station_result.a in station_result:
								station_name = station_result.text.strip()
								station_url = station_result.a.get("href")
								station_url_result = "https://www.mast-net.jp" + station_url
								list2 = []
								list2.append(Prefecture)
								list2.append(station_name)
								list2.append(station_url_result)
								station_list.append(list2)
				#リスト化
				for result in line_2:
					if result.a in result:
						city = result.span.text
						line_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.mast-net.jp" + line_url2)
						line_list.append(list1)

			elif str("area") in first_url.a.get("href"):
				area = first_url.a.get("href")
				line_area_url = "https://www.mast-net.jp" + area
				html = urllib.request.urlopen(line_area_url)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				area_ = soup.find("section", class_="routeSelectArea")
				area_2 = area_.find_all("li")

				#リスト化
				for result in area_2:
					if result.a in result:
						city = result.span.text
						area_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.mast-net.jp" + area_url2)
						area_list.append(list1)
	print (line_list)
	print (area_list)
	print (station_list)						
	df_line = pd.DataFrame(line_list)
	df_area = pd.DataFrame(area_list)
	df_station = pd.DataFrame(station_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		df_line.to_excel(ew, sheet_name='沿線', header=False, index=False)
		df_area.to_excel(ew, sheet_name='市町村', header=False, index=False)
		df_station.to_excel(ew, sheet_name='駅', header=False, index=False)

def tohoku_kyusyu(html):
#一覧情報取得
	soup = BeautifulSoup(html, 'html.parser')
	target = soup.find("div", class_="mapAreaBtn")
	target2 = target.find_all("li")
	line_list = []
	area_list = []
	station_list = []
	for first_url in target2:
		if first_url.a in first_url:
			if str("route") in first_url.a.get("href"):
				line = first_url.a.get("href")
				line_area_url = "https://www.skwf.net" + line
				html = urllib.request.urlopen(line_area_url)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				line_ = soup.find("section", class_="routeSelectArea")
				line_2 = line_.find_all("li")

				for result in line_2:
					if result.a in result:
						line_url2 = result.a.get("href")
						line_url3 = "https://www.skwf.net" + line_url2
						html2 = urllib.request.urlopen(line_url3)
						soup2 = BeautifulSoup(html2, "html.parser")
						station = soup2.find("div", class_="staListBox checkAllWrap_01")
						station2 = station.find_all("li")
						for station_result in station2:
							if station_result.a in station_result:
								station_name = station_result.text.strip()
								station_url = station_result.a.get("href")
								station_url_result = "https://www.skwf.net" + station_url
								list2 = []
								list2.append(Prefecture)
								list2.append(station_name)
								list2.append(station_url_result)
								station_list.append(list2)
				#リスト化
				for result in line_2:
					if result.a in result:
						city = result.span.text
						line_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.skwf.net" + line_url2)
						line_list.append(list1)

			elif str("area") in first_url.a.get("href"):
				area = first_url.a.get("href")
				line_area_url = "https://www.skwf.net" + area
				html = urllib.request.urlopen(line_area_url)
				soup = BeautifulSoup(html, "html.parser")
				Prefecture_search = soup.find("li", class_="current")
				Prefecture = Prefecture_search.text.strip()
				area_ = soup.find("section", class_="routeSelectArea")
				area_2 = area_.find_all("li")

				#リスト化
				for result in area_2:
					if result.a in result:
						city = result.span.text
						area_url2 = result.a.get("href")
						list1 = []
						list1.append(Prefecture)
						list1.append(city)
						list1.append("https://www.skwf.net" + area_url2)
						area_list.append(list1)
	print (line_list)
	print (area_list)
	print (station_list)						
	df_line = pd.DataFrame(line_list)
	df_area = pd.DataFrame(area_list)
	df_station = pd.DataFrame(station_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		df_line.to_excel(ew, sheet_name='沿線', header=False, index=False)
		df_area.to_excel(ew, sheet_name='市町村', header=False, index=False)
		df_station.to_excel(ew, sheet_name='駅', header=False, index=False)


#一覧情報取得取得
def list_whole():
	soup = BeautifulSoup(hokkaido_html, 'html.parser')
	target = soup.find("div", class_="areaInner")
	target2 = target.find_all("li")
	global line
	line = target2[0].a.get("href")
	global area
	area = target2[1].a.get("href")

#沿線_エリア情報取得
def line_area_get(target_url):
	line_area_url = "https://www.mast-net.jp" + target_url
	html = urllib.request.urlopen(line_area_url)
	soup = BeautifulSoup(html, "html.parser")
	Prefecture_search = soup.find("li", class_="current")
	Prefecture = Prefecture_search.text.strip()
	line_area = soup.find("section", class_="routeSelectArea")
	line_area2 = line_area.find_all("li")

	#リスト化
	line_area_list = []
	for result in line_area2:
		if result.a in result:
			city = result.span.text
			line_area_url2 = result.a.get("href")
			list1 = []
			list1.append(Prefecture)
			list1.append(city)
			list1.append("https://www.mast-net.jp" + line_area_url2)
			line_area_list.append(list1)
	print (line_area_list)
	df_line = pd.DataFrame(line_area_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		if target_url == area:
			df_line.to_excel(ew, sheet_name='市町村', header=False, index=False)
		elif target_url == line:
			df_line.to_excel(ew, sheet_name='路線', header=False, index=False)
#駅情報取得
def station_get():
	line_url = "https://www.mast-net.jp/hokkaido/route/"
	html = urllib.request.urlopen(line_url)
	soup = BeautifulSoup(html, "html.parser")
	Prefecture_search = soup.find("li", class_="current")
	Prefecture = Prefecture_search.text.strip()
	line = soup.find("section", class_="routeSelectArea")
	line2 = line.find_all("li")

	station_list = []
	for result in line2:
		if result.a in result:
			line_url2 = result.a.get("href")
			line_url3 = "https://www.mast-net.jp" + line_url2
			html2 = urllib.request.urlopen(line_url3)
			soup2 = BeautifulSoup(html2, "html.parser")
			station = soup2.find("div", class_="staListBox checkAllWrap_01")
			station2 = station.find_all("li")
			for station_result in station2:
				if station_result.a in station_result:
					station_name = station_result.text.strip()
					station_url = station_result.a.get("href")
					station_url_result = "https://www.mast-net.jp" + station_url
					list2 = []
					list2.append(Prefecture)
					list2.append(station_name)
					list2.append(station_url_result)
					station_list.append(list2)
	print (station_list) 
	df_station = pd.DataFrame(station_list)
	with pd.ExcelWriter("test.xlsx", engine="openpyxl", mode="a") as ew:
		df_station.to_excel(ew, sheet_name='駅', header=False, index=False)

if __name__ == "__main__":
	list_whole()
	line_area_get(area)
	line_area_get(line)
	station_get()
	tohoku_kyusyu(tohoku_html)
	syuto(syuto_html)
	chubu(chubu_html)
	kansai_chugoku(kansai_html)
	kansai_chugoku(chugoku_html)
	tohoku_kyusyu(kyusyu_html)
	

