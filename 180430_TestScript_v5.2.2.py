'''
Created on Feb 14, 2018
@author: Vivek Kumbhar
Script to Automate the functionality of Reference Platform. Various test cases
will be automated to run smoke tests on the Reference Platform board to
validate the basic functionality of all the components, features, services, and
modules.
'''
#
# !/usr/bin/env python -W ignore::PendingDeprecationWarning
#
# import pytest
import inspect
import unittest

# import urllib
# import os
import webbrowser
import subprocess
# from urllib.request import urlopen
import webbrowser
import subprocess
import sys
import warnings
from colorama import Fore, Back, Style

from typing import ItemsView
import time

from pexpect import pxssh
import getpass
# import spur
# from spur import SshShell
import paramiko

Device_Name = 'i.MX 6 Series'
Hardware_Version = 'Reference Platform'
Software_Version = '5.2.2'
host = '172.90.0.122'
user = 'root'
pw = ''
test_dir = '/autonet/tests'
stid = 1  # number used as sub test case id to number the test cases withinn a test case
sno = 1  # number used to count total number of test cases
pass_tc = 0
fail_tc = 0
inside_pass_tc = 0
inside_fail_tc = 0

start_time = time.time()
ssh_time = 0

# sudopw = 'golear'

# print (time.strftime("%I:%M:%S%p"))
# print (time.strftime("%x:%X"))
wait = time.sleep

platform = subprocess.getoutput('uname -s -r -m -o')
# print (platform)

# platform = subprocess.run("uname -a", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
# print (platform.stdout)

#class to to suppress the console errors temporarily. Foe example "Error reading SSH protocol banner", which is displayed at the time or board is "rebooting"
class NullDevice():
    def write(self, s):
        pass

def log(msg):
    print(time.strftime("%I:%M:%S%p") + ": " + msg)


def log_red(msg, tid=''):  # change "log_red" to "log" if no color is required in output
    global sno
    global stid
    global fail_tc
    global inside_fail_tc
    print(str(sno) + "." + tid + ": " + str(stid) + ": ", end="")
    print(Fore.RED + msg + Style.RESET_ALL)
    stid += 1
    sno += 1

    fail_tc += 1
    inside_fail_tc += 1


def log_green(msg, tid=''):  # change "log_green" to "log" if no color is required in output
    global sno
    global stid
    global pass_tc
    global inside_pass_tc
    print(str(sno) + "." + tid + ": " + str(stid) + ": ", end="")
    print(Fore.GREEN + msg + Style.RESET_ALL)
    stid += 1
    sno += 1

    pass_tc += 1
    inside_pass_tc += 1


def log_blue(msg):  # change "log_blue" to "print" if no color is required in output
    print(Fore.BLUE + msg + Style.RESET_ALL)


def log_yellow(msg):  # change "log_blue" to "print" if no color is required in output
    print(Fore.YELLOW + msg + Style.RESET_ALL)


def run(self, cmd, tid=''):
    ssh = self.ssh
    try:
        stdin, stdout, stderr = ssh.exec_command('. /etc/profile; ' + cmd)
        # check if there is any error in issuing the command
        output = stdout.read().decode('UTF-8')
        result = stderr.read().decode('UTF-8')
        # print(output)
        # print(result)
        if len(result) > 0:
            log_red("An error in executing the test command encountered" + result + ": FAILED", tid)
            print(Fore.RED + "Output and Results of the failed command:%s, %s" % (output, result) + Style.RESET_ALL)
        else:
            pass

    except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    return(output)

def runr(self, cmd, tid=''):
    ssh = self.ssh
    try:
        stdin, stdout, stderr = ssh.exec_command('. /etc/profile; ' + cmd)
        # check if there is any error in issuing the command
        output = stdout.read().decode('UTF-8').replace("\n", "")
        result = stderr.read().decode('UTF-8').replace("\n", "")
        # print(output)
        # print(result)
        if len(result) > 0:
            log_red("An error in executing the test command encountered" + result + ": FAILED", tid)
            print(Fore.RED + "Output and Results of the failed command:%s, %s" % (output, result) + Style.RESET_ALL)
        else:
            pass

    except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)
    return(output)

def REFP_1000_test_stats():
    # def test_stats(self):
    '''collect the stats for the test run'''

    global sno
    global pass_tc
    global fail_tc

    total = sno - 1
    skipped_tc = total - (pass_tc + fail_tc)
    log_blue('\n[================================================================================================================]')
    log_yellow('[                         End of the Testing Summary: ' +
           time.strftime("%B%d, %Y %I:%M:%S%p %Z") + '                               ]')
    log_blue('[================================================================================================================]')
    # log_yellow('[                                    Total:%s' % total + ' Passed:%s' % pass_tc + ' Failed:%s' % fail_tc + ' Skipped:%s                   ' % skipped_tc)
    log_yellow('[                                    Total:%s' % total + ' Passed:%s' % pass_tc + ' Failed:%s' % fail_tc + ' Skipped:%s                   ' % skipped_tc)
    log_blue('[================================================================================================================]')


log_blue('\n[================================================================================================================]')
log_yellow('[                              Start of the Testing : ' +
           time.strftime("%B%d, %Y %I:%M:%S%p %Z") + '                               ]')
log_blue('[================================================================================================================]')
print('[Device:                ]: %s' % Device_Name)
print('[Hardware Version       ]: %s' % Hardware_Version)
print('[Environment Version    ]: %s' % platform)
print('[Software Version       ]: %s' % Software_Version)
log_blue('[================================================================================================================]')


