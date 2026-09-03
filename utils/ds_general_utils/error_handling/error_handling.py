"""
Task Management and Email Preparation Module

This module provides classes and functions for managing tasks, tracking their 
success, and generating formatted HTML emails summarizing task results for 
reporting or alerting purposes.

Classes:
    Task - Represents an individual task with name, details, and success status.
    TaskManager - Manages a collection of tasks, checks for errors, and generates 
                  HTML-formatted emails for task reporting.

Functions:
    load_config - Utility function to load a JSON configuration file from a specified 
                  directory with a given prefix.
"""

from ..exceptions import PriorTasksFailedError


class Task(dict):
    """
    Represents a task with its name, details, and success status.

    Args:
        task_nm (str): The name of the task.
        task_details (str, optional): Additional details about the task. Defaults to an empty string.
        success (bool, optional): Flag indicating whether the task was successful. Defaults to False.
    """

    def __init__(self, task_nm: str, task_details: str = "", success: bool = False):
        super().__init__({"Name": task_nm, "Details": task_details, "Success": success})

    def set_details(self, details: str) -> None:
        """
        Sets or updates the details of the task.

        Args:
            details (str): The new details for the task.
        """
        self["Details"] = details

    def set_success(self, success_flg: bool) -> None:
        """
        Sets or updates the success status of the task.

        Args:
            success_flg (bool): The new success status for the task.
        """
        self["Success"] = success_flg


class TaskManager:
    """
    Manages a collection of tasks for a specific process, tracking overall success and providing an
    email-friendly summary of task outcomes.

    Args:
        process_nm (str): The name of the process this TaskManager instance tracks.
    """

    def __init__(self, process_nm: str):
        self._tasks = []
        self._process_nm = process_nm
        self._process_success = "Success"

    def add_task(self, task: Task) -> None:
        """
        Adds a task to the manager and updates the overall process status based on the task's success.

        Args:
            task (Task): The task instance to add.

        Note:
            If the task is unsuccessful, the process status will be marked as "Failed."
        """
        self._tasks.append(task)
        if not task["Success"]:
            self._process_success = "Failed"

    def check_errors(self) -> None:
        """
        Checks for any tasks marked as unsuccessful and raises an error if any are found.

        Raises:
            PriorTasksFailedError: If any task in the manager has failed.
        """
        for task in self._tasks:
            if not task["Success"]:
                self._process_success = "Failed"
                raise PriorTasksFailedError("Prior Task Failed")

    def generate_task_email(self, file_dt: str) -> tuple[str, str]:
        """
        Generates a subject and HTML body representing the task report for email.

        Args:
            file_dt (str): The date identifier for the report.

        Returns:
            tuple[str, str]: The email subject and HTML body.

        Note:
            The subject includes the process name, date, and overall success status.
        """
        subject = "{process_nm} {file_dt} Process {success_flg}"
        body = [
            '<table style="border: 1px solid black">',
            """
            <tr>
            <th style="text-align: left;border-collapse: collapse;">Task</th>
            <th style="text-align: left;border-collapse: collapse;">Message</th>
            <th style="text-align: left;border-collapse: collapse;">Success?</th>
            </tr>
            """,
        ]
        for item in self._tasks:
            row = "<tr>"
            for key in item:
                row += TaskManager._generate_row_element(item[key], key)
            row += "</tr>"
            body.append(row)
        body.append("</table>")
        return subject.format(
            process_nm=self._process_nm,
            file_dt=file_dt,
            success_flg=self._process_success,
        ), "".join(body)

    @staticmethod
    def _generate_row_element(text: str, task_type: str) -> str:
        """
        Creates an HTML table cell element for a given task detail.

        Args:
            text (str): The text content of the cell.
            task_type (str): The type of task field (e.g., "Success", "Name").

        Returns:
            str: An HTML string representing the cell element.

        Note:
            Colors cells based on the success status or bolds task names for clarity.
        """
        td_style = ""
        if task_type == "Success":
            if text:
                td_style = "background-color: #90EE90;text-align:center;"
                text = "&#10004;"
            else:
                td_style = "background-color: #FF0000;text-align:center;"
                text = "&#10060;"
        elif task_type == "Name":
            td_style = "font-weight: bold;"
        return f'<td style="border-collapse: collapse; border-top: 1px solid black;{td_style}">{text}</td>'
