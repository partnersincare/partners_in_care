import json
from datetime import datetime
import os


class PriorTasksFailedError(Exception):
    pass


class Task(dict):
    def __init__(self, task_nm: str, task_details: str = "", success: bool = False):
        super().__init__({"Name": task_nm, "Details": task_details, "Success": success})

    def set_details(self, details: str) -> None:
        self["Details"] = details

    def set_success(self, success_flg: bool) -> None:
        self["Success"] = success_flg


class TaskManager:
    def __init__(self, process_nm: str):
        self._tasks = []
        self._process_nm = process_nm
        self._process_success = "Success"

    def add_task(self, task: Task):
        self._tasks.append(task)
        if task["Success"] != True:
            self._process_success = "Failed"

    def check_errors(self) -> None:
        for task in self._tasks:
            if task["Success"] != True:
                self._process_success = "Failed"
                raise PriorTasksFailedError("Prior Task Failed")

    def generate_task_email(self, file_dt: str) -> tuple[str, str]:
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
                row = row + _generate_row_element(item[key], key)
            row = row + "</tr>"
            body.append(row)
        body.append("</table>")
        return subject.format(
            process_nm=self._process_nm,
            file_dt=file_dt,
            success_flg=self._process_success,
        ), "".join(body)

    # def compose_user_message(file_dt):


def _generate_row_element(text: str, task_type: str) -> str:
    td_style = ""
    if task_type == "Success":
        if text:
            td_style = "background-color: #90EE90;text-align:center;"
            text = "&#10004;"
        else:
            td_style = "backgorund-color: #FF0000;text-align:center;"
            text = "&#10060;"
    elif task_type == "Name":
        td_style = "font-weight: bold;"
    element = '<td style="border-collapse: collapse; border-top: 1px solid black;{}">{}</td>'.format(
        td_style, text
    )
    return element


def load_config(directory, file_prefix):
    for filename in os.listdir(directory):
        if filename.startswith(file_prefix) and filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)
                return config_data
    return None
