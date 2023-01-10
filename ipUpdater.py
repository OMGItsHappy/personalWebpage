import requests
import constantsAndKeys as ck


a = requests.post(f"https://${ck.googleUserName}:${ck.googlePassword}@domains.google.com/nic/update?hostname=${ck.hostName}")

print(a.content.decode("utf-8"))

ck.test = "hi"
