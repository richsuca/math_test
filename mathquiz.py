from datetime import datetime
import random
import sqlite3
import os.path
import os

while True:
    no_of_questions = input("No. of questions: ")
    if no_of_questions.isdigit() and (int(no_of_questions) >= 1 and int(no_of_questions) <= 1000):
        no_of_questions = int(no_of_questions)
        break
    else:
        print("Please enter a valid number between 1 and 1000")

while True:
    test_type = input("Test Type: Enter 1 for Addition, 2 for Subtraction, 3 for Multiplication: ")
    if test_type.isdigit() and (int(test_type) >= 1 and int(test_type) <= 3):
        test_type = int(test_type)
        break
    else:
        print("Please enter 1 or 2 or 3")

# Constants for Test Types
TypeAdd = 1
TypeSubtract = 2
TypeMultiply = 3

while True:
    low_x = input("Range Low (X): ")
    if low_x.isdigit() and (int(low_x) >= 1 and int(low_x) <= 1000):
        low_x = int(low_x)
        break
    else:
        print("Please enter a valid number between 1 and 1000")

while True:
    high_x = input("Range High (X): ")
    if high_x.isdigit() and (int(high_x) >= 1 and int(high_x) <= 1000):
        high_x = int(high_x)
        break
    else:
        print("Please enter a valid number between 1 and 1000")

while True:
    low_y = input("Range Low (Y): ")
    if low_y.isdigit() and (int(low_y) >= 1 and int(low_y) <= 1000):
        low_y = int(low_y)
        break
    else:
        print("Please enter a valid number between 1 and 1000")

while True:
    high_y = input("Range High (Y): ")
    if high_y.isdigit() and (int(high_y) >= 1 and int(high_y) <= 1000):
        high_y = int(high_y)
        break
    else:
        print("Please enter a valid number between 1 and 1000")        

def execute_sql(sql, params=()):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(sql, params)
    conn.commit()
    conn.close()
    return c.lastrowid
    
def verify_db(db_path):
    if not os.path.exists(db_path):
        execute_sql('''create table test (
                     id, dated, description, low_x, high_x, low_y, high_y, questions)''')
        execute_sql('create table test_detail (id, x, y, ans, result, time)')

if os.name == 'posix':
    db_path = os.path.expanduser("~") + "/math-test.db"
else:
    db_path = os.path.expanduser("~") + r"\math-test.db"
    
verify_db(db_path)

if test_type == TypeAdd:
    test_desc = 'Addition Test'
elif test_type == TypeSubtract:
    test_desc = 'Subtraction Test'
elif test_type == TypeMultiply:
    test_desc = 'Multiply Test'
else:
    pass #TODO: Throw error here for Invalid Test Type

test_desc = test_desc + ", testing run"

sql = "insert into test(dated, description, low_x, high_x, low_y, high_y, questions) values (?,?,?,?,?,?,?)"
params = (datetime.now(), test_desc, low_x, high_x, low_y, high_y, no_of_questions)
test_id = execute_sql(sql, params)

# set test_id to the generated rowid
sql = "update test set id = ? where rowid = ?"
params = (test_id, test_id)
execute_sql(sql, params)

test = []

def calculate(x,y):
    if test_type == TypeAdd:
        return x + y
    elif test_type == TypeSubtract:
        return x - y
    elif test_type == TypeMultiply:
        return x * y
    else:
        return -99999999

class Question:    
    def __init__(self,x,y,ans,time):
        self.x = x
        self.y = y
        self.ans = ans
        self.result = 1 if calculate(x,y) == ans else 0
        self.time = time

def question_text():
    if test_type == TypeAdd:
        return "%s) %s + %s ? "
    elif test_type == TypeSubtract:
        return "%s) %s - %s ? "
    elif test_type == TypeMultiply:
        return "%s) %s X %s ? "
    else:
        return "Oops, something is wrong in question_text()"
        
def get_answer(n, x, y):
    while True:
        response = input(question_text() % (n, x, y))
        try:
            response_int = int(response)
            return response_int
        except ValueError:
            print("Please enter a valid number for the answer")        

question_hist = {}
            
def get_question():
    give_up_after = 5 # if the same x, y or y, x keeps repeating, give up and use it
    while True:
        x = random.randrange(low_x, high_x)
        y = random.randrange(low_y, high_y)
        #print("x:%s,y:%s" % (x,y))
        if (x, y) in question_hist or (y, x) in question_hist:
            #print("repeat")
            if (x, y) in question_hist:
                question_hist[(x, y)] += 1
                if question_hist[(x, y)] > give_up_after: 
                    #print("giving up")
                    break
            else:
                question_hist[(y, x)] += 1
                if question_hist[(y, x)] > give_up_after: 
                    break
        else:
            question_hist[(x, y)] = 1
            break
    return (x, y)
            
for n in range(0,no_of_questions):
    (x, y) = get_question()
    start_timer = datetime.now()
    ans = get_answer(n+1, x, y)
    stop_timer = datetime.now()
    duration = stop_timer - start_timer
    test.append(Question(x, y, ans, duration.seconds))
    result = 1 if calculate(x,y) == ans else 0
    sql = "insert into test_detail(id, x, y, ans, result, time) values (?,?,?,?,?,?)"
    params = (test_id, x, y, ans, result, duration.seconds)
    execute_sql(sql, params)

def result_text():
    if test_type == TypeAdd:
        return "%s + %s"
    elif test_type == TypeSubtract:
        return "%s - %s"
    elif test_type == TypeMultiply:
        return "%s X %s"
    else:
        return "Oops, something is wrong in result_text()"

no_of_misses = 0

print()
print('Your Report')

for q in test:
        if q.result == 0:
            print((result_text() + " = %s, not %s (Wrong) in %s seconds") 
                    % (q.x, q.y, calculate(q.x, q.y), q.ans, q.time))
            no_of_misses += 1

print("You got %s/%s" % (no_of_questions - no_of_misses, no_of_questions))
