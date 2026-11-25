import requests
u=input("Gib name fürs Getränk ein: ") # user input für die Anzahl der Teilnehmer
url="https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + u #Userparameter wird in die URL eingefügt 

data=requests.get(url)
#--> Umwandeln von Json in DICT
data=data.json()
print(data["drinks"][0]["strInstructionsZH-HANS"])
 