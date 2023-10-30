import json


def get_Studentjson():
    with open("./static/StudentJson.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def write_Studentjson(data):
    updated = json.dumps(data, indent=3)
    with open("./static/StudentJson.json", "w") as write_it:
        write_it.write(updated)
        write_it.close()


def get_profile(roll):
    data = get_Studentjson()[roll]
    return data["email"].upper(), roll.upper(), data["bookBorrow"], data["bookReturn"], data["notReturn"], data["fines"]
