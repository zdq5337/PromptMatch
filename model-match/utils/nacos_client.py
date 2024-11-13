import platform
import socket

import netifaces as ni


def get_ip_address():
    os_name = platform.system()

    if os_name == 'Linux':
        interface_types = ['eth', 'en', 'wl', 'ww']

        for interface_type in interface_types:
            try:
                # 按照网络接口类型查找接口名称 erh
                # en　　以太网　　　　Ethernet 99
                # wl　　无线局域网　　WLAN 98
                # ww　 无线广域网　　WWAN 97
                # eth old linux interface name   100
                interface_names = ni.interfaces()
                for iface in interface_names:
                    if interface_type in iface:
                        interface_addresses = ni.ifaddresses(iface)
                        ipv4_addresses = interface_addresses.get(ni.AF_INET)
                        if ipv4_addresses:
                            ipv4_address = ipv4_addresses[0]['addr']
                            return ipv4_address
            except (KeyError, ValueError, OSError) as e:
                print(f"错误：{e}")
                return None
        return None  # 未找到符合条件的接口
    elif os_name == 'Windows':
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            return host_ip
        except socket.gaierror:
            return None
    else:
        return "Unsupported OS"
