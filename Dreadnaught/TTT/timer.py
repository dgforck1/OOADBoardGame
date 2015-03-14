import time
from thread import start_new_thread, allocate_lock



a = time.clock()
num_threads = 0
thread_started = False
result = None
lock = allocate_lock()



def get_move(a):
    global num_threads, thread_started, result

    lock.acquire()
    num_threads += 1
    thread_started = True
    lock.release()

    '''if a:
    	result = get_move1(board, 0, piece)
    else:
    	result = get_move2(board, 0, piece)'''
    for x in xrange(10000000):
    	f = x * x
    	result = f

    lock.acquire()
    num_threads -= 1
    lock.release()



start = time.clock()
timer = 0
max_time = 10000
start_new_thread(get_move, (None,))



while not thread_started:
	pass
while num_threads > 0:
	timer = (time.clock() - start) * 1000

	if timer < max_time:
		time.sleep(0.1)
		continue
	else:
		print timer
		exit(1)



print 'Function Time: ', timer / 1000, 'seconds'
print 'Script Run Time', time.clock() - a, 'seconds'