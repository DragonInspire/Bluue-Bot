import requests
import json


def objectListToString(input_list):
    new_list = []
    for member in input_list:
        temp = list(member.values())
        for thing in temp:
            new_list.append(thing)
        new_list.append('$')
    new_list=str(new_list)
    new_list = new_list.replace("'", "").replace('"', '').replace('[', '').replace(']','').replace(",", "")
    new_list = "```" + new_list + "```"

    new_list = new_list.replace("$", "\n")
    return new_list

def guildList():
    GUILD_NAME = "The Farplane"

    response = requests.get(f"https://api.wynncraft.com/public_api.php?action=guildStats&command={GUILD_NAME}")

    if response.status_code == 200:
            # Extract the UUID from the response
            response = response.json().get("members")
            memberList = []
            for member in response:
                memberList.append({"rank": member.get("rank"), "name": member.get("name")})

            memberList = objectListToString(memberList)
            return(memberList)
    else:
        print(f"error {response.status_code}")
        return("No response from wynncraft api")