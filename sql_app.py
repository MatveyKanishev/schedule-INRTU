import parsing as prs
import sqlite3

def create():
	connection = sqlite3.connect('INTU_database.db')
	cursor = connection.cursor()
	cursor.execute('''
	CREATE TABLE IF NOT EXISTS INTU (
	id TEXT PRIMARY KEY,
	clas TEXT NOT NULL,
	institute TEXT NOT NULL,
	training TEXT NOT NULL,
	year TEXT NOT NULL,
	day TEXT NOT NULL,
	pairs INTEGER
	)
	''')
	connection.commit()
	connection.close()

def add(id, group, institute, training, year, day, pairs):
	connection = sqlite3.connect('INTU_database.db')
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM INTU WHERE id == ?', (id,))
	results = cursor.fetchall()
	if not results:
		cursor.execute('INSERT INTO INTU (id, clas, institute, training, year, day, pairs) VALUES (?, ?, ?, ?, ?, ?, ?)', (id, group, institute, training, year, day, pairs))
	else:
		set_clause = ', '.join([f"{key} = ?" for key in ['clas', 'institute', 'training', 'year', 'day', 'pairs']])
		query = f"UPDATE INTU SET {set_clause} WHERE id = ?"
		params = [group, institute, training, year, day, pairs] + [id]
		
		cursor.execute(query, params)
	connection.commit()
	connection.close()





def get_filtered_data(group=None, institute=None, year=None, education_level=None):
	conn = sqlite3.connect('INTU_database.db')
	cursor = conn.cursor()
	
	query = 'SELECT day, pairs FROM INTU WHERE 1=1'
	params = []

	def handle_list_filter(column_name, filter_list):
		placeholders = ', '.join('?' for _ in filter_list)
		return f' AND {column_name} IN ({placeholders})', filter_list
	

	if group:
		filter_query, filter_params = handle_list_filter('clas', group) if isinstance(group, list) else (
		f' AND clas = ?', [group])
		query += filter_query
		params.extend(filter_params)
	
	if institute:
		filter_query, filter_params = handle_list_filter('institute', institute) if isinstance(institute, list) else (
		f' AND institute = ?', [institute])
		query += filter_query
		params.extend(filter_params)
	
	if year:
		filter_query, filter_params = handle_list_filter('year', year) if isinstance(year, list) else (
		f' AND year = ?', [year])
		query += filter_query
		params.extend(filter_params)
	
	if education_level:
		filter_query, filter_params = handle_list_filter('training', education_level) if isinstance(education_level,                                                                                           list) else (
		f' AND training = ?', [education_level])
		query += filter_query
		params.extend(filter_params)
	

	cursor.execute(query, params)
	

	results = cursor.fetchall()
	
	conn.close()
	
	return count(results)


def count(results):
	week = {
		"понедельник": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
		"вторник": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
		"среда": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
		"четверг": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
		"пятница": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
		"суббота": [-1, 0, 0, 0, 0, 0, 0, 0, 0]
	}
	for i in results:
		num = i[1]
		while num:
			if num == -1:
				continue
			week[i[0]][num % 10] += 1
			num //= 10
	return week

def updata(url):
	for link in prs.instityte(url):
		# print(*link, url + str(link['href']))
		grup = prs.year(url + str(link['href']))
		# print(grup)
		for i in grup.keys():
			for j in range(len(grup[i])):
				res_url = url + str(grup[i][j][0]) + '&date=2024-12-3'
				# print(grup[i][j][1], end="    ")
				even_week = prs.shods(res_url)
				prs.week(res_url, even_week, grup[i][j][1], str(*link), i)
	
		# print('\n_______________________________________________________________________________________________________')

def mini(week):
	mini = 9999
	for i in week.items():
		for j in range(1, len(i[1])):
			mini = min(i[1][j], mini)
	return mini
def maxi(week):
	maxi = -1
	for i in week.items():
		for j in range(1, len(i[1])):
			maxi = max(i[1][j], maxi)
	return maxi