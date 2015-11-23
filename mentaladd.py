from datetime import datetime
import random
import mysql.connector

while True:
    no_of_questions = raw_input("No. of questions: ")
    if no_of_questions.isdigit() and (int(no_of_questions) >= 1 and int(no_of_questions) <= 1000):
        no_of_questions = int(no_of_questions)
        break
    else:
        print "Please enter a valid number between 1 and 1000"

while True:
    test_type = raw_input("Test Type: Enter 1 for Addition, 2 for Subtraction, 3 for Multiplication: ")
    if test_type.isdigit() and (int(test_type) >= 1 and int(test_type) <= 3):
        test_type = int(test_type)
        break
    else:
        print "Please enter 1 or 2 or 3"

# Constants for Test Types
TypeAdd = 1
TypeSubtract = 2
TypeMultiply = 3

while True:
    low_x = raw_input("Range Low (X): ")
    if low_x.isdigit() and (int(low_x) >= 1 and int(low_x) <= 1000):
        low_x = int(low_x)
        break
    else:
        print "Please enter a valid number between 1 and 1000"

while True:
    high_x = raw_input("Range High (X): ")
    if high_x.isdigit() and (int(high_x) >= 1 and int(high_x) <= 1000):
        high_x = int(high_x)
        break
    else:
        print "Please enter a valid number between 1 and 1000"

while True:
    low_y = raw_input("Range Low (Y): ")
    if low_y.isdigit() and (int(low_y) >= 1 and int(low_y) <= 1000):
        low_y = int(low_y)
        break
    else:
        print "Please enter a valid number between 1 and 1000"

while True:
    high_y = raw_input("Range High (Y): ")
    if high_y.isdigit() and (int(high_y) >= 1 and int(high_y) <= 1000):
        high_y = int(high_y)
        break
    else:
        print "Please enter a valid number between 1 and 1000"        

#TODO: Add exception handling in case it can't connect
conn = mysql.connector.connect(user='root', password='Dont4get', host='localhost',database='sakila')
cur = conn.cursor()

if test_type == TypeAdd:
    test_desc = 'Addition Test'
elif test_type == TypeSubtract:
    test_desc = 'Subtraction Test'
elif test_type == TypeMultiply:
    test_desc = 'Multiply Test'
else:
    pass #TODO: Throw error here for Invalid Test Type

#test_desc = test_desc + ", testing run"

#TODO: Add exception handling in case it can't insert
cur.execute("insert into test(dated, description, low, high, no_of_questions) values ('%s','%s',%s,%s,%s)"
            % (datetime.now(), test_desc, low_x,high_x,no_of_questions))

test_id = cur.lastrowid
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

for n in range(0,no_of_questions):
	x = random.randrange(low_x,high_x)
	y = random.randrange(low_y,high_y)
	start_timer = datetime.now()
	ans = int(raw_input(question_text() % (n+1, x, y)))
	stop_timer = datetime.now()
	duration = stop_timer - start_timer
	test.append(Question(x,y,ans,duration.seconds))
	result = 1 if calculate(x,y) == ans else 0
	sql = "insert into test_detail values (%s,%s,%s,%s,%s,%s)" % (test_id,x,y,ans,result,duration.seconds)
	cur.execute(sql)

conn.commit()

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

for q in test:
        if q.result == 0:
            print (result_text() + " = %s, not %s (Wrong) in %s seconds") % (q.x, q.y, calculate(q.x, q.y), q.ans, q.time)
            no_of_misses += 1

print ("You got %s/%s" % (no_of_questions - no_of_misses, no_of_questions))
