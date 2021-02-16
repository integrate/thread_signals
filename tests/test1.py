import threading, time
from thread_signals.task_broker import Task_broker
from thread_signals.late_start_thread import LateStartThread
from thread_signals import get_func_patcher



def get_interface(executor_thread):

    class interface():

        @staticmethod
        @get_func_patcher(executor_thread, None)
        def hahaha():
            print('Real hahaha')

        @staticmethod
        @get_func_patcher(executor_thread, None)
        def hohoho(t1, t2, t3):
            print('Real hohoho', t1, t2, t3)

    return interface



def run_in_other_thread():
    i.hahaha()
    i.hohoho(1, t3=4, t2=7)

    broker = Task_broker.get_task_broker(threading.get_ident())
    while True:
        broker.run_all_tasks()
        time.sleep(1 / 10)

t = LateStartThread(target=run_in_other_thread, name="Other thread")
executor_thread = t.ident
i = get_interface(executor_thread)
t.start()

i.hahaha()
i.hohoho(t1=[1, True, "sdfsdf", 4], t3=(1, 2, 3), t2={'sdf':2})

t.join(0)
