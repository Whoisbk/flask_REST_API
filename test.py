import requests

BASE = "http://127.0.0.1:5000/"

#this is the information we send
#the response will be returned in json format eg.Dictionaries

data = [{"Episodes": 24,"Name":"Jujutsu kaisen","Seasons": 1,"Rating": "9/10"},
        {"Episodes": 12,"Name":"God of Highschool","Seasons": 1,"Rating": "7/10"},
        {"Episodes": 12,"Name":"Tower of God","Seasons": 1,"Rating": "9/10"},
        {"Episodes": 25,"Name":"Doctor Stone","Seasons": 2,"Rating": "9/10"}] 


for i in range(len(data)):
    response = requests.put(BASE + "myAnime/"+ str(i),data[i])
    print(response.json())


#response = requests.delete(BASE + "myAnime/0")
#print(response)#delete request does not return any json 

input()
response = requests.get(BASE + "myAnime/2")#returns the data in the anime dict that has an id of 1
print(response.json())

