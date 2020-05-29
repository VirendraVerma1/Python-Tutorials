import json
from difflib import get_close_matches

def translate(w):
    w=w.lower()
    if w in data:
        return data[w]
    elif (len(get_close_matches(w,data.keys()))>0):
        yn=input("Did you mean %s instead? Enter y if yes or Enter n for no: " % get_close_matches(w,data.keys())[0])
        if yn=="y":
            return data[get_close_matches(w,data.keys())[0]]
        else :
            return "The word doesn't exist."
    else:
        return "Enter a propper word"
data=json.load(open("data.json"))
word=input("Enter a word: ")
output=translate(word)
if type(output)==list:
    for item in output:
        print(item)
else:
    print(output)
