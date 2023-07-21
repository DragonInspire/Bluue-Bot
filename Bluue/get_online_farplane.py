import requests
import json

def nameList():
    GUILD_NAME = "The Farplane"

    response = requests.get(f"https://api.wynncraft.com/public_api.php?action=guildStats&command={GUILD_NAME}")

    if response.status_code == 200:
            # Extract the UUID from the response
            response = response.json().get("members")
            nameList = []
            for member in response:
                nameList.append(member.get("name"))

            return(nameList)
    else:
        print(f"error {response.status_code}")
        return("No response from wynncraft api")


def onlinePlayers():

    response = requests.get(f"https://api.wynncraft.com/public_api.php?action=onlinePlayers")

    if response.status_code == 200:
        # Extract the UUID from the response
        response = response.json()

        return response

    else:
        return("no response from wynncraft api")



def get_online_farplane():
    farplaneList = nameList()
    online = onlinePlayers()


    players = list(online.values())[1::]
    worlds = list(online.keys())[1::]

    farplaneOnline = {}

    i = 0
    for worldID in worlds:
        farplaneOnline[worldID] = []

    for world in players:
        for player in farplaneList:
            if player in world:
                farplaneOnline[worlds[i]].append(player)
        i+=1

    worlds_to_delete = []
    for world in farplaneOnline:
        if farplaneOnline[world] == []:
            worlds_to_delete.append(world)

    for world in worlds_to_delete:
        del farplaneOnline[world]

    return(farplaneOnline)