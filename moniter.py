from __future__ import print_function
import platform
import os
import psutil
import time
#print("\nServer hook script is running ")
#UI=input("\nIf you want get Remote server information enter 'REMOTE' \nif you want to get local machine information enter 'LOCAL'\n:")
#print(UI)

print("==============================================================================")
print("#####################SYSTEM INFORMATIONS######################################")
print("==============================================================================")
print("Architecture : " + platform.architecture()[0])
print("Machine      : " + platform.machine())
print("Hostname     : " + platform.node())
print("system       : " + platform.system())
dist = platform.dist()
dist = " ".join(x for x in dist)
print("Distribution : " + dist)
print("==============================================================================")
# processor
def processinfo():
        cpu_count = psutil.cpu_count()
        print("Total CPU count :" +str(cpu_count))
        print("\nProcessors: ")
        with open("/proc/cpuinfo", "r")  as f:
            info = f.readlines()

        cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
        for index, item in enumerate(cpuinfo):
            print("    " + str(index) + ": " + item)
processinfo()

print("==============================================================================")

memory_stats = psutil.virtual_memory()
memory_total = memory_stats.total
memory_used = memory_stats.used
memory_used_percent = memory_stats.percent
print("Memory:\n\tPercent:", memory_used_percent, "\n\tTotal:", memory_total / 1e+6, "MB", "\n\tUsed:", memory_used / 1e+6, "MB")
# Disk Info
disk_info = psutil.disk_partitions()
print("Disks:")
disks = []
for x in disk_info:
    # Try fixes issues with connected 'disk' such as CD-ROMS, Phones, etc.
    try:
        disk = {
            "name" : x.device,
            "mount_point" : x.mountpoint,
            "type" : x.fstype,
            "total_size" : psutil.disk_usage(x.mountpoint).total,
            "used_size" : psutil.disk_usage(x.mountpoint).used,
            "percent_used" : psutil.disk_usage(x.mountpoint).percent
        }

        disks.append(disk)

        print("Disk name: ",disk["name"], " \n  Mount Point:", disk["mount_point"], " \n  Type",disk["type"], " \n  Size:", disk["total_size"] / 1e+9,"   \n  Usage:", disk["used_size"] / 1e+9, "  \n  Percent Used:", disk["percent_used"])
    except:
        print("")
print("==============================================================================")


# uptime
uptime = None
with open("/proc/uptime", "r") as f:
    uptime = f.read().split(" ")[0].strip()
uptime = int(float(uptime))
uptime_hours = uptime // 3600
uptime_minutes = (uptime % 3600) // 60
print(" ")
print("Uptime: " + str(uptime_hours) + ":" + str(uptime_minutes) + " hours")

print("==============================================================================")

def get_bandwidth():
    # Get net in/out
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv
    #print(net1_out)
    #print(net1_in)
    time.sleep(1)

    # Get new net in/out
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv

    #print(net2_out)
    #print(net2_in)

    # Compare and get current speed
    if net1_in > net2_in:
        current_in = 0
    else:
        current_in = net2_in - net1_in

    if net1_out > net2_out:
        current_out = 0
    else:
        current_out = net2_out - net1_out
    print("Network Usage Status :")
    print("\ntraffic_in :" +str(current_in) + "\ntraffic_out:" +str(current_out) )
    #network = {"traffic_in": current_in, "traffic_out": current_out}
    #return network
    #print(network)
get_bandwidth()

print("==============================================================================")


"""
 List of all process IDs currently active
"""

def process_list():

    pids = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pids.append(subdir)

    return pids


if __name__=='__main__':

    pids = process_list()
    print(" ")
    print('Total number of running processes:: {0}'.format(len(pids)))
    print(" ")


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''

    listOfProcessObjects = []

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo['name'].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return listOfProcessObjects;


def main():
#pstree
    print("\n*** Checking process details ***")
    proc = input("\nEnter the name of the process to get Details or Press Enter to get all running process : ")
    print("\nlooking for the " +proc+ " process details ......")

    # Check if any chrome process was running or not.
    if checkIfProcessRunning(proc):
        print('Yes a ' + proc + ' process is running')
    else:
        print('\nNo ' + proc + ' process is running')

    print("\n*** Find PIDs of a running process by Name ***")

    # Find PIDs od all the running instances of process that contains 'chrome' in it's name
    listOfProcessIds = findProcessIdByName(proc)

    if len(listOfProcessIds) > 0:
        print('\nProcess Exists | PID and other details are')
        for elem in listOfProcessIds:
            processID = elem['pid']
            processName = elem['name']
            processCreationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
            print((processID, processName, processCreationTime))
    else:
        print('\nNo Running Process found with given text')

    print('\n** Find running process by name using List comprehension **')

    # Find PIDs od all the running instances of process that contains 'user-entered process' in it's name
    procObjList = [procObj for procObj in psutil.process_iter() if proc in procObj.name().lower()]

    for elem in procObjList:
        print (elem)


    if len(listOfProcessIds) > 0:
        killprocess = input("\nWant to kill any unwanted process enter 'yes' or  enter 'no' to continue further :")
        #print(killprocess)
        if killprocess == "yes":
            print("\nprocess killing is activated...")
            abc = input("   " " \n" "       Enter the process Name to Terminate : ")
            for line in os.popen("ps ax | grep " + abc + " | grep -v grep"):
                fields = line.split()
                pid = fields[0]
                print(pid)
                #os.kill(int(pid), signal.SIGKILL)
        else:
           pass


if __name__ == '__main__':
    main()

print("==============================================================================")

