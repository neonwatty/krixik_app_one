import subprocess
from typing import IO, Optional


def execute_subprocess_command(command: list, cwd: str = ".", stdin: Optional[IO] = None) -> str:
    output = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return_code = output.wait()

    # get stdout and stderr
    stdout, stderr = output.communicate()
    stdout = stdout.decode("utf-8")

    assert return_code == 0, f"return code {return_code} for command {command} - error --> {stdout}"
    return stdout
