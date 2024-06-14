import os
import subprocess
from sys import stderr, stdout
from evillimiter.console.io import IO

DEVNULL = open(os.devnull, 'w')

def check_doas_sudo():
    try: 
        subprocess.run("which doas", check=True, stdout=DEVNULL, stderr=DEVNULL, shell=True)
        return "doas "
    except subprocess.CalledProcessError as e:
        return "sudo "

def execute(command, root=True):
    return subprocess.call(check_doas_sudo() + command if root else command, shell=True)


def execute_suppressed(command, root=True):
    return subprocess.call(check_doas_sudo() + command if root else command, shell=True, stdout=DEVNULL, stderr=DEVNULL)


def output(command, root=True):
    return subprocess.check_output(check_doas_sudo() + command if root else command, shell=True).decode('utf-8')


def output_suppressed(command, root=True):
    return subprocess.check_output(check_doas_sudo() + command if root else command, shell=True, stderr=DEVNULL).decode('utf-8')


def locate_bin(name):
    try:
        return output_suppressed('which {}'.format(name)).replace('\n', '')
    except subprocess.CalledProcessError:
        IO.error('missing util: {}, check your PATH'.format(name))
