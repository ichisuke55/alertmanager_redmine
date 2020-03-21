#/usr/bin/python3.5

import json
import logging
from redminelib import Redmine
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")
requests_log = logging.getLogger('requests.pachages.urllib3')
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class TroubleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = json.loads(self.rfile.read(int(self.headers.get('content-length'))).decode('utf-8'))

        alert_data = self.build_alert_data(data)
        logging.info('received data: %s' % alert_data)
        self.create_alert_redmine_issue(alert_data, data['status'])


    def build_alert_data(self, data):
        alert_data = {
            "status": data["status"],
            "alertname": data["alerts"][0]["labels"]["alertname"],
            "starts_at": data["alerts"][0]["startsAt"],
            "summary": data["alerts"][0]["annotations"]["summary"],
            "alert_num": len(data["alerts"])
        }
        return alert_data


    def create_alert_redmine_issue(self, alert_data, alert_status):
        c = RedmineTicket()
        c.generate_redmine_ticket(alert_data)


class RedmineTicket():
    def __init__(self):
        SERVER = 'https://example/redmine/'
        KEY = 'ACCESS_KEY'
        USER_NAME = 'ichisuke'
        USER_PASS = 'hogesuke' 
        self.redmine = Redmine(SERVER, key=KEY, username=USER_NAME, password=USER_PASS, requests={'verify': False})


    def generate_redmine_ticket(self, data):
        issue = self.redmine.issue.new()
        issue.project_id = 5
        issue.tracker_id = 40
        issue.subject = '[FIRING:' + str(data["alert_num"]) + ']' +  data["alertname"]
        issue.description = '手順に沿って対応を進めてください。'
        issue.status_id = 1
        issue.priority_id = 5
        if data["status"] == 'firing':
            issue.save()


if __name__ == '__main__':
    httpd = HTTPServer(('', 9999), TroubleHandler)
    httpd.serve_forever()
