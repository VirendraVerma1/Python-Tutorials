import urllib.request
req=urllib.request.Request(url='http://www.google.com/')
f=urllib.request.urlopen(req)
print(f.read().decode('utf-8'))
