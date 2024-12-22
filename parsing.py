import requests
from bs4 import BeautifulSoup
import time
import re
import sql_app

def instityte(url: str):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	links_with_subdiv = soup.find_all('a', href=lambda x: x and '?subdiv=' in x)
	links_with_subdiv.remove(links_with_subdiv[0])
	links_with_subdiv.remove(links_with_subdiv[5])
	return links_with_subdiv


def groop(url: str):
	grup = requests.get(url)
	gg = BeautifulSoup(grup.text, 'html.parser')
	links_with_grup = gg.find_all('a', href=lambda x: x and '?group=' in x)
	return links_with_grup


def year(url: str):
	response_res = requests.get(url)
	soup_res = BeautifulSoup(response_res.text, 'html.parser')
	even_week = soup_res.find(class_='kurs-list')
	pattern = r"Курс\s\d"
	# print(str(even_week).split(r"Курс\s\d"))
	stri = str(even_week).replace('\n<ul>\n<li><a', ' ')
	s = re.split(pattern, stri)
	s = s[1:]
	dikt = {}
	name = re.findall(pattern, str(even_week))
	for i in range(len(s)):
		gg = re.findall(r"[?]group=\d*", s[i])
		ll = re.findall(r"[А-Я]*.-\d+-\d+", s[i])
		dikt[name[i]] = [[gg[i], ll[i]] for i in range(len(ll))]

	return dikt

	
	
	
def shods(url: str):
	response_res = requests.get(url)
	soup_res = BeautifulSoup(response_res.text, 'html.parser')
	
	# print(url)
	
	even_week = soup_res.find(class_='full-even-week')
	return even_week


def week(res_url: str, even_week, grop: str, inst: str, year : str):
	
	if even_week:
		day_headings = even_week.find_all(class_='day-heading')

		translt = {'8:15': 1, '10:00': 2, '11:45': 3, '13:45': 4, '15:30': 5, '17:10': 6, '18:45': 7, '20:20': 8}
		for day in day_headings:
			day_text = day.get_text(strip=True)
			stri = grop + str(day_text)[:3]
			#print(stri)
			# Ищем класс "class-lines"
			class_lines = day.find_next(class_='class-lines')
			
			if class_lines:
				# Ищем все элементы с классом "class-time" внутри "class-lines"
				class_times = class_lines.find_all(class_='class-time')
				masiw = ''
				for class_time in class_times:
					class_time_text = class_time.get_text(strip=True)
					masiw += str(translt[class_time_text])
				learn = 'специалитет'
				if re.findall(r"[б]", grop):
					learn = 'бакалавриат'
				if re.findall(r"[м]", grop):
					learn = 'магистратура'
				day = day_text.split(',')[0]
				sql_app.add(stri, grop, inst, learn, year, day, int(masiw))
				# print('\n', stri, int(masiw), inst, day, learn, grop)