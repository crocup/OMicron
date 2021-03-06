from itertools import groupby
from app import db_collection, db_scanner
from app.database import Inventory_Data_All


def chart_dashboard():
    """
    функция для агрегации данных по построению графиков на вкладке /dashboard
    Графики: port, service
    Таблицы: Last Task, Last CVE
    :return: список данных
    """
    ip_list = Inventory_Data_All()
    top_ports_list = []
    top_services_list = []
    top_vuln_list = []
    for i in ip_list:
        result_vulnerability = db_scanner.result.find({"host": i["ip"]}).sort("_id", -1).limit(1)
        for scanner in result_vulnerability:
            for result in scanner["scanner"]:
                top_ports_list.append(result["port"])
                top_services_list.append(result["service"]["name"])
            for vuln in scanner["scanner"]:
                for vuln_cve in vuln["vulnerability"]["cve_mitre"]:
                    top_vuln_list.append(vuln_cve["cve"])
    r_port = groupby(sorted(top_ports_list))
    r_service = groupby(sorted(top_services_list))
    count_vuln = len(set(list(top_vuln_list)))

    top_ports = top(top_ports_list, r_port)
    top_services = top(top_services_list, r_service)

    return ip_list, count_vuln, top_ports, top_services


def top(list_top, val):
    """
    создание массива данных (пример: [[ssh, 23],[http, 10]])
    :param list_top: список
    :param val: значение
    :return: отсортированный массив данных
    """
    res_sort = []
    for k, g in val:
        persent_port = (int(len(list(g))) * 100) / int(len(list_top))
        res_sort.append([k, round(persent_port, 2)])
    res_result = sorted(res_sort, key=lambda x: x[1], reverse=True)
    return res_result


def new_vulnerability():
    """
    функция возвращает список последних издексов CVE из базы данных
    :return: список последних CVE в базе данных
    """
    return db_collection.find().sort("_id", -1).limit(3)
