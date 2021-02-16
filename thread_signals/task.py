import sys, threading, json

from tblib import pickling_support
pickling_support.install()
import pickle

class Task(threading.Event):
    def __init__(self, executor_thread_id, not_serialized_data, serialized_data):
        threading.Event.__init__(self)

        self._executor_thread_id = executor_thread_id

        self._not_serialized_data = not_serialized_data
        self._serialized_data = json.dumps(serialized_data, indent=True)

        self._result_success = None
        self._result_data = None
        self._excdata = None

    def run_task(self):
        if self.is_set():
            raise Exception('Task could only be run once!')

        if self._executor_thread_id != threading.get_ident():
            raise Exception('Task could only be run from executor thread!')

        try:
            serialized_data = json.loads(self._serialized_data)
            res = self._do_task(self._not_serialized_data, serialized_data)

        except Exception as e:
            self._set_exception(e)
        else:
            self._set_result(res)

        self.set()

    def _do_task(self, not_serialized_data, serialized_data):
        raise Exception('Method must be overriden!')

    def _set_exception(self, e):
        self._result_success = False
        self._excdata = pickle.dumps(sys.exc_info())

    def _set_result(self, res):
        self._result_success = True
        self._result_data = json.dumps(res)

    def is_successful(self):
        if not self.is_set():
            raise Exception('Task not run yet!')

        return self._result_success

    def get_exception(self):
        if not self.is_set():
            raise Exception('Task not run yet!')

        if self._excdata is None:
            return None

        return pickle.loads(self._excdata)

    def get_result(self):
        if not self.is_set():
            raise Exception('Task not run yet!')

        if self._result_data is None:
            return None

        return json.loads(self._result_data)



class TaskFuncRun(Task):
    def __init__(self, executor_thread_id, func, args, kwargs):
        Task.__init__(self, executor_thread_id, func, [args, kwargs])

    def _do_task(self, not_serialized_data, serialized_data):
        func = not_serialized_data
        args = serialized_data[0]
        kwargs = serialized_data[1]
        return func(*args, **kwargs)

