# -*- coding: utf-8 -*-
import itertools

from abc import ABCMeta, abstractmethod
from threading import Thread


class MultiThreadingPluginBase(metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def execute(workers):
        workers, workers_cp = itertools.tee(workers, 2)
        threads = (Thread(target=w.map) for w in workers_cp)
        threads, threads_cp = itertools.tee(threads)
        for thread in threads: thread.start()
        for thread in threads_cp: thread.join()

        results = [worker.result for worker in workers]
        return results

    def custom_map(self, worker_class, input_class, config):
        workers = worker_class.create_workers(input_class, config)
        return self.execute(workers)
