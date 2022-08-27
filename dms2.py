import datetime
import time
import uuid
from typing import Optional, Any, List, Dict
from urllib.parse import urljoin
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DMS2:
    def __init__(self, url):
        # get session
        self.url = url
        self.session = requests.session()

        # get session ID
        self._do_request("/dms2/Login.jsp", "GET")
        self.session_id = self.session.cookies["JSESSIONID"]

    def _do_request(self, path: str, method: str, data: Optional[Any] = None):
        return self.session.request(method, urljoin(self.url, path), data=data, verify=False)

    def login(self, username, password):
        # build data for login
        data = {
            "securedUsername": username + self.session_id,
            "securedPassword": password + self.session_id
        }

        # login
        self._do_request("/dms2/Login.jsp", "POST", data=data)

        # sleep a little
        time.sleep(1)

    def logout(self):
        self._do_request("/dms2/SystemSettingServlet?action=logout", "POST")

    def _get_monitoring(self, content):
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S:000")
        data = f"{str(uuid.uuid4())}:<?xml version='1.0' encoding='utf-8' standalone='yes'?>" \
               f"<root><header sa='web' da='dms' messageType='request' " \
               f"dateTime='{now}' dvmControlMode='individual' />" + content + "</root>";
        resp = self._do_request("/dms2/getMonitoring?currentPage=main", "POST", data=data)
        return resp.json()

    def get_monitoring(self):
        return self._get_monitoring("<getMonitoring><all/></getMonitoring>")

    def control(self, addresses: List[str], values: Dict[str, Any]) -> None:
        address_list = "".join([f"<address>{a}</address>" for a in addresses])
        control = "".join([f"<{key}>{value}</{key}>" for key, value in values.items()])
        content = f"<setDeviceControl><controlList><control><controlValue>{control}</controlValue>" \
                  f"<addressList>{address_list}</addressList></control></controlList></setDeviceControl>"
        print(content)
        return self._get_monitoring(content)

    def switch_power(self, addresses: List[str], power: bool):
        return self.control(addresses, {"power": "on" if power else "off"})

    def set_temp(self, addresses: List[str], temp: float) -> None:
        return self.control(addresses, {"setTemp": temp})
