#
# Created by maks5507 (me@maksimeremeev.com)
#

import numpy as np
from pathlib import Path
import json
import multiprocessing
from twisted.logger import Logger, textFileLogObserver
import importlib.util

from .worker import Worker


class Launcher:
    def __init__(self, log_file):
        """
        :param log_file: path to file to write log messages to
        """
        self.log = Logger(observer=textFileLogObserver(open(log_file, 'a')))

    @staticmethod
    def __terminate_all(processes):
        """
        Terminates all dependent processes running
        """
        if isinstance(processes, list):
            for process in processes:
                process.terminate()
        else:
            for id in processes:
                for process in processes[id]:
                    process.terminate()

    def launch(self, config):
        """
        :param config: configuration file for the launcher=. See the required format in readme
        """
        processes = {}
        try:
            config = json.loads(config)

            jobs = {}
            started = set()
            for job_id in config:
                jobs[job_id] = config[job_id]
                module_name = jobs[job_id]["name"]
                class_name = ''.join([f'{prt[0].upper()}{prt[1:]}' for prt in module_name.split('_')])

                init_args = config[job_id]['init_args']
                init_args['log'] = self.log

                prefix = jobs[job_id]['prefix']

                if prefix[-3:] == '.py':
                    spec = importlib.util.spec_from_file_location(module_name, prefix)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    module = importlib.import_module(f'{prefix}.{module_name}')

                attr = getattr(module, class_name)
                jobs[job_id]['instance'] = attr(**init_args)

            while len(started) != len(jobs):
                for i, job_id in enumerate(jobs):
                    job = jobs[job_id]

                    num_finished = 0
                    for parent_job in job['depends_on']:
                        if parent_job in started and not processes[parent_job].is_alive():
                            num_finished += 1

                    if len(job['depends_on']) == num_finished:
                        started.add(i)
                        processes[job_id] = []

                        self.log.info('Launching {job_id} number {i}', job_name=job_id, i=i)

                        for j in range(job['n_jobs']):
                            if job['add_process_num']:
                                job['run_args']['process_num'] = j

                            target = job['instance'].run
                            if job['mode'] == 'worker':
                                target = Worker(job['instance'].run, self.log).run

                            processes[job_id] += [multiprocessing.Process(target=target,
                                                                          kwargs=job['run_args'])]
                            processes[job_id][-1].start()

                for job_id in processes:
                    for process in processes[job_id]:
                        process.join()

                self.__terminate_all(processes)
        finally:
            self.__terminate_all(processes)
