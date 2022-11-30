import threading
import paramiko
import time
import csv
import json


def configure(sw):
    sshcli = paramiko.SSHClient()
    sshcli.load_system_host_keys()
    sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Connecting to {sw['ipaddr']}...")
    sshcli.connect(hostname=sw['ipaddr'], port=22, username=sw['usr'], password=sw['pswd'], look_for_keys=False,
                   allow_agent=False)
    shell = sshcli.invoke_shell()
    print(f'Connected to {sw["ipaddr"]}!!!')

    with open('ICCN_switch_SNMPCommands.txt') as c:
        commands = c.read().splitlines()
        print(f'Configuring SNMP on {sw["ipaddr"]}...')
        for command in commands:
            shell.send(command + '\n')
            time.sleep(2)
    shell.recv(10000)
    shell.send('show ip route' + '\n')
    time.sleep(2)
    # out = shell.recv(10000)
    # print(out.decode())

    if sshcli.get_transport().is_active():
        print(f'Closing Connection with {sw["ipaddr"]}!!!')
        sshcli.close()


with open('devices.csv') as f:
    reader = csv.reader(f, delimiter=':', lineterminator='\n')
    ICCN_Switches = {}
    for row in reader:
        switch = {'ipaddr': row[1], 'port': 22, 'usr': row[2], 'pswd': row[3]}
        tmp = {}
        for switch_version in [row[0]]:
            tmp["switch_%s" % switch_version] = switch
            ICCN_Switches.update(tmp)

# For JSON formatting
# with open('test.json', 'w') as f:
#     json.dump(ICCN_Switches, f)
# with open('test.json') as f:
#     data = json.load(f)
# print(data)


threads = list()
for swtch in list(ICCN_Switches.values()):
    th = threading.Thread(target=configure, args=(swtch,))
    threads.append(th)

for th in threads:
    th.start()

for th in threads:
    th.join()

########################################################################################################################
# print('Dictionary of all the hosts with keys as switch name and values as dictionary of host info:')
# print(ICCN_Switches)
# print('# This will print the ip of switch 7028')
# print(ICCN_Switches['switch_7028']['ipaddr'])
# print('# This will print all the host info')
# print(ICCN_Switches.values())
# print('# Will print the first host info')
# print(list(ICCN_Switches.values())[0])
# print(' # This will print the ip addresses of all the hosts')
# print(ICCN_Switches.keys())
# print('# This will print the name of the first host')
# print(list(ICCN_Switches.keys())[0])
# print('# This will print the ip of the first host')
# print(ICCN_Switches[list(ICCN_Switches.keys())[0]]['ipaddr'])

# For JSON formatting
# with open('test.json', 'w') as f:
#     json.dump(ICCN_Switches, f)
# with open('test.json') as f:
#     data = json.load(f)
# print(data)
