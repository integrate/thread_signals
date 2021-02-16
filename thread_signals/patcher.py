import threading
from thread_signals.task_broker import Task_broker


def get_func_patcher(executor_thread_id, timeout):
    def func_patcher(orig_func):
        return simple_func_patcher(orig_func, executor_thread_id, timeout)

    return func_patcher


def simple_func_patcher(orig_func, executor_thread_id, timeout):
    def patched_func(*args, **kwargs):
        if threading.get_ident() == executor_thread_id:
            return orig_func(*args, **kwargs)

        # print("Task added for call " + orig_func.__name__ + "(" + ", ".join(
        #     [str(i) for i in args] + [str(name) + "=" + str(value) for (name, value) in kwargs.items()]) + ")")

        broker = Task_broker.get_task_broker(executor_thread_id)
        res = broker.run_func_as_task(orig_func, args, kwargs, timeout)
        if type(res) is bool:
            raise Exception("Command {fnc_name} not run in {timeout} seconds".format(fnc_name=orig_func.__name__,
                                                                                     timeout=str(timeout)))

        if res[0] is False:
            raise res[2]
        else:
            return res[1]


    return patched_func
