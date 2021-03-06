import re
import nmap3
from app import db_scanner
from app.database import Inventory_Data_Record, Inventory_Data_Delete


def check_host_discovery():
    """
    проверка на наличие новых ip в системе
    :return:
    """
    pass


def delete_ip(host):
    try:
        Inventory_Data_Delete(host)
    except Exception as e:
        status = "error: {}".format(e)
        print(status)


class Inventory(object):

    def __init__(self, target):
        """

        :param target: ip address/mask network (example 192.168.100.0/24)
        """
        self.target = target

    def scan_arp(self):
        """

        :return: list ip address and mac
        """
        try:
            clients_list = []
            hd_scan = nmap3.NmapHostDiscovery()
            result = hd_scan.nmap_no_portscan(self.target)
            for res in result:
                check_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", res)
                if check_ip:
                    ip = check_ip.group()
                    clients_list.append(ip)
        except Exception as e:
            print(e)
            clients_list = []
        return clients_list

    def result_scan(self):
        """

        :return:
        """
        try:
            result = list(self.scan_arp())
            Inventory_Data_Record(result)
            return "success"
        except Exception as e:
            status = "error: {}".format(e)
            return status
