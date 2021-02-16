import threading

from thread_signals.task import TaskFuncRun

class Task_broker():
    def __init__(self, executor_thread_id):
        self._executor_thread_id = executor_thread_id

        self._task_list = []
        self._task_list_lock = threading.RLock()

    def _add_task_to_queue_and_wait(self, task, timeout):
        #add task to list
        with self._task_list_lock:
            self._task_list.append(task)

        #wait for execution
        res = task.wait(timeout)
        if not res: return False

        return (task.is_successful(), task.get_result(), task.get_exception())

    def run_func_as_task(self, func, args, kwargs, timeout):
        t = TaskFuncRun(self._executor_thread_id, func, args, kwargs)
        return self._add_task_to_queue_and_wait(t, timeout)

    def _get_earliest_task(self):
        with self._task_list_lock:
            if len(self._task_list)>0:
                t = self._task_list[0]
                del self._task_list[0]
            else:
                t = None

        return t

    def run_all_tasks(self):
        if threading.get_ident() != self._executor_thread_id:
            raise Exception('Tasks could only be run from execution thread!')

        t = self._get_earliest_task()
        while t is not None:
            t.run_task()
            t = self._get_earliest_task()


    #one broker per thread
    _broker_list_lock = threading.RLock()
    _broker_list = {} #thread_id: broker
    @classmethod
    def get_task_broker(cls, executor_thread_id):
        with cls._broker_list_lock:
            if executor_thread_id in cls._broker_list:
                res= cls._broker_list[executor_thread_id]
            else:
                res = cls(executor_thread_id)
                cls._broker_list[executor_thread_id] = res


        return res