class SmokeTests(unittest.TestCase):
    "Class to run smoke tests on the Reference Platform"

    def setUp(self):
        tid = 'REFP_000'
        global start_time
        global ssh_time
        warnings.simplefilter("ignore", category=PendingDeprecationWarning)
        warnings.simplefilter("ignore", category=ResourceWarning)
        ssh = paramiko.SSHClient()  # handle
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        log_blue(
            '\n[================================================================================================================]')

        log_yellow('[                         Start of the Test Suite Execution : ' +
                   time.strftime("%B%d, %Y %I:%M:%S%p %Z") + '                       ]')
        log_blue('[================================================================================================================]')

        while True:
            #writing next two lines to suppress the console error "Error reading SSH protocol banner", which is displayed at the time or board is "rebooting"
            original_stderr = sys.stderr
            sys.stderr = NullDevice()
            try:
                #print('test2')
                #wait(2)
                ssh.connect(host, username=user, password=pw, look_for_keys=False, allow_agent=False, banner_timeout=None, auth_timeout=None)
                ssh_time = (time.time() - start_time)
                break

            except paramiko.ssh_exception.socket.error as e:
                #print('\nATTENTION: SSH transport has socket error...\n')
                continue
            except paramiko.ssh_exception.AuthenticationException as e:
                #print('\nATTENTION: SSH transport has Authentication excepetion...\n')
                continue
            except paramiko.ssh_exception.BadHostKeyException as e:
                #print('\nATTENTION: SSH transport has BadHostKeyException...\n')
                continue
            except paramiko.ssh_exception.SSHException as e:
                #print('\nATTENTION: SSH transport has SSHException...\n')
                continue
            except Exception as e:
                #print('\nATTENTION: SSH transport has undefined exception...\n')
                continue

        #setting the standard errors back again
        original_stderr = sys.stderr
        self.ssh = ssh  # handle

    def tearDown(self):
        global stid
        global inside_fail_tc
        global inside_pass_tc
        ssh = self.ssh  # handle
        # self.driver.reset()
        # self.driver.close_app()
        stid -= 1
        ssh.close()
        skipped = stid - (inside_pass_tc + inside_fail_tc)
        log_blue('[================================================================================================================]')
        log_yellow('[                          End of the Test Suite Execution : ' +
                   time.strftime("%B%d, %Y %I:%M:%S%p %Z") + '                        ]')
        log_yellow('[                                    Total:%s' % stid + ' Passed:%s' % inside_pass_tc + ' Failed:%s' % inside_fail_tc + ' Skipped:%s                   ' % skipped)
        log_blue('[================================================================================================================]')
        stid = 1
        inside_fail_tc = 0
        inside_pass_tc = 0
        wait(1)

    def test_Collect_Performance_Metrics(self):
        '''collect performance metrics'''
        # TBD
        # global stid
        tid = 'REFP_000'
        ssh = self.ssh  # handle
        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Collect the Reference Platform performance metrics')
        print('[Product Requirement    ]: None')
        print('[Development Task       ]: Miscellaneous')
        print('[Test Automation Task   ]: CONLAREINS-474')
        log_blue('[================================================================================================================]')

        while True:
            try:
                stdin, stdout, stderr = ssh.exec_command('. /etc/profile; hostname')  # check if there is any error in issuing the command
                result = stderr.read().decode('UTF-8').replace("\n", "")
                if len(result) > 0:
                    # log_red("error in executing the command encountered" + result + ": FAILED", tid)
                    pass
                else:
                    wait(1)
                    stdin, stdout, stderr = ssh.exec_command('. /etc/profile; hostname')
                    output = stdout.read().decode('UTF-8').replace("\n", "")
                    break
            except Exception as e:
                log_red("Operation error:" + str(e) + ": FAILED", tid)
                break

        command_time = time.time() - start_time
        log_green('Time to successful SSH from power cycle: %.2f' % ssh_time + ' Seconds', tid)
        log_green('Time to first command from power cycle: %.2f' % command_time + ' Seconds', tid)


        #doing the calculation of the SSH and COMMAND time after the reboot
        #add the code after these comments if reboot test needs to be done

        '''
        reboot_start_time = time.time()
        output = run(self, 'reboot', tid)
        while True:
            #writing next two lines to suppress the console error "Error reading SSH protocol banner", which is displayed at the time or board is "rebooting"
            original_stderr = sys.stderr
            sys.stderr = NullDevice()
            try:
                #print('test2')
                #wait(2)
                ssh.connect(host, username=user, password=pw, look_for_keys=False, allow_agent=False, banner_timeout=None, auth_timeout=None)
                reboot_ssh_time = (time.time() - reboot_start_time)
                break

            except Exception as e:
                #print('\nATTENTION: SSH transport has undefined exception...\n')
                continue

        #setting the standard errors back again
        original_stderr = sys.stderr

        while True:
            try:
                stdin, stdout, stderr = ssh.exec_command('. /etc/profile; hostname')  # check if there is any error in issuing the command
                result = stderr.read().decode('UTF-8').replace("\n", "")
                if len(result) > 0:
                    # log_red("error in executing the command encountered" + result + ": FAILED", tid)
                    pass
                else:
                    wait(1)
                    stdin, stdout, stderr = ssh.exec_command('. /etc/profile; hostname')
                    output = stdout.read().decode('UTF-8').replace("\n", "")
                    break
            except Exception as e:
                log_red("Operation error:" + str(e) + ": FAILED", tid)
                break
        reboot_command_time = time.time() - reboot_start_time
        log_green('Time to successful SSH after soft reboot: %.2f' % reboot_ssh_time + ' Seconds', tid)
        log_green('Time to first command after soft reboot: %.2f' % reboot_command_time + ' Seconds', tid)

        # end of doing the calculation of the SSH and COMMAND time after the reboot
        '''
        #Collect the bootup time for kernel and userspace
        output = runr(self, 'systemd-analyze', tid)
        log_green(output, tid)

        #Collect the Hardware name
        output = runr(self, 'cat /proc/cpuinfo | grep Hardware', tid)
        log_green(output, tid)

        #Collect the Hardware version
        output = runr(self, 'cat /proc/version', tid)
        log_green('Linux Version: ' + output[14:], tid)


        #Collect the Board name
        output = runr(self, 'fw_printenv board_name', tid)
        log_green('Board Name: ' + output[11:], tid)

        #Collect the Rev
        output = runr(self, 'fw_printenv board_rev', tid)
        log_green('Revision Number: ' + output[10:], tid)

        #Collect the MAC
        output = runr(self, 'fw_printenv ethaddr', tid)
        log_green('MAC address or Serial Number of the board: ' + output[8:], tid)
        #Collect the Kernel Number
        output = runr(self, 'fw_printenv kernel', tid)
        log_green('Kernel ID: ' + output[7:], tid)
        #Collect the Image file name
        output = runr(self, 'fw_printenv fdt_file', tid)
        log_green('Image File Name: ' + output[9:], tid)
        #Collect the File Size
        output = runr(self, 'fw_printenv filesize', tid)
        log_green('Image File Size: ' + output[9:], tid)
        #Collect the Meomory Size Available
        '''
        output = runr(self, 'free', tid)
        log_green('Resting Memory Available' + output[10:50], tid)
        '''
        #Collect the storage Available
        output = runr(self, 'df -h|grep Filesystem', tid)
        log_green('Memory Available: ' + output, tid)
        #Collect the storage Available
        output = runr(self, 'df -h|grep /dev/root', tid)
        log_green('Memory Available: ' + output, tid)
        #Collect the storage Available
        output = runr(self, 'df -h|grep /dev/mapper/user', tid)
        log_green('Memory Available: ' + output, tid)
        #Collect the storage Available
        output = runr(self, 'df -h|grep /dev/mapper/autonet', tid)
        log_green('Memory Available: ' + output, tid)
        #Collect the storage Available
        output = runr(self, 'df -h|grep /dev/mapper/proprietary', tid)
        log_green('Memory Available: ' + output, tid)
        #Collect Memory utilization
        output = runr(self, 'top -n1|grep Mem:', tid)
        log_green('Storage Available: ' + output[10:90], tid)
        #Collect CPU utilization
        output = runr(self, 'top -n1|grep CPU:', tid)
        log_green('CPU Utilization: ' + output[5:90], tid)

    def test_REFP_001_Prompt_and_Hostname(self):
        '''Verify the prompt and Hostname of the Reference Platform to contain Einstein, Mac address (serial number), path and software version '''
        # global stid
        tid = 'REFP_001'
        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the prompt and Hostname of the Device to contain Einstein, Mac, path and version')
        print('[Product Requirement    ]: EINST-001')
        print('[Development Task       ]: CONLAREINS-68')
        print('[Test Automation Task   ]: CONLAREINS-78')
        log_blue('[================================================================================================================]')

        # Test case to check if software version number is embedded in the prompt
        try:
            stdin, stdout, stderr = ssh.exec_command(
                '. /etc/profile; echo $PS1')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8')

            if output.find("\\u@\\h(%s):\\w$" % Software_Version) != -1:
                log_green(
                    "Verify that the prompt is correctly composed: PASSED", tid)
            else:
                log_red("Verify that the prompt is correctly composed: FAILED", tid)

            if output.find(Software_Version) != -1:
                log_green(
                    "Verify the software version (%s) is part of the prompt: PASSED" % Software_Version, tid)
            else:
                log_red("Verify the software version (%s) is part of the prompt: FAILED" %
                        Software_Version, tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # Test case to check if hostname has einstein
        try:
            stdin, stdout, stderr = ssh.exec_command('hostname')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8')

            if output.find('einstein') != -1:
                log_green("Verify the hostname to be 'einstein': PASSED", tid)
            else:
                log_red("Verify the hostname to be 'einstein': FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # Test case to check if mac address in ifconfig and in the hostname is same
        try:
            stdin, stdout, stderr = ssh.exec_command('hostname')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            host = stdout.read().decode('UTF-8')[9:-1]

            stdin, stdout, stderr = ssh.exec_command('ifconfig')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            mac = stdout.read().decode('UTF-8')[41:55]
            serial = mac.replace(":", "")

            if host.find(serial) != -1:
                log_green("Verify that MAC(%s) and Serial(%s) in prompt are same: PASSED" % (
                    serial, host), tid)
            else:
                log_red("Verify that MAC(%s) and Serial(%s) in prompt are same: FAILED" % (
                    serial, host), tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # Test case to check if username is root
        try:
            stdin, stdout, stderr = ssh.exec_command('whoami')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8')

            if output.find('root') != -1:
                log_green(
                    "Verify the username in the prompt to be 'root': PASSED", tid)
            else:
                log_red(
                    "Verify the username in the prompt to be 'root': FAILED", tid)
        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_002_Default_IP_DNS_DHCP(self):
        '''Verify the default IP address for eth0 and check if DNS and DHCP services are running '''
        tid = 'REFP_002'
        global inside_pass_tc
        global inside_fail_tc

        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the default assigned ip of eth0 and running of DNS and DHCP')
        print('[Product Requirement    ]: EINST-002')
        print('[Development Task       ]: CONLAREINS-69')
        print('[Test Automation Task   ]: CONLAREINS-79')
        log_blue('[================================================================================================================]')

        # Test case to check if DNS and DHCP is running
        try:
            stdin, stdout, stderr = ssh.exec_command(
                'pidof dnsmasq > /dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")

            if output == '0':
                log_green(
                    "Verify that the DNS and DHCP processes are successfully running: PASSED", tid)
            else:
                log_red(
                    "Verify that the DNS and DHCP processes are successfully running: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # Test case to check if default IP address is 172.90.0.122
        try:
            stdin, stdout, stderr = ssh.exec_command(
                "[[ $(hostname -i) =~ '172.90.0.122' ]] && echo $? || echo 'FAILED'")
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")

            if output == '0':
                log_green(
                    "Verify that the default IP address of the Eth0 is %s: PASSED" % host, tid)
            else:
                log_red(
                    "Verify that the default IP address of the Eth0 is %s: FAILED" % host, tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_003_Secure_Storage_Keys(self):
        '''Verify the secure Data Storage implementation. Verify that the system provides a secure storage of keys to prevent exfiltration of sensitive key material'''
        tid = 'REFP_003'

        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the secure Data Storage implementation')
        print('[Product Requirement    ]: EINST-014')
        print('[Development Task       ]: CONLAREINS-26, CONLAREINS-27')
        print('[Test Automation Task   ]: CONLAREINS-77')
        log_blue('[================================================================================================================]')

        # Verify Secure data storage encryption
        try:
            stdin, stdout, stderr = ssh.exec_command(
                'cd %s; ./securedata/test_kernelcrypt random 32 > /dev/null; echo $?' % test_dir)
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")

            if output == '0':
                log_green(
                    "Verify that Linux kernel crypto provider are available and working: PASSED", tid)
                log_green(
                    "Verify that User code can access linux kernel crypto providers: PASSED", tid)
                log_green(
                    "Verify that Random number generation from kernel provider is working: PASSED", tid)
                log_green(
                    "Verify that AES-128 kernel provider is working (encrypt a block, decrypt a block): PASSED", tid)
                log_green(
                    "Verify that SHA-256 kernel provider is working: PASSED", tid)
            else:
                log_red("Verify Secure data storage encryption: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # Tests the functionality of the API described in securedata.h.
        try:

            # TBD

            stdin, stdout, stderr = ssh.exec_command(
                "cd %s; ./securedata/test_validation crypt 'my name is sushil123!' > /dev/null; echo $?" % test_dir)
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    "error in executing the test command encountered" + result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")

            if output == '0':
                log_green(
                    "Verify that Library is linkable on deployment platform: PASSED", tid)
                log_green(
                    'Verify that a “black key” can be created and saved to a file: PASSED', tid)
                log_green(
                    'Verify that the “black key” can be restored from the file: PASSED', tid)
                log_green(
                    "Verify that data can be round-trip encrypted and decrypted to memory using a black key: PASSED", tid)
                log_green(
                    "Verify that data can be round-trip encrypted and decrypted to a file using a black key: PASSED", tid)
                log_green(
                    "Verify that changing any bit in the encrypted data will cause decryption to fail: PASSED", tid)

            else:
                log_red("Validating Secure data storage encryption: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_004_Linux_as_OS(self):
        '''Verify that the reference platform device uses Linux as the Operating System'''
        tid = 'REFP_004'

        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print(
            '[Title                  ]: Verify that device uses Linux as the Operating System')
        print('[Product Requirement    ]: EINST-002')
        print('[Development Task       ]: CONLAREINS-7')
        print('[Test Automation Task   ]: CONLAREINS-109')
        log_blue('[================================================================================================================]')

        # Verify that the OS is Unix
        try:
            stdin, stdout, stderr = ssh.exec_command('uname')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")

            # print(result.decode('UTF-8'))
            # print(output)

            if output == 'Linux':
                log_green(
                    "Verify that the device uses Linux as the Operating System: PASSED", tid)
            else:
                log_red(
                    "Verify that the device uses Linux as the Operating System: FAILED", tid)
                log_red("Failed because device uses: %s" % output)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_005_Linux_Kernel_Version_ARM(self):
        '''Verify that the Reference Platform board is running the Linux Kernel version 4.9 for ARM'''
        tid = 'REFP_005'

        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify that the Reference Platform is running the Linux Kernel version 4.9.11 for ARM')
        print('[Product Requirement    ]: EINST-002')
        print('[Development Task       ]: CONLAREINS-8')
        print('[Test Automation Task   ]: CONLAREINS-110')
        log_blue('[================================================================================================================]')

        # Verify that the OS is Unix
        try:
            stdin, stdout, stderr = ssh.exec_command('uname -a')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")

            if output.find('Linux') != -1 and output.find('GNU/Linux') != -1 and output.find('4.9.11') != -1:
                log_green(
                    "Verify that the device uses Linux version Kernel 4.9.11 as the Operating System: PASSED", tid)
            else:
                log_red(
                    "Verify that the device uses Linux version kernel 4.9.11 as the Operating System: FAILED", tid)
                log_red(
                    "Failed because device uses following version of OS: %s" % output, tid)

            if output.find('arm') != -1 and output.find('GNU/Linux') != -1:
                log_green(
                    "Verify that the device uses Linux for ARM: PASSED", tid)
            else:
                log_red("Verify that the device uses Linux for ARM: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_006_Ethernet_Driver(self):
        '''Verify that the Ethernet driver is installed and working correctly'''
        tid = 'REFP_006'
        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify that the Ethernet driver is installed and working correctly')
        print('[Product Requirement    ]: EINST-002')
        print('[Development Task       ]: CONLAREINS-15')
        print('[Test Automation Task   ]: CONLAREINS-120')
        log_blue('[================================================================================================================]')

        # This outputs on stdout and returns 0 if success
        ping_output = subprocess.check_output(
            ["ping", "-c", "2", "172.90.0.122"]).decode('UTF-8')

        if ping_output.find('2 packets transmitted, 2 received') != -1:
            log_green(
                "Verify that the Ethernet driver is installed and working correctly: PASSED", tid)
        else:
            log_red(
                "Verify that the Ethernet driver is installed and working correctly: FAILED", tid)
            log_red("Unable to contact the device over Ethernet interface")

        ethtool = subprocess.check_output(
            ['sudo', 'ethtool', 'eno1']).decode('UTF-8')

        # alternate way to test if the ETH0 interface is up or down is following
        # cat /sys/class/net/eth0/operstate if the return is up/down  (reference platform)
        # cat /sys/class/net/eno1/operstate if the return is up/down  (ubuntu)
        # ip link show |grep eth0
        # dmesg | grep eth
        # cat /sys/class/net/eth0/carrier  or cat /sys/class/net/eno1/carrier returns 1 if up and 0 if down
        # ip a show eth0 up

        # os.system("")
        # os.system("echo %s" % sudopw)

        if ethtool.find('Link detected: yes') != -1:
            log_green("Verify that the Ethernet interface is UP: PASSED", tid)
        else:
            log_red("Verify that the Ethernet interface is UP: FAILED", tid)
            log_red("The Ethernet interface is not up: %s" % ethtool, tid)

        if ethtool.find('Speed: 1000Mb/s') != -1:
            log_green(
                "Verify that the Ethernet interface speed is 1000 Mbps: PASSED", tid)

        else:
            log_red(
                "Verify that the Ethernet interface speed is 1000 Mbps: FAILED", tid)
            log_red("The Ethernet interface speed is incorrect: %s" %
                    ethtool, tid)

        if ethtool.find('Duplex: Full') != -1:
            log_green(
                "Verify that the Ethernet interface is Full Duplex: PASSED", tid)
        else:
            log_red("Verify that the Ethernet interface is Full Duplex: FAILED", tid)
            log_red("The Ethernet interface is not Full duplex: %s" %
                    ethtool, tid)

        try:
            stdin, stdout, stderr = ssh.exec_command('ifconfig')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            ip = stdout.read().decode('UTF-8')

            if ip.find('inet addr:172.90.0.122') != -1:
                log_green(
                    "Verify that Ethernet interface has the correct IP address 172.90.0.122: PASSED", tid)
            else:
                log_red(
                    "Verify that Ethernet interface has the correct IP address 172.90.0.122: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_007_Routing(self):
        '''Verify that routing capabilities of the device'''
        tid = 'REFP_007'
        ssh = self.ssh  # handle

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print(
            '[Title                  ]: Verify that routing capabilities of the device')
        print('[Product Requirement    ]: EINST-031')
        print('[Development Task       ]: CONLAREINS-22')
        print('[Test Automation Task   ]: CONLAREINS-140')
        log_blue('[================================================================================================================]')

        try:
            stdin, stdout, stderr = ssh.exec_command('route')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            route = stdout.read().decode('UTF-8')

            if route.find("default         gateway         0.0.0.0         UG    0      0        0 eth0") != -1:
                log_green(
                    "Verify that default gateway is setup to eth0: PASSED", tid)
            else:
                log_red("Verify that default gateway is setup to eth0: FAILED", tid)

            if route.find("10.0.0.0        *               255.255.255.0   U     400    0        0 vlan100") != -1:
                log_green(
                    "Verify that routing table has 10.0.0.0 as vlan100: PASSED", tid)
            else:
                log_red("Verify that routing table has 10.0.0.0: FAILED", tid)

            if route.find('172.90.0.0    *               255.255.255.0   U     100    0        0 eth0') != -1:
                log_green(
                    "Verify that routing table has 172.90.0.0 has eth0: PASSED", tid)
            else:
                log_red(
                    "Verify that routing table has 172.90.0.0: has eth0: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_008_SMACK_Module(self):
        '''Verify that SMACK linux security module is implemented correctly on the device'''
        tid = 'REFP_008'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print(
            '[Title                  ]: Verify that routing capabilities of the device')
        print('[Product Requirement    ]: EINST-007')
        print('[Development Task       ]: CONLAREINS-12, CONLAREINS-13')
        print('[Test Automation Task   ]: CONLAREINS-118')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle

        try:
            stdin, stdout, stderr = ssh.exec_command('cat /smack/load2')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            smack = stdout.read().decode('UTF-8')
            # print(smack)

            # ===================================================================
            # if "_ syslog w" in smack:
            #     log_green("PASS")
            # else:
            #     log_red("FAIL")
            #
            # assert "_ syslog w" in smack
            # ===================================================================

            if smack.find("_ syslog rw") != -1:
                log_green(
                    "Verify that SMACK Rule '_ syslog w' is implemented and available: PASSED", tid)
            else:
                log_red(
                    "Verify that SMACK Rule '_ syslog w' is implemented and available: FAILED", tid)

            if smack.find("syslog _ w") != -1:
                log_green(
                    "Verify that SMACK Rule 'syslog _ w' is implemented and available: PASSED", tid)
            else:
                log_red(
                    "Verify that SMACK Rule 'syslog _ w' is implemented and available: FAILED", tid)

            if smack.find("admin framework w") != -1:
                log_green(
                    "Verify that SMACK Rule 'admin framework w' is implemented and available: PASSED", tid)
            else:
                log_red(
                    "Verify that SMACK Rule 'admin framework w' is implemented and available: FAILED", tid)

            if smack.find("framework admin w") != -1:
                log_green(
                    "Verify that SMACK Rule 'framework admin w' is implemented and available: PASSED", tid)
            else:
                log_red(
                    "Verify that SMACK Rule 'framework admin w' is implemented and available: FAILED", tid)

            if smack.find("admin _ rwx") != -1:
                log_green(
                    "Verify that SMACK Rule 'admin _ rwx' is implemented and available: PASSED", tid)
            else:
                log_red(
                    "Verify that SMACK Rule 'admin _ rwx' is implemented and available: FAILED", tid)

            if smack.find("framework _ rwx") == -1:
                log_green(
                    "Verify that SMACK Rule 'framework _ rwx' is implemented and available: PASSED", tid)
            else:
                log_red(
                    "Verify that SMACK Rule 'framework _ rwx' should not be listed: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_009_Monitor_Process(self):
        '''Verify the successful implementation, running and functionality of Monitor process'''
        tid = 'REFP_009'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation, running and functionality of Monitor process')
        print('[Product Requirement    ]: EINST-024')
        print('[Development Task       ]: CONLAREINS-43')
        print('[Test Automation Task   ]: CONLAREINS-159')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        #check if the monitor process is running
        output = runr(self, 'pidof monitor > /dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the Monitor process is successfully running: PASSED", tid)
        else:
            log_red("Verify that the Monitor process is successfully running: FAILED", tid)
        #check if monitor.log file exist
        output = runr(self, 'ls /var/log/monitor.log > /dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the monitor logs are being generated: PASSED", tid)
        else:
            log_red("Verify that the monitor logs are being generated: FAILED", tid)


        # check ping to SW
        output = run(self, 'ping -c 2 172.90.0.1', tid)
        if '2 packets transmitted, 2 packets received' in output:
            log_green("Verify that ping works from imx6 to SW Modem(172.90.0.1): PASSED", tid)
        else:
            log_red("Verify that ping works from imx6 to SW Modem(172.90.0.1): FAILED", tid)

        # check if cellular connection is up
        output = run(self, 'cell_shell isconnected', tid)
        if 'yes' in output:
            log_green("Verify that cellular connection is UP(cell_shell isconnected): PASSED", tid)
        else:
            log_red("Verify that cellular connection is UP(cell_shell isconnected): FAILED", tid)

        # check if cellular connection is up
        output = run(self, 'cell_shell getprofile', tid)
        output = output.replace("\n", "")
        # print(output)
        if 'sim:Ready' in output:
            log_green("Verify that SIM is present and ready: PASSED", tid)
        else:
            log_red("Verify that SIM is present and ready: FAILED", tid)

        # check if cellular connection is up
        output = run(self, 'ping -c 2 www.google.com', tid)
        if '2 packets transmitted, 2 packets received' in output:
            log_green("Verify that internet can be accessed over the cellular connection: PASSED", tid)
        else:
            log_red("Verify that internet can be accessed over the cellular connection: FAILED", tid)

        #check if there is connectivity to TRU manager server IP address
        output = runr(self, 'ping -c 2 52.2.59.234 >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that imx6 board can talk to TRU Manager ip address: PASSED", tid)
        else:
            log_red("Verify that imx6 board can talk to TRU Manager ip address:", tid)

        #check if there is connectivity to TRU manager server URL
        output = runr(self, 'ping -c 2 trumain-primary-ext.telematicsgateway.net >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that imx6 board can talk to TRU Manager URL: PASSED", tid)
        else:
            log_red("Verify that imx6 board can talk to TRU Manager URL:", tid)

        #check if monitor log contains steps to bring up the connection
        output = runr(self, 'cat /var/log/monitor.log | grep "Connecting" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that monitor process is attempting to establish cellular connection: PASSED", tid)
        else:
            log_red("Verify that monitor process is attempting to establish cellular connection: FAILED", tid)

        output = runr(self, 'cat /var/log/monitor.log | grep "Response to connect: OK" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that monitor process go response to connect cellular connection: PASSED", tid)
        else:
            log_red("Verify that monitor process go response to connect cellular connection: FAILED", tid)

        output = runr(self, 'cat /var/log/monitor.log | grep "profile:sim:Ready,iccid:" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that SIM is ready: PASSED", tid)
        else:
            log_red("Verify that SIM is ready: FAILED", tid)

        output = runr(self, 'cat /var/log/monitor.log | grep "Connection established" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that monitor process has established good cellular connection: PASSED", tid)
        else:
            log_red("Verify that monitor process has established good cellular connection: FAILED", tid)

        output = runr(self, 'cat /var/log/monitor.log | grep "Entering upLoop" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that monitor process has started the upLoop: PASSED", tid)
        else:
            log_red("Verify that monitor process has started the upLoop: FAILED", tid)

        output = runr(self, 'cat /var/log/monitor.log | grep "Attempting to connect to cell_talker" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that monitor process is attempting to connect to cell_talker process: PASSED", tid)
        else:
            log_red("Verify that monitor process is attempting to connect to cell_talker process: FAILED", tid)

        output = runr(self, 'cat /var/log/monitor.log | grep "Connected to cell_talker" >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that monitor process has connected to cell_talker: PASSED", tid)
        else:
            log_red("Verify that monitor process has connected to cell_talker: FAILED", tid)


    def test_REFP_010_Unitcomm_Process(self):
        '''Verify the successful implementation, running and functionality of Unitcomm process'''
        tid = 'REFP_010'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation, running and functionality of Unitcomm process')
        print('[Product Requirement    ]: EINST-023')
        print('[Development Task       ]: CONLAREINS-42')
        print('[Test Automation Task   ]: CONLAREINS-158')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        #check if the unitcomm process is running
        output = runr(self, 'pidof unitcomm > /dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the Unitcomm process is successfully running: PASSED", tid)
        else:
            log_red("Verify that the Unitcomm process is successfully running: FAILED", tid)
        #check if unitcomm.log file exist
        output = runr(self, 'ls /var/log/unitcomm.log > /dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the Unitcomm logs are being generated: PASSED", tid)
        else:
            log_red("Verify that the Unitcomm logs are being generated: FAILED", tid)

        #check if hostname in unitcomm.log and outside is same
        output = runr(self, 'hostname', tid)
        host = output[9:]
        output = runr(self, 'cat /var/log/unitcomm.log |grep Hostname')
        if host in output:
            log_green("Verify that the hostname in unitcomm.log and Unit Id is same: PASSED", tid)
        else:
            log_red("Verify that the hostname in unitcomm.log and Unit Id is same: FAILED", tid)
        #check if server ip address is valid in unitcomm
        output = runr(self, 'cat /var/log/unitcomm.log')
        if "ServerIP: 52.2.59.234" in output:
            log_green("Verify that the TRU Manager ip address is correct in unitcomm.log: PASSED", tid)
        else:
            log_red("Verify that the TRU Manager ip  address is correct in unitcomm.log:", tid)
        #check if WAN interface is up in unitcomm
        output = runr(self, 'cat /var/log/unitcomm.log')
        if "WAN up" in output:
            log_green("Verify that WAN interface is up in unitcomm.log: PASSED", tid)
        else:
            log_red("Verify that WAN interface is up in unitcomm.log:", tid)

        #check if there is connectivity to TRU manager server IP address
        output = runr(self, 'ping -c 2 52.2.59.234 >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that imx6 board can talk to TRU Manager ip address: PASSED", tid)
        else:
            log_red("Verify that imx6 board can talk to TRU Manager ip address:", tid)

        #check if there is connectivity to TRU manager server URL
        output = runr(self, 'ping -c 2 trumain-primary-ext.telematicsgateway.net >/dev/null; echo $?')
        if output == '0':
            log_green("Verify that imx6 board can talk to TRU Manager URL: PASSED", tid)
        else:
            log_red("Verify that imx6 board can talk to TRU Manager URL:", tid)


    def test_REFP_011_Celltalker_Process(self):
        '''Verify the successful implementation, running and functionality of Celltalker process'''
        tid = 'REFP_011'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation and functionality of Celltalker/SW Talker process')
        print('[Product Requirement    ]: EINST-025')
        print('[Development Task       ]: CONLAREINS-44')
        print('[Test Automation Task   ]: CONLAREINS-160')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        output = runr(self, 'ssh -o "StrictHostKeyChecking=no" root@172.90.0.1 "hostname" 2>/dev/null', tid)
        #here the warning and error code(the result output of exec_command) is directed to null, 1 is the output and 2 is error message and $? is exit code. they can be redirected to files
        if 'swi-mdm9x40' in output:
            output = runr(self, 'pidof sw_talker-eth > /dev/null; echo $?', tid)
            if output == '0':
                log_green( "Verify that the sw_talker-eth process is successfully running: PASSED", tid)
            else:
                log_red( "Verify that the sw_talker-eth process is successfully running: FAILED", tid)
        else:
            output = runr(self, 'pidof cell_talker > /dev/null; echo $?', tid)
            if output == '0':
                log_green( "Verify that the cell_talker process is successfully running: PASSED", tid)
            else:
                log_red( "Verify that the cell_talker process is successfully running: FAILED", tid)

    def test_REFP_012_LocationManager_Process(self):
        '''Verify the successful implementation, running and functionality of LocationManager process'''
        tid = 'REFP_012'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation, and functionality of LocationManager process')
        print('[Product Requirement    ]: EINST-022')
        print('[Development Task       ]: CONLAREINS-41')
        print('[Test Automation Task   ]: CONLAREINS-157')
        log_blue('[================================================================================================================]')
        #TBD
        ssh = self.ssh  # handle
        # check if the respawner stared the gps_mon-eth and its logs
        output = runr(self, 'cat  /var/log/respawner.log | grep "/usr/local/bin/gps_mon-eth -e" >/dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the respawner process actually started the location manager: PASSED", tid)
        else:
            log_red("Verify that the respawner process actually started the location manager: FAILED", tid)

        output = runr(self, 'cat  /var/log/respawner.log | grep "/var/log/gps_mon-eth.log" >/dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the respawner process started capturing location manager logs: PASSED", tid)
        else:
            log_red("Verify that the respawner process started capturing location manager logs: FAILED", tid)

        output = runr(self, 'pidof gps_mon-eth > /dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the Location Manager process is successfully running: PASSED", tid)
        else:
            log_red("Verify that the Location Manager process is successfully running: FAILED", tid)

        output = runr(self, 'cat  /var/log/gps_mon-eth.log | grep "einstein" >/dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the Location Manager logs have correct hostname: PASSED", tid)
        else:
            log_red("Verify that the Location Manager logs have correct hostname: FAILED", tid)

        output = runr(self, 'cat  /var/log/gps_mon-eth.log | grep "Opened eth socket" >/dev/null; echo $?', tid)
        if output == '0':
            log_green("Verify that the Location Manager logs have opened eth socket: PASSED", tid)
        else:
            log_red("Verify that the Location Manager logs have opened eth socket: FAILED", tid)

        # check for /tmp files
        output = runr(self, 'ls /tmp/gps_present 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth has detected a GPS Source: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth has detected a GPS Source: FAILED", tid)

        output = runr(self, 'find /tmp/gps_time 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth has obtained time from the GPS: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth has obtained time from the GPS: FAILED", tid)

        output = runr(self, 'find /tmp/gps_position 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth has obtained current location the GPS: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth has obtained current location the GPS: FAILED", tid)

        output = runr(self, 'find /tmp/gps_speed 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth has obtained current speed from the GPS: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth has obtained current speed from the GPS: FAILED", tid)

        output = runr(self, 'find /tmp/no_gps_time 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth is unable to obtain time from GPS: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth is unable to obtain time from GPS: FAILED", tid)

        output = runr(self, 'find /tmp/no_gps_position 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth is unable to obtain position from GPS: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth is unable to obtain position from GPS: FAILED", tid)

        output = runr(self, 'find /tmp/gps_last_position 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the gps_mon-eth contains last known position and GPS position unavailable: PASSED", tid)
        else:
            log_red("Verify that the gps_mon-eth contains last known position and GPS position unavailable: FAILED", tid)

        output = runr(self, 'find /tmp/gps_num_stats 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the number of satellites are available to get the fix: PASSED", tid)
        else:
            log_red("Verify that the number of satellites are available to get the fix: FAILED", tid)

        output = runr(self, 'find /autonet/admin/previous_position 1>/dev/null 2>&1; echo $?', tid)
        if output == '0':
            log_green("Verify that the last position saved across the power cycle is available: PASSED", tid)
        else:
            log_red("Verify that the last position saved across the power cycle is available: FAILED", tid)


    def test_REFP_013_Event_Logger_Process(self):
        '''Verify the successful implementation, running and functionality of EventLogger process'''
        tid = 'REFP_013'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation, and functionality of EventLogger process')
        print('[Product Requirement    ]: EINST-057')
        print('[Development Task       ]: CONLAREINS-419')
        print('[Test Automation Task   ]: CONLAREINS-443')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        # TBD
        try:
            stdin, stdout, stderr = ssh.exec_command(
                'pidof event_logger > /dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            Event_Logger = stdout.read().decode('UTF-8').replace("\n", "")

            if Event_Logger == '0':
                log_green(
                    "Verify that the EventLogger process is successfully running: PASSED", tid)
            else:
                log_red(
                    "Verify that the EventLogger process is successfully running: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_014_Config_Manager_Process(self):
        '''Verify the successful implementation, running and functionality of ConfigManager process'''
        tid = 'REFP_014'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation, and functionality of ConfigManager process')
        print('[Product Requirement    ]: EINST-026')
        print('[Development Task       ]: CONLAREINS-131')
        print('[Test Automation Task   ]: CONLAREINS-233')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        output = runr(self, 'pidof config_manager > /dev/null; echo $?', tid)
        if output == '0':
                log_green("Verify that the ConfigManager process is successfully running: PASSED", tid)
        else:
                log_red("Verify that the ConfigManager process is successfully running: FAILED", tid)

        autonet_conf = runr(self, 'cat /autonet/etc/autonet.conf >/dev/null; echo $?', tid)
        if output == '0':
                log_green("Verify that the autonet.conf file exist in /autonet/etc folder: PASSED", tid)

                autonet_conf = run(self, 'cat /autonet/etc/autonet.conf', tid)
                config_test = run(self, '/autonet/tests/config-manager/config_test 127.0.0.1', tid)

                if "unit.v1-servers trumain-primary-ext.telematicsgateway.net trumain-secondary-ext.telematicsgateway.net" in autonet_conf and "unit.v1-servers,trumain-primary-ext.telematicsgateway.net trumain-secondary-ext.telematicsgateway.net" in config_test:
                    log_green("Verify that the v1-servers with correct keys exist in autonet.conf and config_test: PASSED", tid)
                else:
                    log_green("Verify that the v1-servers with correct keys exist in autonet.conf and config_test: FAILED", tid)

                if "unit.server-port 5151" in autonet_conf and "unit.server-port,5151" in config_test:
                    log_green("Verify that the unit.server-port with correct keys exist in autonet.conf and config_test: PASSED", tid)
                else:
                    log_green("Verify that the unit.server-port with correct keys exist in autonet.conf and config_test: FAILED", tid)

                if "unit.listen-port 5150" in autonet_conf and "unit.listen-port,5150" in config_test:
                    log_green("Verify that the unit.listen-port with correct keys exist in autonet.conf and config_test: PASSED", tid)
                else:
                    log_green("Verify that the unit.listen-port with correct keys exist in autonet.conf and config_test: FAILED", tid)

                if "unit.localdir ." in autonet_conf and "unit.localdir,." in config_test:
                    log_green("Verify that the unit.localdir with correct keys exist in autonet.conf and config_test: PASSED", tid)
                else:
                    log_green("Verify that the unit.localdir with correct keys exist in autonet.conf and config_test: FAILED", tid)

                if "unit.speedtest-server speedtest.telematicsgateway.net" in autonet_conf and "unit.speedtest-server,speedtest.telematicsgateway.net" in config_test:
                    log_green("Verify that the unit.speedtest-server with correct keys exist in autonet.conf and config_test: PASSED", tid)
                else:
                    log_green("Verify that the unit.speedtest-server with correct keys exist in autonet.conf and config_test: FAILED", tid)

                if "unit.update-servers update.telematicsgateway.net" in autonet_conf and "unit.update-servers,update.telematicsgateway.net" in config_test:
                    log_green("Verify that the unit.update-servers with correct keys exist in autonet.conf and config_test: PASSED", tid)
                else:
                    log_green("Verify that the unit.update-servers with correct keys exist in autonet.conf and config_test: FAILED", tid)
        else:
                log_red("Verify that the autonet.conf file exist in /autonet/etc folder: FAILED", tid)


    def test_REFP_015_Vehicle_Abstraction_Process(self):
        '''Verify the successful implementation, running and functionality of Vehicle Abstraction process'''
        tid = 'REFP_015'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation and functionality of Vehicle Abstraction process')
        print('[Product Requirement    ]: EINST-028')
        print('[Development Task       ]: CONLAREINS-54')
        print('[Test Automation Task   ]: CONLAREINS-170')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        # TBD
        # Check the Ethernet Interface on the board
        try:
            stdin, stdout, stderr = ssh.exec_command(
                'pidof va > /dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            Vehicle_Abstraction = stdout.read().decode('UTF-8').replace("\n", "")

            if Vehicle_Abstraction == '0':
                log_green(
                    "Verify that the Vehicle Abstraction process is successfully running: PASSED", tid)
            else:
                log_red(
                    "Verify that the Vehicle Abstraction process is successfully running: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_016_rootfs_mods_implementation(self):
        '''Verify the successful implementation of re-design of rootfs_mods'''
        tid = 'REFP_016'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation of re-design of rootfs_mods')
        print('[Product Requirement    ]: EINST-001')
        print('[Development Task       ]: CONLAREINS-81')
        print('[Test Automation Task   ]: CONLAREINS-192')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle

        # Check the Ethernet Interface on the board
        try:

            stdin, stdout, stderr = ssh.exec_command(
                '%s/rootfsmods/test_rootfsmods > /dev/null; echo $?' % test_dir)
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    "error in executing the test command encountered" + result + ": FAILED", tid)

            rootfs_mods = stdout.read().decode('UTF-8').replace("\n", "")

            if rootfs_mods == '0':
                log_green(
                    "Verify that the re-design of rootfs_mods is implemented correctly: PASSED", tid)
            else:
                log_red(
                    "Verify that the re-design of rootfs_mods is implemented correctly: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_017_file_system_structure(self):
        '''Verify the design of file system structure'''
        tid = 'REFP_017'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the design of file system structure')
        print('[Product Requirement    ]: EINST-021, EINST-004')
        print('[Development Task       ]: CONLAREINS-67, CONLAREINS-34, CONLAREINS-253')
        print('[Test Automation Task   ]: CONLAREINS-183, CONLAREINS-283')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle

        try:

            stdin, stdout, stderr = ssh.exec_command('mount')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    "error in executing the test command encountered" + result + ": FAILED", tid)

            file_structure = stdout.read().decode('UTF-8')
            # print(file_structure)

            # Testing "/"
            if "/dev/mmcblk2p5 on / type ext4 (ro,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that the file structure has "/dev/mmcblk2p5" mounted correctly: PASSED', tid)
            else:
                log_red(
                    'Verify that the file structure has "/dev/mmcblk2p5" mounted correctly: FAILED', tid)

            if "/dev/mmcblk2p5" in file_structure:
                log_green(
                    'Verify that file system "/" is NOT encrypted: PASSED', tid)
            else:
                log_red('Verify that file system "/" is encrypted: FAILED', tid)

            if "/dev/mmcblk2p5 on / type ext4" in file_structure:
                log_green(
                    'Verify that "/" is ext4 type file structure: PASSED', tid)
            else:
                log_red('Verify that "/" is ext4 type file structure: FAILED', tid)

            if "/dev/mmcblk2p5 on / type ext4 (ro,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that "/" is read-only file structure: PASSED', tid)
            else:
                log_red('Verify that "/" is read-only file structure: FAILED', tid)

            stdin, stdout, stderr = ssh.exec_command('touch /test')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_green(
                    'Verify that "/" is Read Only type file structure: PASSED', tid)
                # log_red("error in executing the test command encountered" + result + ": FAILED", tid)
            else:
                log_red(
                    'Verify that "/" is Read Only type file structure: FAILED', tid)
                stdin, stdout, stderr = ssh.exec_command('rm /test')

            # Testing "/proprietary"
            if "/dev/mapper/proprietary on /proprietary type ext4 (ro,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that the file structure has "/proprietary" mounted correctly: PASSED', tid)
            else:
                log_red(
                    'Verify that the file structure has "/proprietary" mounted correctly: FAILED', tid)

            if "/dev/mapper/proprietary" in file_structure:
                log_green('Verify that "/proprietary" is encrypted: PASSED', tid)
            else:
                log_red('Verify that "/proprietary" is encrypted: FAILED', tid)

            if "/proprietary type ext4" in file_structure:
                log_green(
                    'Verify that "/proprietary" is ext4 type file structure: PASSED', tid)
            else:
                log_red(
                    'Verify that "/proprietary" is ext4 type file structure: FAILED', tid)

            stdin, stdout, stderr = ssh.exec_command('touch /proprietary/test')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_green(
                    'Verify that "/proprietary" is Read Only type file structure: PASSED', tid)
                # log_red("error in executing the test command encountered" + result + ": FAILED", tid)
            else:
                log_red(
                    'Verify that "/proprietary" is Read Only type file structure: FAILED', tid)
                stdin, stdout, stderr = ssh.exec_command(
                    'rm /proprietary/test')

            # Testing "/autonet"
            if "/dev/mapper/autonet on /autonet type ext4 (rw,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that the file structure has "/autonet" mounted correctly: PASSED', tid)
            else:
                log_red(
                    'Verify that the file structure has "/autonet" mounted correctly: FAILED', tid)

            if "/dev/mapper/autonet" in file_structure:
                log_green('Verify that "/autonet" is encrypted: PASSED', tid)
            else:
                log_red('Verify that "/autonet" is encrypted: FAILED', tid)

            if "/autonet type ext4" in file_structure:
                log_green(
                    'Verify that "/autonet" is ext4 type file structure: PASSED', tid)
            else:
                log_red(
                    'Verify that "/autonet" is ext4 type file structure: FAILED', tid)

            stdin, stdout, stderr = ssh.exec_command('touch /autonet/test')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that "/autonet" is Read/Write type file structure: FAILED', tid)
            else:
                log_green(
                    'Verify that "/autonet" is Read/Write type file structure: PASSED', tid)
                stdin, stdout, stderr = ssh.exec_command('rm /autonet/test')
                # log_red("error in executing the test command encountered" + result + ": FAILED", tid)

            # Testing "/user"
            if "/dev/mapper/user on /user type ext4 (rw,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that the file structure has "/user" mounted correctly: PASSED', tid)
            else:
                log_red(
                    'Verify that the file structure has "/user" mounted correctly: FAILED', tid)

            if "/dev/mapper/user" in file_structure:
                log_green('Verify that "/user" is encrypted: PASSED', tid)
            else:
                log_red('Verify that "/user" is encrypted: FAILED', tid)

            if "/user type ext4" in file_structure:
                log_green(
                    'Verify that "/user" is ext4 type file structure: PASSED', tid)
            else:
                log_red(
                    'Verify that "/user" is ext4 type file structure: FAILED', tid)

            stdin, stdout, stderr = ssh.exec_command('touch /user/test')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that "/user" is Read/Write type file structure: FAILED', tid)
            else:
                log_green(
                    'Verify that "/user" is Read/Write type file structure: PASSED', tid)
                stdin, stdout, stderr = ssh.exec_command('rm /user/test')
                # log_red("error in executing the test command encountered" + result + ": FAILED", tid)

            # Testing "/tmp"
            if "tmpfs on /tmp type tmpfs (rw,relatime)" in file_structure:
                log_green(
                    'Verify that the file structure has "/tmp" mounted correctly: PASSED', tid)
            else:
                log_red(
                    'Verify that the file structure has "/tmp" mounted correctly: FAILED', tid)

            if "tmpfs on /tmp" in file_structure:
                log_green('Verify that "/tmp" is NOT encrypted: PASSED', tid)
            else:
                log_red('Verify that "/tmp" is encrypted: FAILED', tid)

            if "/tmp type tmpfs" in file_structure:
                log_green(
                    'Verify that "/tmp" is tmpfs type file structure: PASSED', tid)
            else:
                log_red(
                    'Verify that "/tmp" is tmpfs type file structure: FAILED', tid)

            stdin, stdout, stderr = ssh.exec_command('touch /tmp/test')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that "/tmp" is Read/Write type file structure: FAILED', tid)
            else:
                log_green(
                    'Verify that "/tmp" is Read/Write type file structure: PASSED', tid)
                stdin, stdout, stderr = ssh.exec_command('rm /tmp/test')

            # cryptsetup to check if password is required to mount the partitions
            stdin, stdout, stderr = ssh.exec_command(
                'echo wrongpw|cryptsetup open --type luks /dev/mmcblk2p11 test --tries=1')
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if "No key available with this passphrase" not in result:
                log_red(
                    'Verify that a password is required to mount a device(/dev/mmcblk2p11) using cryptsetup: FAILED', tid)
            else:
                log_green(
                    'Verify that a password is required to mount a device(/dev/mmcblk2p11) using cryptsetup: PASSED', tid)

            # cryptsetup to check if password is required to mount the partitions: successful
            stdin, stdout, stderr = ssh.exec_command(
                'echo connexus|cryptsetup open --type luks /dev/mmcblk2p11 test --tries=1')
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that a device(/dev/mmcblk2p11) can be mounted if correct password used: FAILED', tid)
            else:
                log_green(
                    'Verify that a device(/dev/mmcblk2p11) can be mounted if correct password used: PASSED', tid)

            # Check if device is active using cyptsetup: successful
            stdin, stdout, stderr = ssh.exec_command('cryptsetup status test')
            output = stdout.read().decode('UTF-8').replace("\n", "")
            if "/dev/mapper/test is active" not in output:
                log_red(
                    'Verify that a device(/dev/mmcblk2p11) is active to be mounted using cryptsetup: FAILED', tid)
            else:
                log_green(
                    'Verify that a device(/dev/mmcblk2p11) is active to be mounted using cryptsetup: PASSED', tid)

            # Check /tmp/test directory is created: successful
            stdin, stdout, stderr = ssh.exec_command('mkdir /tmp/test')
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that the creation of directory /tmp/test is successful: FAILED', tid)
            else:
                log_green(
                    'Verify that the creation of directory /tmp/test is successful: PASSED', tid)

            # Check if /tmp/test can be mounted successfully: successful
            stdin, stdout, stderr = ssh.exec_command(
                'mount /dev/mapper/test /tmp/test')
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that the /tmp/test can be mounted /dev/mapper/test successfully: FAILED', tid)
            else:
                log_green(
                    'Verify that the /tmp/test can be mounted /dev/mapper/test successfully: PASSED', tid)

            # Check if /tmp/test has all the essential files: successful
            stdin, stdout, stderr = ssh.exec_command('ls /tmp/test/etc')
            result = stderr.read().decode('UTF-8').replace("\n", "")
            output = stdout.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red('Verify that a /tmp/test/etc exist: FAILED', tid)
            else:
                if "local_features" and "features" and "autonet.conf" in output:
                    log_green(
                        'Verify that the /tmp/test/etc has essential files present: PASSED', tid)
                else:
                    log_red(
                        'Verify that the /tmp/test/etc has essential files present: FAILED', tid)

            # Check if /tmp/test can be unmounted successfully: successful
            stdin, stdout, stderr = ssh.exec_command('umount /tmp/test')
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    'Verify that a /tmp/test can be unmounted /dev/mapper/test successfully: FAILED', tid)
            else:
                log_green(
                    'Verify that a /tmp/test can be unmounted /dev/mapper/test successfully: PASSED', tid)

            # cryptsetup to check if password is required to close the partitions: successful
            stdin, stdout, stderr = ssh.exec_command('cryptsetup close test')
            result = stderr.read().decode('UTF-8').replace("\n", "")

            if len(result) > 0:
                log_red(
                    'Verify that a device(/dev/mmcblk2p11) can be closed successfully using cryptsetup: FAILED', tid)
            else:
                log_green(
                    'Verify that a device(/dev/mmcblk2p11) can be closed successfully using cryptsetup: PASSED', tid)
                stdin, stdout, stderr = ssh.exec_command('rmdir /tmp/test')
                result = stderr.read().decode('UTF-8').replace("\n", "")
                if len(result) > 0:
                    log_red(
                        'Verify that the /tmp/test is deleted successfully: FAILED', tid)
                else:
                    log_green(
                        'Verify that the /tmp/test is deleted successfully: PASSED', tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_018_Respawner_Process(self):
        '''Verify the successful implementation, running and functionality of Respawner process'''
        tid = 'REFP_018'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify the successful implementation and functionality of Respawner process')
        print('[Product Requirement    ]: EINS-41')
        print('[Development Task       ]: CONLAREINS-403')
        print('[Test Automation Task   ]: CONLAREINS-427')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle

        # TBD
        try:
            stdin, stdout, stderr = ssh.exec_command(
                'pidof respawner > /dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("error in executing the command encountered" +
                        result + ": FAILED", tid)

            Respawner = stdout.read().decode('UTF-8').replace("\n", "")

            if Respawner == '0':
                log_green(
                    "Verify that the Respawner process is successfully running: PASSED", tid)
            else:
                log_red(
                    "Verify that the Respawner process is successfully running: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_019_dm_verity(self):
        '''Verify the design of file system structure'''
        tid = 'REFP_019'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print(
            '[Title                  ]: Verify the implementation of dm-verity feature')
        print('[Product Requirement    ]: EINST-018')
        print('[Development Task       ]: CONLAREINS-95')
        print('[Test Automation Task   ]: CONLAREINS-206')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle

        try:
            stdin, stdout, stderr = ssh.exec_command('mount')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red(
                    "error in executing the test command encountered" + result + ": FAILED", tid)

            file_structure = stdout.read().decode('UTF-8')
            # print(file_structure)

            # Testing "/"
            if "/dev/dm-0 on / type ext4 (ro,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that the root partition is mounted as "/dev/dm-0" to support dm-verity: PASSED', tid)
            else:
                log_red(
                    'Verify that the root partition is mounted as "/dev/dm-0" to support dm-verity: FAILED', tid)

            if "/dev/dm-0" in file_structure:
                log_green(
                    'Verify that root partition "/" is NOT encrypted: PASSED', tid)
            else:
                log_red('Verify that root partition "/" is encrypted: FAILED', tid)

            if "/dev/dm-0 on / type ext4" in file_structure:
                log_green(
                    'Verify that the root partition "/" is ext4 type file structure: PASSED', tid)
            else:
                log_red(
                    'Verify that the root partition"/" is ext4 type file structure: FAILED', tid)

            if "/dev/dm-0 on / type ext4 (ro,relatime,data=ordered)" in file_structure:
                log_green(
                    'Verify that the root partition "/" is Read-Only type file structure: PASSED', tid)
            else:
                log_red(
                    'Verify that the root partition"/" is Read-Only type file structure: FAILED', tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_020_OS_Linux_Hardened(self):
        '''Verify if the OS(Linux) is hardened'''
        tid = 'REFP_020'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify if the OS(Linux) has hardened design')
        print('[Product Requirement    ]: EINST-015, EINST-016, EINST-017, EINST-018, EINST-005, EINST-006')
        print('[Development Task       ]: CONLAREINS-9, CONLAREINS-11')
        print('[Test Automation Task   ]: CONLAREINS-117')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        # poison positive
        try:
            stdin, stdout, stderr = ssh.exec_command('/autonet/tests/poison/test_page_poison >/dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("An error in executing the test command encountered" + result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")
            # print(output)
            if output == '0':
                log_green(
                    "Verify that the Poison positive test works: PASSED", tid)
            else:
                log_red(
                    "Verify that the Poison positive test works: PASSED: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # fortify positive
        try:
            stdin, stdout, stderr = ssh.exec_command('/autonet/tests/fortify/test_fortify 1 >/dev/null 2>&1; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("An error in executing the test command encountered" + result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")
            # print(output)
            if output == '0':
                log_green(
                    "Verify that the Fortify positive test works: PASSED", tid)
            else:
                log_red(
                    "Verify that the Fortify positive test works: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

        # fortify negative
        try:
            stdin, stdout, stderr = ssh.exec_command('/autonet/tests/fortify 111111 >/dev/null 2>&1; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("An error in executing the test command encountered" + result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")
            # print(output)
            if output != '0':
                log_green(
                    "Verify that the Fortify negative test works: PASSED", tid)
            else:
                log_red(
                    "Verify that the Fortify negative test works: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

    def test_REFP_021_Legato(self):
        '''Verify if Legato is installed and running successfully'''
        tid = 'REFP_021'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify if Legato is installed and running successfully')
        print('[Product Requirement    ]: EINST-008')
        print('[Development Task       ]: CONLAREINS-19')
        print('[Test Automation Task   ]: CONLAREINS-137')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        # legato running
        try:
            stdin, stdout, stderr = ssh.exec_command('pidof supervisor > /dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("An error in executing the test command encountered" + result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")
            # print(output)
            if output == '0':
                log_green(
                    "Verify that the Legato (supervisor) is running successfully: PASSED", tid)
            else:
                log_red(
                    "Verify that the Legato (supervisor) is running successfully: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)
        # legato file structure
        try:
            stdin, stdout, stderr = ssh.exec_command('mount | grep "legato" > /dev/null; echo $?')
            # check if there is any error in issuing the command
            result = stderr.read().decode('UTF-8').replace("\n", "")
            if len(result) > 0:
                log_red("An error in executing the test command encountered" + result + ": FAILED", tid)

            output = stdout.read().decode('UTF-8').replace("\n", "")
            # print(output)
            if output == '0':
                log_green(
                    "Verify that the Legato file structure is mounted: PASSED", tid)
            else:
                log_red(
                    "Verify that the Legato file structure is mounted: FAILED", tid)

        except Exception as e:
            log_red("Operation error:" + str(e) + ": FAILED", tid)

# using run function this point on
    def test_REFP_022_Sierra_Wirless_eCall(self):
        '''Verify if eCall Functionality works on Sierra Wireless NAD'''
        tid = 'REFP_022'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify if eCall Functionality works on Sierra Wireless NAD')
        print('[Product Requirement    ]: None')
        print('[Development Task       ]: CONLAREINS-50')
        print('[Test Automation Task   ]: CONLAREINS-166')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle

        # check ping to SW
        output = run(self, 'ping -c 2 172.90.0.1', tid)
        if '2 packets transmitted, 2 packets received' in output:
            log_green("Verify that ping works from imx6 to SW (172.90.0.1): PASSED", tid)
        else:
            log_red("Verify that ping works from imx6 to SW (172.90.0.1): FAILED", tid)

        # check if cellular connection is up
        output = run(self, 'cell_shell isconnected', tid)
        if 'yes' in output:
            log_green("Verify that cellular connection is UP(cell_shell isconnected): PASSED", tid)
        else:
            log_red("Verify that cellular connection is UP(cell_shell isconnected): FAILED", tid)

        # check if cellular connection is up
        output = run(self, 'cell_shell getprofile', tid)
        output = output.replace("\n", "")
        # print(output)
        if 'sim:Ready' in output:
            log_green("Verify that SIM is present and ready: PASSED", tid)
        else:
            log_red("Verify that SIM is present and ready: FAILED", tid)

        if 'provider:AT&T' in output:
            log_green("Verify that cellular service provider exist and is ATT&T: PASSED", tid)
        else:
            log_red("Verify that cellular service provider exist and is ATT&T: FAILED", tid)

        if 'mdn:provider' in output:
            log_red("Verify that MDN exist: FAILED", tid)
        else:
            log_green("Verify that MDN exist: PASSED", tid)

        # check if cellular connection is up
        output = run(self, 'ping -c 2 www.google.com', tid)
        if '2 packets transmitted, 2 packets received' in output:
            log_green("Verify that internet can be accessed over the cellular connection: PASSED", tid)
            output = run(self, 'cell_shell "ecall TEST +33141081040 2C3CDXCT8FH915638 VEHICLE_PASSENGER_M1 TYPE_GASOLINE 2"', tid)
            if 'OK' in output:
                log_green("Verify that eCall test call could be successfully placed: PASSED", tid)
            else:
                log_red("Verify that eCall test call could be successfully placed: FAILED", tid)
        else:
            log_red("Verify that internet can be accessed over the cellular connection: FAILED", tid)

    def test_REFP_023_add_files_to_boot(self):
        '''Verify if some mandatory files are added to /boot'''
        tid = 'REFP_023'

        print('[Test Case ID           ]: %s' % tid)
        print('[Test Case Name         ]: %s' % inspect.stack()[0].function)
        print('[Title                  ]: Verify if some mandatory files are added to /boot')
        print('[Product Requirement    ]: EINST_001')
        print('[Development Task       ]: CONLAREINS-80')
        print('[Test Automation Task   ]: CONLAREINS-191')
        log_blue('[================================================================================================================]')

        ssh = self.ssh  # handle
        output = runr(self, '[[ -r /boot/zImage ]]; echo $?', tid)
        if output == '0':
            log_green("Verify that file 'zImage' exist in /boot: PASSED", tid)
        else:
            log_red("Verify that file 'zImage' exist in /boot: FAILED", tid)

        output = runr(self, '[[ -r /boot/u-boot.imx ]]; echo $?', tid)
        if output == '0':
            log_green("Verify that file 'u-boot.imx' exist in /boot: PASSED", tid)
        else:
            log_red("Verify that file 'u-boot.imx' exist in /boot: FAILED", tid)

        output = runr(self, '[[ -r /boot/zImage-imx6qp-sabreauto.dtb ]]; echo $?', tid)
        if output == '0':
            log_green("Verify that file 'zImage-imx6qp-sabreauto.dtb' exist in /boot: PASSED", tid)
        else:
            log_red("Verify that file 'zImage-imx6qp-sabreauto.dtb' exist in /boot: FAILED", tid)

'''
# example of using the run function
        output = run(self, 'pwd', tid)
        if output == '/root':
            print('pass')
        else:
            print('fail')
'''

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main(exit=False)
    REFP_1000_test_stats()
