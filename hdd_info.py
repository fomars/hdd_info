import sys
import os
import subprocess

def list_hdds_win():
    wmic = subprocess.Popen('wmic diskdrive get name,size', shell=True, stdout=subprocess.PIPE)
    out, err = wmic.communicate()
    drives = out.split('\n')[1:-2]
    return '\n'.join(drives)

def list_hdds():
    if os.name == 'nt':
        return list_hdds_win()
    elif os.name == 'posix':
        return list_hdds_unix()
    else:
        return 'Your system is not supported'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(list_hdds())
    elif len(sys.argv) == 2:
        print(list_partitions(sys.argv[1]))