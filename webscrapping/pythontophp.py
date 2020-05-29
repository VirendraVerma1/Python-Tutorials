import urllib.request
import urllib.parse

data = urllib.parse.urlencode({'spam': "no one knows", 'eggs': "what are you doing", 'bacon': "213"})
data = data.encode('utf-8')
request = urllib.request.Request("http://usearch.000webhostapp.com/new.php")

# adding charset parameter to the Content-Type header.
request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")

f = urllib.request.urlopen(request, data)
print(f.read().decode('utf-8'))
