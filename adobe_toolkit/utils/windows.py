import ctypes
import subprocess
import winreg
from typing import Optional, List

def get_registry_value(key: str, value: str) -> Optional[str]:
    """Retrieve a value from the Windows registry.

    Args:
        key (str): The registry key path.
        value (str): The name of the value to retrieve.

    Returns:
        Optional[str]: The value from the registry, or None if not found.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
            return winreg.QueryValueEx(reg_key, value)[0]
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None

def list_running_processes() -> List[str]:
    """List all currently running processes on the Windows system.

    Returns:
        List[str]: A list of names of running processes.
    """
    try:
        process_list = subprocess.check_output(['tasklist'], text=True)
        processes = [line.split()[0] for line in process_list.splitlines()[3:] if line]
        return processes
    except subprocess.CalledProcessError as e:
        print(f"Error listing processes: {e}")
        return []

def kill_process(name: str) -> bool:
    """Kill a process by its name.

    Args:
        name (str): The name of the process to kill.

    Returns:
        bool: True if the process was killed successfully, False otherwise.
    """
    try:
        subprocess.run(['taskkill', '/F', '/IM', name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error killing process '{name}': {e}")
        return False

def is_admin() -> bool:
    """Check if the current user has admin privileges.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def run_as_admin(cmd: str) -> int:
    """Run a command with administrative privileges.

    Args:
        cmd (str): The command to run.

    Returns:
        int: The exit code of the command.
    """
    try:
        return subprocess.run(['runas', '/user:Administrator', cmd], check=True).returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running command as admin: {e}")
        return e.returncode
