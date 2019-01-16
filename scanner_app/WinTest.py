import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    print('is an admin')

    # TODO run main file
    print(__file__)
    errorRet = ctypes.windll.shell32.ShellExecuteA(None, "runas", sys.executable, 'scanner_app/Main.py', None, 1)
    # keep getting path not found errors here
    print(int(errorRet))


    input('Test complete: press enter')
else:
    print('restarting...')

    # https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-shellexecutew
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

