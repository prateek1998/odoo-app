import time
import telnetlib
from strip_ansi import strip_ansi
import xmlrpc.client

# Defining Vars for ODOO API call #
#url = "https://traversa-odoo-traversa-uat-2889919.dev.odoo.com/"
#db = "traversa-odoo-traversa-uat-2889919"
#username = "pselvarajan@traversa.net"
#password = "Testing1234!"
#create function

#STEPS:
#1. Enter odoo ID in UI and fetch data using function(PORT,FIRMWARE).
#2. Connect function to pass vars from one function to other.
#3. Parse and display result from switch to UI
class aruba_os_telnet:
    def __init__(self):
        self.ip_address_aruba_telnet = ''#10.210.210.117
        self.port_aruba_telnet = ''#2004
        self.firmware_to_upgrade = ''#firmware
        self.tftp_server = ''
        self.configuring_ip = ''
        self.url = "https://traversa-odoo-traversa-uat-2889919.dev.odoo.com/"
        self.db = "traversa-odoo-traversa-uat-2889919"
        self.username = "pselvarajan@traversa.net"
        self.password = "Testing1234!"
    def data_store(self, input_data):
        self.ip_address_aruba_telnet = input_data['proxy_ip']#10.210.210.117
        self.port_aruba_telnet = input_data['port_no']#2004
        self.firmware_to_upgrade = input_data['firmware']#firmware
        self.tftp_server = input_data['tftp_server']    
    def odoo_fetch_api(self, input_data):
        manu_id = input_data['odoo_id']
        #print(manu_id)
        # manufacturing_order = "WH/MO/00107"
        common = xmlrpc.client.ServerProxy('{}xmlrpc/2/common'.format(self.url))
        models = xmlrpc.client.ServerProxy('{}xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})
        partners = models.execute_kw(self.db, uid, self.password, 'mrp.production', 'search', [[['name', '=', manu_id]]])
        manufacturing_order_firmware = models.execute_kw(self.db, uid, self.password, 'mrp.production', 'read', [partners], {'fields': ['firmware']})
        manufacturing_order_mgmt_ip = models.execute_kw(self.db, uid, self.password, 'mrp.production', 'read', [partners], {'fields': ['mgmt_ip']})
        #print(manufacturing_order_firmware[-1]['firmware'])
        # self.firmware_to_upgrade = manufacturing_order_firmware[-1]['firmware']
        output_data = {
            'firmware': manufacturing_order_firmware[-1]['firmware'],

        }
        # print("1",output_data)
        return output_data
        #print(self.firmware_to_upgrade)
        # port_aruba_telnet = 
        #print(manufacturing_order_mgmt_ip[-1]['mgmt_ip']) 
    def send_telnet_commands(self,command):
        '''
        Send Telnet Command
        Input = "String" Datatype
        Output = "NoneType" Datatype
        '''
        telnet_socket.write(command.encode('utf-8') + b"\n")
    def read_telnet_commands(self):
        '''
        Read Telnet Output
        Output = "string" Datatype
        '''
        readoutput = telnet_socket.read_all().decode('ascii')
        pretty_readouput = strip_ansi(readoutput)
        return pretty_readouput
    def close_telnet_connection(self):
        '''
        Closes Telnet connection
        '''
        telnet_socket.close()
    def connect_telnet(self):
        '''
        Create Socket
        Output = "Object" Datatype
        '''
        global telnet_socket
        telnet_socket = telnetlib.Telnet(self.ip_address_aruba_telnet,self.port_aruba_telnet)
        print("succesfull")
    def firmware_upgrade(self):
        '''
        Upgrade to given firmware
        Input = "String" Datatype
        '''
        print("firmware_upgrade function")
        final_firmware = ("copy tftp flash "+  self.tftp_server+" "+self.firmware_to_upgrade+" primary\n").encode()
        telnet_socket.write(final_firmware)
        telnet_socket.write(b"y\n")
        #read until firmware is complete
        sleep(200)
        print("completed")
    def configure_ip(self):
        '''
        Config IP address for vlan 4094 and assign to interface 1
        '''
        print("configurng Mgmt IP")
        self.configuring_ip = '10.211.211.'+ str(self.port_aruba_telnet)[-2:]+'/24'
        print(self.configuring_ip)
        telnet_socket.write(b"configure terminal\n")
        telnet_socket.write(b"ip default-gateway 10.211.211.1\n")
        telnet_socket.write(b"vlan 4094\n")
        telnet_socket.write(b"untag 1\n")
        telnet_socket.write(b"untag 1/1\n")
        telnet_socket.write(b"ip address "+ self.configuring_ip +"\n")
        telnet_socket.write(b"end\n")
        print("completed")
    def remove_ip(self, te):
        '''
        Config IP address for vlan 4094 and assign to interface 1
        '''
        print("removing Mgmt IP")
        system = net_connect.send_config_set(['no ip default-gateway'])
        telnet_socket = telnetlib.Telnet(self.ip_address_aruba_telnet,self.port_aruba_telnet)
        telnet_socket.write(b"configure terminal\n")
        telnet_socket.write(b"no vlan 4094\n")
        telnet_socket.write(b"y\n")        
        print("completed")
    def copy_primaryflash_secondaryflash(self):
        '''
        Config IP address for vlan 4094 and assign to interface 1
        '''
        print("copy primary flash to secondary flash")
        sleep(30)
        copy_pri_sec_fl = net_connect.send_config_set(['copy flash flash secondary'])
        print(copy_pri_sec_fl)
        print("completed")
    def reload(self):
        '''
        Boot system to upgrade the firmware.
        '''
        print("rebooting the switch")
        sleep(10)
        boot_system = net_connect.send_config_set(['kill 2', 'boot system','y','n'])
        print(boot_system)
        print("completed")
    def configure_new_manager_password(self):
        '''
        Config New switch username and password
        '''
        print("configure_new_manager_password")
        telnet_socket.write(b"\r\n")
        sleep(0.5)
        telnet_socket.write(b"\r\n")
        sleep(2)
        telnet_socket.write(b"admin\n")
        sleep(1)
        telnet_socket.write(b"Pr0curve\n")
        sleep(1)
        telnet_socket.write(b"Pr0curve\n")
        print("completed")
    def configure_ssh(self):
        '''
        Config SSH through telnet
        '''
        print("Configuring SSH")
        telnet_socket.write(b"configure terminal\n")
        telnet_socket.write(b"crypto key generate ssh rsa bit 2048\n")
        telnet_socket.write(b"ip ssh\n")
        telnet_socket.write(b"end\n")
        print("completed")
    def get_ssh_data(self):
        '''
        SSH device connection
        '''
        global net_connect
        print("SSH connection")
        #Need to change host ip to be a variable
        aruba = { 
        'device_type': 'hp_procurve', 
        'host':self.configuring_ip, 
        'username': 'admin',  
        'password': 'Pr0curve', 
        }
        net_connect = ConnectHandler(**aruba)
        system = net_connect.send_command("show system")
        serial_number = re.findall("Serial Number.*", system)
        mac_address = re.findall("Base MAC Addr.*", system)
        version = re.findall("Software revision.*", system)
        serial_number_string = serial_number[0].partition(":")[-1].strip()
        mac_address_string = mac_address[0].partition(":")[-1].strip()
        version_string = version[0].partition(":")[-1].strip()[0:13]
        print(serial_number_string)
        print(mac_address_string)
        print(version_string)
    
# 10.210.210.251 ---> file server ip

# 10.210.210.117 ---> terminal/proxy server

#Steppers
# 1. check the connection status from odoo.
# 2. Received data from odoo server.
# 3. Connection web server and switch (telnet connect function).
# 4. upgrading firmware (firmware_upgrade).
# 5. firmware upgraded.


# Table
# 1.s no
# 2.time
# 3. old firmware
# 4. new firmware
# 5. modal of switch
# 6. status

# test = aruba_os_telnet()
# test.odoo_fetch_api()
# #switch A
# #test = aruba_os_telnet("10.210.210.117",2005) #switch B
# test.connect_telnet()
# #test.send_telnet_commands("sh version")

# #print(result)
# test.firmware_upgrade()
# result = test.read_telnet_commands()
# print(result)
# #test.close_telnet_connection()
