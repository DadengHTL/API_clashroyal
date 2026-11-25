import requests
u=input("Gib Anzahl der Teilnehmer ein: ") # user input für die Anzahl der Teilnehmer
url="https://bored.api.lewagon.com/api/activity?participants=" + u #Userparameter wird in die URL eingefügt 

data=requests.get(url)
#--> Umwandeln von Json in DICT
data=data.json()
print(data["activity"])
