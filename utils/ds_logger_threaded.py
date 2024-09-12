"""
Multi-Threaded Distributed Logging Module

This module provides a utility for creating a multi-threaded, distributed logging system.
It allows you to configure a logger for your application and log messages to a file while
offloading the logging process to a separate thread. This enables your application to
continue running without being delayed by the time-consuming process of writing logs.

Usage:
1. Import this module into your Python application.

2. To create a logger for your program and task, use the `get_mt_ds_logger` function:

    Example:
    ```python
    import mt_ds_logger

    # Configure the logger with a log file name, program name, task name, and optional settings.
    logger = mt_ds_logger.get_mt_ds_logger('app.log', 'MyApp', 'TaskA', level='INFO')

    # Log messages as you normally would.
    logger.info('This is an information message.')
    logger.warning('This is a warning message.')

    # Make sure to call logger.cleanup() when ending your use of the logger, typically
    # during application shutdown to ensure proper termination of the logger and worker thread.
    logger.cleanup()
    ```
"""


import logging
import threading
from queue import Queue
import socket


def __log_worker__(log_queue, log_file_name, log_format, log_level):
    """
    This Internal only function represents a worker thread for logging. Is not to be explicitly called.

    Args:
        log_queue (Queue): A queue for receiving log records.
        log_file_name (str): The name of the log file to write logs to.
        log_format (str): The format for log messages.
        log_level (str): The logging level (e.g., 'INFO', 'DEBUG').

    This function runs in a separate thread, continuously processing log records
    and writing them to a log file.
    """

    worker_logger = logging.getLogger("log_worker")
    file_handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    worker_logger.addHandler(file_handler)
    worker_logger.setLevel(log_level)
    worker_logger.propagate = (
        False  # Prevent messages from propagating to the root logger
    )

    while True:
        record = log_queue.get()
        if record is None:  # Indicates that the thread should exit
            break
        worker_logger.handle(record)


def get_mt_ds_logger(logger_file_name, program, task, level="INFO", format_string=None):
    """
    Create a multi-threaded, distributed logger with the specified settings.

    Args:
        logger_file_name (str): The name of the log file to write logs to.
        program (str): The name of the program or module using the logger.
        task (str): The name of the task or component within the program.
        level (str): The logging level (e.g., 'INFO', 'DEBUG'). Default is 'INFO'.
        format_string (str, optional): The format for log messages. Default is None.

    Returns:
        logger (Logger): A logger instance configured with the specified settings.

    This function sets up a multi-threaded, distributed logging system. It creates a
    worker thread for handling log records and returns a logger configured to use
    this worker thread for logging.

    Note: To ensure proper cleanup and termination of the logger and worker thread,
    make sure to call `logger.cleanup()` when ending your use of the logger, typically
    during application shutdown.

    """

    if format_string is None:
        machine_name = socket.gethostname()
        format_string = (
            f"{machine_name}:{program}:{task}:%(asctime)s:%(levelname)s:%(message)s"
        )

    log_queue = Queue()
    log_thread = threading.Thread(
        target=__log_worker__, args=(log_queue, logger_file_name, format_string, level)
    )
    log_thread.daemon = False  # ensures that the main program doesn't end before the logging thread has terminated
    log_thread.start()

    logger = logging.getLogger(f"{program}.{task}")
    logger.setLevel(level)
    logger.propagate = False  # Prevent messages from propagating to the root logger

    def cleanup():
        """
        Cleanup function to gracefully terminate the logger and worker thread.
        Call this function when your application is shutting down.

        """
        log_queue.put(None)
        log_thread.join()
        logger.removeHandler(handle)

    handle = logging.handlers.QueueHandler(log_queue)
    logger.addHandler(handle)  # Add a handler to queue log messages
    logger.cleanup = cleanup
    return logger
