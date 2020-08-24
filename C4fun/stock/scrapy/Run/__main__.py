import threading
import stock_daily
import stock_After
import stock_t86


def stock_1():
    stock_daily.main()

def stock_2():
    stock_After.main()

def stock_3():
    stock_t86.main()

t1 = threading.Thread(target = stock_2)
t2 = threading.Thread(target = stock_3)

t1.start()
t2.start()
stock_1()