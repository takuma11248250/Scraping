import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 

#-----------webdriver認証---------------------
options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
#---------------------------------------------
#-----------スクレイピング対象先サイト設定-----------
target_url = 'https://jp.indeed.com/advanced_search'
driver.get(target_url)
time.sleep(5)
#---------------------------------------------
#-----------日付設定と配列作成--------------------
today = datetime.today()
month = datetime.strftime(today, '%Y-%m')
month = month + '-01'
result_jobcnt_list = []
#---------------------------------------------
#-----------スプレッド認証情報設定-----------------
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/takuma_kono/key/gcp/causal-temple-316609-f8cdee53d360.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = '1r4dXDiTbiSvbkoGmPSb6lyINtfJf-83gW7WhTE9D-Fs'
wb = gc.open_by_key(SPREADSHEET_KEY)
ws = wb.worksheet('月別')
#---------------------------------------------

#-----------セグメント検索処理--------------------
def search_box(job_name):
	search_box_job = driver.find_element_by_xpath('/html/body/div[2]/form/fieldset[1]/div[5]/div[2]/input')
	search_box_job.send_keys(job_name)
	search_box_employ = driver.find_element_by_xpath('/html/body/div[2]/form/fieldset[1]/div[7]/div[2]/select')
	select_element = Select(search_box_employ)
	select_element.select_by_value('fulltime')
	search_btn = driver.find_element_by_xpath('/html/body/div[2]/form/button')
	search_btn.click()
	time.sleep(5)
	result_jobcnt = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[3]/div[4]/div[2]/div/div[1]').text
	cut_number = result_jobcnt.find('件')
	result_jobcnt = result_jobcnt[7:cut_number-1]
	print (int(result_jobcnt))
	jobcnt_list = []
	jobcnt_list.extend([month, job_name, int(result_jobcnt)])
	result_jobcnt_list.append(jobcnt_list)
	job_name = ""
	driver.get(target_url)
#---------------------------------------------	

search_box('データアナリスト')
search_box('データエンジニア')
search_box('データサイエンティスト')
driver.quit()
for result_value in result_jobcnt_list:
	ws.append_row(result_value)
