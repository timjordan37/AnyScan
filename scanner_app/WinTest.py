import sys
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    print('is an admin')
    input('Test complete')
    # TODO run main file
else:
    print('restarting...')

    # https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-shellexecutew
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

