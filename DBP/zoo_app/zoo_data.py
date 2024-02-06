import psycopg2

try:
    conn = psycopg2.connect('postgresql://postgres:12345@localhost:5432/zoo')
except:
    print(':(')

cursor = conn.cursor()
last = {'animals': 0, 'diets': 0, 'birds': 0, 'reptiles': 0, 'workers': 0}
long_queries = {'birds': 'select birds.n, species, name, wintering_place, departure, arrival from birds, animals where birds.n = animals.n',
                'reptiles': 'select reptiles.n, species, name, temperature, hibernation_days from reptiles, animals where reptiles.n = animals.n',
                'couples': 'select f.n f_n, f.prof f_prof, f.name f_name, s.n s_n, s.prof s_prof, s.name s_name from workers f, workers s where f.n = s.marriage and f.n > s.n'}
dates = {'animals': [3], 'birds': [4, 5], 'reptiles': [], 'workers': [3], 'environments': [], 'diets': [], 'couples': []}

def get_table(table_name):
    if table_name == 'environments': key = 'name'
    else: key = 'N'
    if table_name in long_queries.keys():
        query = long_queries[table_name]
    else:
        query = 'SELECT * FROM ' + table_name + ' ORDER BY ' + key
    cursor.execute(query)
    rows = cursor.fetchall()
    for i in range(len(rows)):
        rows[i] = list(rows[i])
        for j in dates[table_name]:
            rows[i][j] = normal_date(rows[i][j], table_name)
        rows[i] = tuple(rows[i])
    if table_name == 'couples': 
        for i in range(len(rows)):
            rows[i] = list(rows[i])
            rows[i].insert(3, '')
            rows[i] = tuple(rows[i])
    global last
    if len(rows) > 0 and table_name != 'couples': last[table_name] = rows[-1][0]
    return rows

def normal_date(date, table_name):
    date = str(date)
    if table_name == 'birds': date = f"{date[8:10]}.{date[5:7]}"
    else: date = f"{date[8:10]}.{date[5:7]}.{date[:4]}"
    return date

def add_year(date):
    if date =='':
        return 'null'
    return date + '.2000'

def get_last(table_name):
    global last
    last[table_name]+=1
    return last[table_name]

def add_row(table_name, info):
    global last
    if table_name != 'environments': last[table_name]+=1
    query = 'INSERT INTO ' + table_name + ' VALUES ('+ ', '.join(info) + ')'
    cursor.execute(query)
    conn.commit()

def get_table_query(table_name):
    return long_queries[table_name]

def delete_rows(table_name, column_name, delete_list):
    query = 'DELETE FROM ' + table_name + ' WHERE ' + column_name + ' IN (' + ', '.join(delete_list) + ')'
    cursor.execute(query)
    conn.commit() 

def alter_row(table_name, column_name, checked, new_info):
    query = 'UPDATE ' + table_name + ' SET ' + new_info + ' WHERE ' + column_name + ' = ' + checked
    cursor.execute(query)
    conn.commit() 

def get_checked(table_name, column_name, key):
    if table_name in long_queries.keys():
        table = f"({long_queries[table_name]})"
    else: table = table_name
    query = 'SELECT * FROM ' + table + ' WHERE ' + column_name + ' = ' + str(key)
    cursor.execute(query)
    rows = cursor.fetchall()
    for i in range(len(rows)):
        rows[i] = list(rows[i])
        for j in dates[table_name]:
            rows[i][j] = normal_date(rows[i][j], table_name)
        rows[i] = tuple(rows[i])
    return rows[0]

def get_checked_couple(key):
    query = f"select f.n, s.n from workers f, workers s where f.n = s.marriage and f.n > s.n and f.n = {key};"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows[0]

def search(table_name, searched, columns):
    if table_name in long_queries.keys(): table = f"({long_queries[table_name]})"
    else: table = table_name
    query = 'SELECT * FROM ' + table + ' WHERE ' + columns[0] + ' = ' + searched[0]
    if len(searched) == 1 and not(searched[0].isdigit()):
        query += ' OR '+ columns[-1] + ' = ' + searched[0]
    elif len(searched) == 2:
        query += ' AND '+ columns[-1] + ' = ' + searched[-1]
        query += ' OR ('+ columns[-1] + ' = ' + searched[0] + ' AND '+ columns[0] + ' = ' + searched[1] + ')'
    cursor.execute(query)
    found = cursor.fetchall()
    for i in range(len(found)):
        found[i] = list(found[i])
        for j in dates[table_name]:
            found[i][j] = normal_date(found[i][j], table)
        found[i] = tuple(found[i])
    if table == 'couples': 
        for i in range(len(found)):
            found[i] = list(found[i])
            found[i].insert(3, '')
            found[i] = tuple(found[i])
    return(found)

def exists(table_name, column, key):
    query = f"SELECT COUNT(*) FROM {table_name}  WHERE {column} = {key}"
    cursor.execute(query)
    existense = cursor.fetchall()
    return existense[0][0]

def get_indwellers(environment_names):
    query = f"SELECT n FROM animals WHERE environment in ('" + "', '".join(environment_names) + "')"
    cursor.execute(query)
    existense = cursor.fetchall()
    return [element[0] for element in existense]

def get_eaters(diet_indexes):
    query = f"SELECT n FROM animals WHERE diet in ('" + "', '".join(diet_indexes) + "')"
    cursor.execute(query)
    existense = cursor.fetchall()
    return [element[0] for element in existense]

def get_special_animals(serial_numbers, type):
    query = f"SELECT n FROM {type} WHERE n in ('" + "', '".join(serial_numbers) + "')"
    cursor.execute(query)
    existense = cursor.fetchall()
    return [element[0] for element in existense]

def just_get(query):
    cursor.execute(query)
    content = cursor.fetchall()
    return content

def add_couple(n_first, n_second):
    statuses = []
    cursor.execute(f'SELECT FAMILY_STATUS FROM workers WHERE N = {n_first}')
    statuses.append(cursor.fetchall()[0][0])
    cursor.execute(f'SELECT FAMILY_STATUS FROM workers WHERE N = {n_second}')
    statuses.append(cursor.fetchall()[0][0])
    for i in range(len(statuses)):
        statuses[i] = statuses[i].split(',')
        statuses[i][0] = 'женат(a)'
        statuses[i] = ', '.join(statuses[i])
    cursor.execute(f"UPDATE workers SET family_status = '{statuses[0]}', marriage = {n_second} WHERE N = {n_first}")
    conn.commit()
    cursor.execute(f"UPDATE workers SET family_status = '{statuses[1]}', marriage = {n_first} WHERE N = {n_second}")
    conn.commit()

def divorce_couple(n_first, n_second):
    statuses = []
    cursor.execute(f'SELECT FAMILY_STATUS FROM workers WHERE N = {n_first}')
    statuses.append(cursor.fetchall()[0][0])
    cursor.execute(f'SELECT FAMILY_STATUS FROM workers WHERE N = {n_second}')
    statuses.append(cursor.fetchall()[0][0])
    for i in range(len(statuses)):
        statuses[i] = statuses[i].split(',')
        statuses[i][0] = 'разведен(a)'
        statuses[i] = ', '.join(statuses[i])
    cursor.execute(f"UPDATE workers SET family_status = '{statuses[0]}', marriage = null WHERE N = {n_first}")
    conn.commit()
    cursor.execute(f"UPDATE workers SET family_status = '{statuses[1]}', marriage = null WHERE N = {n_second}")
    conn.commit()

