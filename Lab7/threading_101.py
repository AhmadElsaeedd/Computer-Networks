# This library must be imported
import threading

def foo(mesg: str, num: int):
    print('This fuction is ran in another thread')
    print('The passed arguments are', mesg, num)


# this is how you create a thread
# the thread will execute the 'target' function
# the arugments passed to this function are specified as a list in 'args'
t = threading.Thread(target=foo, args=['some string', 14])
t.start()

print('two threads are being executed at this time')