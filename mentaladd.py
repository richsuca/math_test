from datetime import datetime
import random
import mysql.connector

class Question:
	def __init__(self,x,y,ans,time):
		self.x = x
		self.y = y
		self.ans = ans
		self.result = 1 if x+y == ans else 0
		self.time = time

no_of_questions = int(raw_input("No. of questions: "))
l = int(raw_input("Range Low: "))
h = int(raw_input("Range High: "))

conn = mysql.connector.connect(user='root', password='Dont4get', host='localhost',database='sakila')
cur = conn.cursor()
cur.execute("insert into test(dated, description, low, high, no_of_questions) values ('%s','%s',%s,%s,%s)" % (datetime.now(),'Addition', l,h,no_of_questions))
test_id = cur.lastrowid
test = []

for n in range(0,no_of_questions):
	x = random.randrange(l,h)
	y = random.randrange(l,h)
	start_timer = datetime.now()
	ans = int(raw_input("%s + %s ? " %(x,y)))
	stop_timer = datetime.now()
	duration = stop_timer - start_timer
	test.append(Question(x,y,ans,duration.seconds))
	result = 1 if x+y == ans else 0
	sql = "insert into test_detail values (%s,%s,%s,%s,%s,%s)" % (test_id,x,y,ans,result,duration.seconds)
	cur.execute(sql)

conn.commit()

for q in test:
        if q.result == 0:
            print "%s + %s = %s, not %s (%s) in %s seconds" % (q.x, q.y, q.x+q.y, q.ans, q.result, q.time)
        else:
            print "%s + %s = %s (%s) in %s seconds" % (q.x, q.y, q.ans, q.result, q.time)
            
