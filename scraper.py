import requests

print("Input the URL:")
input_ = input("> ")
r = requests.get(input_)
print()

if r.status_code == 200 and "content" in r.json():
    print(r.json()["content"])
else:
    print("Invalid quote resource!")
