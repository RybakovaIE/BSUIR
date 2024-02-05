#Лабораторная работа 1
#Вариант: 21
#Выполнили: Рыбакова И.Е., Кондратьева И.Д., гр. 121701

def print_fuzzy_set(fuzzy_set):
    print('{', end = '')
    for i in range(len(fuzzy_set)):
        print('<', fuzzy_set[i][0], ',', fuzzy_set[i][1], '>', end = '')
        if i != len(fuzzy_set)-1:
            print(', ', end = '')
    print('}', end = '')

def print_fuzzy_matrix(matrix):
    rows_num = len(matrix)
    cols_num = len(matrix[0])
    print('{', end = '')
    for i in range(rows_num):
        for j in range(cols_num):
            print('<<', matrix[i][j][0][0], ',', matrix[i][j][0][1], '>,', matrix[i][j][1], '>', end = '')
            if j != cols_num-1:
                print(', ', end = '')
        if i != rows_num-1: print('\n', end = '')
    print('}')

def print_simple_matrix(matrix):
    rows_num = len(matrix)
    cols_num = len(matrix[0])
    for i in range(rows_num):
        print('|', end = ' ')
        for j in range(cols_num):
            number = matrix[i][j][1]
            if number == 1: number = '1.0'
            print(number, end = ' ')
        print('|')

def print_fuzzy_conjunction(rows_num, cols_num, matrix, set):
    middle = int(rows_num//2)
    for i in range(rows_num):
        print('|', set[i][1], end = ' | ')
        if i == middle-1: print('~ ', end = '')
        elif i == middle: print(chr(8743), end = ' ')
        else: print('  ', end = '')
        print('| ', end = '')
        for j in range(cols_num):
            number = rules[rule_name][i][j][1]
            if number == 1: number = '1.0'
            print(number, end = ' ')
        print('|', end = '')
        if i == middle: print(' = ', end = '')
        else: print('  ', end = ' ')
        print('|', end = ' ')
        for j in range(cols_num):
            number = matrix[i][j]
            if number == 1: number = '1.0'
            print(number, end = ' ')
        print('|')

def read_rule(line, sets):
    first = line[0]
    second = line[-1]
    if not(first.isalpha()) or not(second.isalpha()) or line[1:3] != '~>':
        return 'Синтаксическая ошибка. Невозможно считать правило '
    if first not in sets.keys() or second not in sets.keys():
        return 'Несуществующее множество в правиле '
    else:
        return fuzzy_implication(sets[first], sets[second])

def read_set(line):
    fuzzy_set = []
    if line[0] != '{'or line[len(line)-1] != '}':
        return "error"
    i = 1
    while line[i] != '}':
        if line[i] == '<':
            if line[i:].find('>') == -1:
                return "error"
            else :
                fuzzy_set.append(read_element(line[i:line[i:].find('>')+1+i]))
                if fuzzy_set[-1] == 'error': return 'error'
            i = line[i:].find('>') + 1 + i
        else:
            if line[i] != ',':
                return "error"
            else: i+=1
    return fuzzy_set

def read_element(line):
    if line[0] != '<'or line[len(line)-1] != '>':
        return "error"
    if line[1:].find(',') == -1:
        return "error"
    else :
        argument = line[1:line.find(',')]
    membership_value = line[line.find(',')+1 : len(line)-1]
    try:
        membership_value = float(membership_value)
    except ValueError:
        return 'error'
    return (argument, membership_value)

def godel_implication(a, b):
    if a <= b: return 1
    else: return b

def fuzzy_implication(set1, set2):
    matrix = []
    for element1 in set1:
        matrix.append([((element1[0], element2[0]), godel_implication(element1[1], element2[1])) for element2 in set2])
    return matrix

def fuzzy_conjunction(set, matrix):
    return [[min(set[i][1], matrix[i][j][1]) for j in range(len(matrix[0]))] for i in range(len(set))]

def matrix_to_set(matrix):
    return [max(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))]

def find_identical(new_set, sets):
    for set in sets:
        if new_set == set: return True
    return False

def solve(set, rule_name):
    rows_num = len(rules[rule_name])
    cols_num = len(rules[rule_name][0])
    print('\n\nпосылка: ', end = '')
    print_fuzzy_set(set)
    print('\nправило: ', rule_name)
    print('\n', end = '')
    matrix = fuzzy_conjunction(set, rules[rule_name])
    print_fuzzy_conjunction(rows_num, cols_num, matrix, set)

    print('\nИз данной матрицы получаем ответ: ', end = '')
    membership_values = matrix_to_set(matrix)
    result_set = [(rules[rule_name][0][0][0][1][0]+str(i), membership_values[i]) for i in range(len(membership_values))]
    print_fuzzy_set(result_set)

    if find_identical(result_set, all_sets):
        print('\nТакой предикат уже есть')
    else:
        new_sets.append(result_set)
        all_sets.append(result_set)



file = open('D://5_sem//lois//task.txt')

unused_sets = dict()
all_sets = []
rules = dict()
errors_count = 0
for line in file.readlines():
    if line.find('~>') == -1:
        left = line[:line.find('{')].replace(' ', '')
        if len(left) != 2 or (not(left[0].isalpha()) or left[-1] != '='):
            print("Синтаксическая ошибка. Невозможно считать множество.")
        else:
            name = left[0]
            line = line[line.find('{'):len(line)].replace(' ', '').strip()
            new_set = read_set(line)
            if new_set == 'error': print("Синтаксическая ошибка. Невозможно считать множество ", name)
            else: 
                unused_sets[name] = new_set
                all_sets.append(new_set)
    else:
        rule = read_rule(line.strip(), unused_sets)
        if isinstance(rule, str):
            print(rule, line)
        else:
            rules[line.strip()] = rule
            print('\n', line)
            print_fuzzy_matrix(rule)
            print('\nили\n')
            print_simple_matrix(rule)
unused_sets = list(unused_sets.values())

new_sets = []
go_on = True
while go_on:
    sets_num = len(all_sets)
    for set in unused_sets:
        for rule_name in rules.keys():
            set_char = set[0][0][0]
            rule_char = rules[rule_name][0][0][0][0][0]
            if len(set) == len(rules[rule_name]) and set_char == rule_char:
                solve(set, rule_name)
                input()
    unused_sets = new_sets
    new_sets = []
    if sets_num == len(all_sets):
        print('Новые посылки больше не появляются. Завершение процесса')
        go_on = False
        

