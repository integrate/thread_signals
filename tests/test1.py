import time
from thread_signals import get_func_patcher, LateStartThread, get_thread_broker, interface_patcher



class interface():

    @staticmethod
    def hahaha():
        print('Real hahaha')
        # a=3/0

    @staticmethod
    def hohoho(t1, t2, t3):
        print('Real hohoho', t1, t2, t3)




def run_in_other_thread():
    i.hahaha()
    i.hohoho(1, t3=4, t2=7)

    broker = get_thread_broker()
    while True:
        broker.run_all_tasks()
        time.sleep(1 / 10)

t = LateStartThread(target=run_in_other_thread, name="Other thread")
i = interface_patcher(interface, t.ident, None)
t.start()

i.hahaha()
i.hohoho(t1=[1, True, "sdfsdf", 4], t3=(1, 2, 3), t2={'sdf':2})
