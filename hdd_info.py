import sys
import os
import subprocess
from abc import ABCMeta, abstractmethod


class OSHelper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def list_hdds(self):
        pass

    @abstractmethod
    def list_parts(self, disk_nr):
        pass


class WinHelper(OSHelper):
    def run_diskpart(self, command):
        fname = 'command.txt'
        with open(fname, 'w') as f:
            f.write(command)
        dp = subprocess.Popen('diskpart /s {}'.format(fname), shell=True, stdout=subprocess.PIPE)
        o,e = dp.communicate()
        if dp.returncode == 0:
            return o
        else:
            if o:
                print o
            else:
                print("An error has occured. Please try running as administrator")

    def list_hdds(self):
        COMMAND = 'list disk'
        output = self.run_diskpart(COMMAND)
        if output:
            return '\n'.join(output.split('\n')[6:])

    def list_parts(self, n):
        COMMAND = 'select disk {}\nlist partition'.format(int(n))
        output = self.run_diskpart(COMMAND)
        if output:
            return '\n'.join(output.split('\n')[7:])


def get_os_helper():
    """
    :rtype: OSHelper
    """
    if os.name == 'nt':
        return WinHelper()
    elif os.name == 'posix':
        return UnixHelper()


if __name__ == '__main__':
    helper = get_os_helper()
    if len(sys.argv) == 1:
        print(helper.list_hdds())
    elif len(sys.argv) == 2:
        print(helper.list_parts(sys.argv[1]))