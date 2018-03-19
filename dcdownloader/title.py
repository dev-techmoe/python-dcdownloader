import sys, platform

def for_linux(title):
    sys.stdout.write("\x1b]2;%s\x07" % title)
    sys.stdout.flush()

def for_windows(title):
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(str(title))

def check_platform():
    platform_flag = platform.system()
    if platform_flag == 'Windows':
        return False
    else:
        return True

def update(title):
    if check_platform():
        for_linux(title)
    else:
        for_windows(title)

if __name__ == '__main__':
    while True:
        import time
        update('test - %s' % time.time())
        time.sleep(1)
        