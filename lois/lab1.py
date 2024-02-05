def correction_check(line):
    operations = ['/\\','\\/','->','~']
    simplified = unify_letters(line)
    if simplified == None:
        return False
    simplified = no_negotions(simplified)
    for i in range(len(operations)):
        simplified = simplified.replace(operations[i], '/\\')
    while find_binary(simplified, '/\\'):
        simplified = simplified.replace('(A/\\A)', 'A')
    return simplified == 'A'

def no_negotions(line):
    i = 0
    while i < len(line):
        if line[i] == '(':
            if line[i+1:i+4] == '!A)':
                line = line[:i] + 'A' + line[i+4:]
        i += 1
    return line

def simplify(line, op):
    while find_binary(line, op):
        line = line.replace('(A' + op + 'A)', 'A')
    return line

def find_binary(line, op):
    for i in range(0, len(line)-5):
        if line[i:i+6] == '(A' + op + 'A)':
            return True
    return False

def unify_letters(line):
    i = 0
    while i < len(line)-1:
        if line[i].isalpha and line[i].isupper():
            line = line[:i] + 'A' + line[i+1:]
        i += 1
    return line

while True:
    line = input('Введите формулу: ')
    line = line.replace(' ', '')
    if correction_check(line):
        line = unify_letters(line)
        line = no_negotions(line)
        line = simplify(line, '\\/')
        line = simplify(line, '/\\')
        if line == 'A':
            print('является КНФ')
        else:
            print('не является КНФ')
    else:
        print('формула введена неверно')
