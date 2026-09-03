"""
Multi-Threaded Distributed Logging Module

This module provides a utility class, MultiThreadedLogger, to create a multi-threaded, distributed logging system.
It enables your application to log messages to a file while offloading the logging process to a separate thread,
allowing the main program to continue running without being delayed by logging operations.

Usage:
1. Import this module and initialize the MultiThreadedLogger class in your Python application.

2. To create and use the logger:
    Example:
    ```python
    from logging_module import MultiThreadedLogger

    # Initialize the logger with desired settings.
    logger_manager = MultiThreadedLogger('app.log', 'MyApp', 'TaskA', level='INFO')

    # Retrieve the logger and use it for logging.
    logger = logger_manager.logger
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')

    # Ensure to call logger_manager.cleanup() on application shutdown.
    logger_manager.cleanup()
    ```
"""

import logging
import threading
from queue import Queue
import socket
import os


class MultiThreadedLogger:
    """
    A utility class to set up a multi-threaded, distributed logger with specified settings.
    """

    def __init__(
        self,
        logger_file_name: str,
        program: str,
        task: str,
        level: str = "INFO",
        format_string: str = None,
    ):
        """
        Initialize the MultiThreadedLogger with specified settings.

        Args:
            logger_file_name (str): The name of the log file to write logs to.
            program (str): The name of the program using the logger.
            task (str): The name of the task or component within the program.
            level (str): The logging level (e.g., 'INFO', 'DEBUG'). Default is 'INFO'.
            format_string (str, optional): The format for log messages. Defaults to None.

        The initialization also starts a background thread to process log entries.

        It also ensures the log directory exists, creates an archive directory if needed,
        and moves older log files to the archive directory if there are more than 5 log files.
        """
        self.worker_logger = None
        self.log_queue = Queue()
        self.log_file_name = logger_file_name
        # Check if the directory exists, if not, create it
        log_dir = os.path.dirname(logger_file_name)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Check for more than 5 .log files and archive older ones
        log_files = sorted(
            [f for f in os.listdir(log_dir) if f.endswith(".log")],
            key=lambda x: os.path.getmtime(os.path.join(log_dir, x)),
        )
        if len(log_files) > 5:
            archive_dir = os.path.join(log_dir, "archive")
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            for log_file in log_files[:-5]:
                os.rename(
                    os.path.join(log_dir, log_file), os.path.join(archive_dir, log_file)
                )

        self.program = program
        self.task = task
        self.level = level
        self.format_string = (
            format_string
            or f"{socket.gethostname()}:{program}:{task}:%(asctime)s:%(levelname)s:%(message)s"
        )

        # Start the logging worker thread
        self.log_thread = threading.Thread(target=self.__log_worker__)
        self.log_thread.daemon = False
        self.log_thread.start()

        # Set up the main logger
        self.logger = self.__initialize_logger__()

    def __initialize_logger__(self) -> logging.Logger:
        """
        Initialize and return a logger that uses a queue handler.

        Returns:
            logging.Logger: A logger instance configured to use the queue handler.
        """
        logger = logging.getLogger(f"{self.program}.{self.task}")
        logger.setLevel(self.level)
        logger.propagate = False  # Prevent messages from propagating to the root logger

        # Queue handler for offloading log handling to the worker thread
        queue_handler = logging.handlers.QueueHandler(self.log_queue)
        logger.addHandler(queue_handler)
        return logger

    def __log_worker__(self) -> None:
        """
        Worker thread function that continuously processes log records from the queue and writes to a file.
        """
        self.worker_logger = logging.getLogger("log_worker")
        # Remove old handlers if present
        self.worker_logger.handlers.clear()

        file_handler = logging.FileHandler(self.log_file_name)
        formatter = logging.Formatter(self.format_string)
        file_handler.setFormatter(formatter)
        self.worker_logger.addHandler(file_handler)
        self.worker_logger.setLevel(self.level)
        self.worker_logger.propagate = False

        while True:
            record = self.log_queue.get()
            if record is None:
                break
            self.worker_logger.handle(record)

    def cleanup(self) -> None:
        """
        Gracefully terminate the logging thread and cleanup resources.
        Call this function on application shutdown to ensure proper cleanup.
        """
        # Signal the logging thread to terminate
        self.log_queue.put(None)
        self.log_thread.join()

        # Close and remove all handlers from the main logger
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Close and remove all handlers from the worker_logger
        if hasattr(self, "worker_logger"):
            for handler in self.worker_logger.handlers[:]:
                handler.close()
                self.worker_logger.removeHandler(handler)

        # Clear handlers to avoid resource leakage
        self.logger.handlers.clear()
        if hasattr(self, "worker_logger"):
            self.worker_logger.handlers.clear()
