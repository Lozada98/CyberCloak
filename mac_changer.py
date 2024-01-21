import subprocess
import argparse
import re
import platform

class MacChanger:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-i", "--interface", dest="interface", help="Interface to change MAC Address")
        self.parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC Address")
        self.args = self.parser.parse_args()

    def get_arguments(self):
        if not self.args.interface:
            self.parser.error("[-] Please indicate an interface, use --help for more information")
        elif not self.args.new_mac:
            self.parser.error("[-] Please provide a MAC address, use --help for more information")
        return self.args

    def change_mac(self, interface, new_mac):
        try:
            print("[+]  Changing MAC Address for" + interface + " to " + new_mac)

            os_name = platform.system().lower()
            if os_name == 'linux':
                subprocess.call(["ifconfig", interface, "down"])
                subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
                subprocess.call(["ifconfig", interface, "up"])
            elif os_name == 'darwin':  # macOS
                subprocess.call(["ifconfig", interface, "ether", new_mac])
            elif os_name == 'windows':
                # Comando para cambiar la dirección MAC en Windows
                subprocess.call(["netsh", "interface", "set", "interface", f"Name={interface}", f"NewMac={new_mac}"])
            else:
                print("[-] Unsupported operating system")

        except Exception as e:
            print("[-] Error changing MAC address: ", str(e))

    def get_current_mac(self, interface):
        try:
            if platform.system().lower() == 'windows':
                # Comando para obtener la dirección MAC en Windows
                ifconfig_result = subprocess.check_output(["getmac", f"/FO=CSV /V /NH /VALUE /IMAGENAME={interface}"])
                mac_address_search_result = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", ifconfig_result.decode('utf-8'))
            else:
                ifconfig_result = subprocess.check_output(["ifconfig", interface])
                mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))

            if mac_address_search_result:
                return mac_address_search_result.group(0)
            else:
                print("[-] We could not read the MAC address")
        except Exception as e:
            print("[-] Error getting current MAC address: ", str(e))

if __name__ == "__main__":
    mac_changer = MacChanger()

    args = mac_changer.get_arguments()

    current_mac = mac_changer.get_current_mac(args.interface)
    print("Current MAC = " + str(current_mac))

    mac_changer.change_mac(args.interface, args.new_mac)

    current_mac = mac_changer.get_current_mac(args.interface) 
    if current_mac == args.new_mac:
        print("[+] MAC address successfully changed to " + current_mac)
    else:
        print("[-] MAC address was not changed ")



    
    

