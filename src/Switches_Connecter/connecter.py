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


#Port
#IP_Address
#FIRMWARE
#
#Webserver -> Switch

#STEPS:
#1. Enter odoo ID in UI and fetch data using function(PORT,FIRMWARE).
#2. Connect function to pass vars from one function to other.
#3. Parse and display result from switch to UI
class aruba_os_telnet:
    def __init__(self):
        self.ip_address_aruba_telnet = "10.210.210.117"
        self.port_aruba_telnet = 2004
        self.firmware_to_upgrade = ""
        self.url = "https://traversa-odoo-traversa-uat-2889919.dev.odoo.com/"
        self.db = "traversa-odoo-traversa-uat-2889919"
        self.username = "pselvarajan@traversa.net"
        self.password = "Testing1234!"
    def odoo_fetch_api(self, manu_id):
        print(manu_id)
        # manufacturing_order = "WH/MO/00107"
        common = xmlrpc.client.ServerProxy('{}xmlrpc/2/common'.format(self.url))
        models = xmlrpc.client.ServerProxy('{}xmlrpc/2/object'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})
        partners = models.execute_kw(self.db, uid, self.password, 'mrp.production', 'search', [[['name', '=', manu_id]]])
        manufacturing_order_firmware = models.execute_kw(self.db, uid, self.password, 'mrp.production', 'read', [partners], {'fields': ['firmware']})
        manufacturing_order_mgmt_ip = models.execute_kw(self.db, uid, self.password, 'mrp.production', 'read', [partners], {'fields': ['mgmt_ip']})
        #print(manufacturing_order_firmware[-1]['firmware'])
        self.firmware_to_upgrade = manufacturing_order_firmware[-1]['firmware']
        print(self.firmware_to_upgrade)
        # port_aruba_telnet = 
        print(manufacturing_order_mgmt_ip[-1]['mgmt_ip'])
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
        print("upgrading firmware")
        print(self.firmware_to_upgrade)
        final_firmware = ("copy tftp flash 10.210.210.251 "+self.firmware_to_upgrade+" primary\n").encode()
        print(final_firmware)
        print(type(final_firmware))

        telnet_socket.write(final_firmware)
        telnet_socket.write(b"y\n")
        #pass

# 10.210.210.251 ---> file server ip

# 10.210.210.117 ---> terminal/proxy server

# manu_id 


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