from time import sleep
import telnetlib
import re
from netmiko import ConnectHandler
from strip_ansi import strip_ansi
import xmlrpc.client


# Defining Vars for ODOO API call #
#url = "https://traversa-odoo-traversa-uat-2889919.dev.odoo.com/"
#db = "traversa-odoo-traversa-uat-2889919"
#username = "pselvarajan@traversa.net"
#password = "Testing1234!"
#create function

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
        try:
            print("Uploading Data in store")
            self.ip_address_aruba_telnet = input_data['proxy_ip']#10.210.210.117
            self.port_aruba_telnet = input_data['port_no']#2004
            self.firmware_to_upgrade = input_data['firmware']#firmware
            self.tftp_server = input_data['tftp_server']    
            sleep(0.5)
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def connect_telnet(self):
        '''
        Create Socket
        Output = "Object" Datatype
        '''
        try:
            global telnet_socket
            print("Creating Telnet Socket")
            telnet_socket = telnetlib.Telnet(self.ip_address_aruba_telnet,self.port_aruba_telnet)
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def configure_new_manager_password(self):
        '''
        Config New switch username and password
        '''
        try:
            print("configure_new_manager_password")
            telnet_socket.write(b"\r\n")
            sleep(0.5)
            telnet_socket.write(b"\r\n")
            sleep(4)
            telnet_socket.write(b"admin\n")
            sleep(2)
            telnet_socket.write(b"Pr0curve\n")
            sleep(2)
            telnet_socket.write(b"Pr0curve\n")
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def configure_ip(self):
        '''
        Config IP address for vlan 4094 and assign to interface 1
        '''
        try:        
            print("configurng Mgmt IP")
            self.configuring_ip = '10.211.211.'+str(int(str(self.port_aruba_telnet)[-2:]))
            byteipformat = ("ip address "+ self.configuring_ip +"/24\n").encode()
            #print(self.configuring_ip)
            telnet_socket.write(b"configure terminal\n")
            telnet_socket.write(b"ip default-gateway 10.211.211.1\n")
            telnet_socket.write(b"vlan 4094\n")
            telnet_socket.write(b"untag 1\n")
            telnet_socket.write(b"untag 1/1\n")
            telnet_socket.write(byteipformat)#b"ip address "+ self.configuring_ip +"\n")
            telnet_socket.write(b"end\n")
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def configure_ssh(self):
        '''
        Config SSH through telnet
        '''
        try:
            print("Configuring SSH")
            telnet_socket.write(b"configure terminal\n")
            telnet_socket.write(b"crypto key generate ssh rsa bit 2048\n")
            telnet_socket.write(b"ip ssh\n")
            telnet_socket.write(b"end\n")
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def get_ssh_data(self):
        '''
        SSH device connection
        '''
        try:
            global net_connect
            print("SSH connection")
            #Need to change host ip to be a variable
            aruba = { 
            'device_type': 'hp_procurve', 
            'host':self.configuring_ip, 
            'username': 'admin',  
            'password': 'Pr0curve', 
            'fast_cli': True,
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
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def firmware_upgrade(self):
        '''
        Upgrade to given firmware
        Input = "String" Datatype
        '''
        try:
            print("firmware_upgrade function")
            final_firmware = ("copy tftp flash "+  self.tftp_server+" "+self.firmware_to_upgrade+" primary\n").encode()
            telnet_socket.write(final_firmware)
            telnet_socket.write(b"y\n")
            #read until firmware is complete
            sleep(50)
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def copy_primaryflash_secondaryflash(self):
        '''
        Config IP address for vlan 4094 and assign to interface 1
        '''
        try:
            print("copy primary flash to secondary flash")
            sleep(20)
            copy_pri_sec_fl = net_connect.send_config_set(['copy flash flash secondary'])
            print(copy_pri_sec_fl)
            sleep(20)
            print("completed")
        except Exception as e:
            print(e)
            raise e
    def reload(self):
        '''
        Boot system to upgrade the firmware.
        '''
        try:
            print("telnet rebooting the switch")
            telnet_socket.write(b"admin\n")
            telnet_socket.write(b"Pr0curve\n")
            telnet_socket.write(b"kill 3\n")
            telnet_socket.write(b"kill 2\n")
            telnet_socket.write(b"kill 1\n")
            telnet_socket.write(b"boot system\n")
            telnet_socket.write(b"y\n")
            telnet_socket.write(b"n\n")
            print("completed")
        except Exception as e:
            print(e)
            raise e
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
    
    def add(self):
        try:
            sleep(2)
            a = 4
            b = 6
            sum = a+ b
            sleep(2)
            print("add success")
        except Exception as e:
            print(e)
    def sub(self):
        try:
            a = 44
            b = 14
            sum = a- b
            sleep(2)
            print("sub success")
        except Exception as e:
            print(e)
            raise e
    def mul(self):
        try:
            a = 4
            b = 6
            sum = a * b
            sleep(2)
            print("mul success")
        except Exception as e:
            print(e)
    def delete(self):
        try:
            a = 40
            b = 6
            sum = 10 * (1/0)
            sleep(4)
            print("delete success")
        except Exception as e:
            raise e
            pass
