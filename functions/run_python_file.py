import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, absolute_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output_string = ""

        if not process.returncode == 0:
            output_string += f"Process exited with code {process.returncode}."
        if process.stdout == "" and process.stderr == "":
            output_string += "No output produced."
        if process.stdout != "":
            output_string += f"STDOUT: {process.stdout}."
        if process.stderr != "":
            output_string += f"STDERR: {process.stderr}."

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
