import sys
from multiprocessing import Manager, Process
import yaml
import json
from jsonschema import validate
import os.path
import logging
from tempfile import mkstemp
import os
from tx.parallex.dependentqueue import DependentQueue
from tx.parallex.task import enqueue, EndOfQueue, either_data
from tx.parallex.process import work_on
from tx.parallex.io import write_to_disk, read_from_disk
from tx.parallex.python import python_to_spec
from tx.parallex.spec import dict_to_spec
from tx.parallex.objectstore import PlasmaStore, SimpleStore
from tx.readable_log import getLogger

logger = getLogger(__name__, logging.INFO)

with open(os.path.join(os.path.dirname(__file__), "schema.json")) as f:
    schema = json.load(f)

def run_python(number_of_workers, pyf, dataf, system_paths=[], validate_spec=True, output_path=None, level=0, object_store=None):
    with open(pyf) as s:
        py = s.read()
    with open(dataf) as d:
        data = yaml.safe_load(d)
    return _start_python(number_of_workers, py, data, system_paths, validate_spec, output_path, level, object_store)


def run(number_of_workers, specf, dataf, system_paths=[], validate_spec=True, output_path=None, level=0, object_store=None):
    with open(specf) as s:
        spec = yaml.safe_load(s)
    with open(dataf) as d:
        data = yaml.safe_load(d)
    return _start(number_of_workers, spec, data, system_paths, validate_spec, output_path, level, object_store)


def start_python(number_of_workers, py, data, system_paths, validate_spec, output_path, level, object_store):
    add_paths = list(set(system_paths) - set(sys.path))
    sys.path.extend(add_paths)
    logger.debug(f"add_paths = {add_paths}")
    try:
        spec = python_to_spec(py)
    finally:
        for _ in range(len(add_paths)):
            sys.path.pop()
    return start(number_of_workers, spec, data, system_paths, validate_spec, output_path, level, object_store)


DEFAULT_PLASMA_STORE_SIZE = 50000000


def start(number_of_workers, spec, data, system_paths, validate_spec, output_path, level, object_store):
    if validate_spec:
        validate(instance=spec, schema=schema)
    if output_path is None:
        fd, temp_path = mkstemp()
        os.close(fd)
    else:
        temp_path = output_path

    try:
        shutdown_object_store = False
        with Manager() as manager:
            if object_store is None:
                try:
                    import pyarrow
                    logger.info("using PlasmaStore")
                    object_store = PlasmaStore(manager, DEFAULT_PLASMA_STORE_SIZE)
                except:
                    logger.info("using SimpleStore")
                    object_store = SimpleStore(manager)
                object_store.init()
                shutdown_object_store = True
            
            job_queue = DependentQueue(manager, EndOfQueue(), object_store)
            enqueue(dict_to_spec(spec), either_data(data), job_queue, level=level)
            processes = []
            for _ in range(number_of_workers):
                p = Process(target=work_on, args=(job_queue, system_paths))
                p.start()
                processes.append(p)
            p2 = Process(target=write_to_disk, args=(job_queue, temp_path))
            p2.start()
            processes.append(p2)
            for p in processes:
                p.join()
            if output_path is None:
                return read_from_disk(temp_path)

    finally:
        if shutdown_object_store:
            object_store.shutdown()
        if output_path is None:
            os.remove(temp_path)
