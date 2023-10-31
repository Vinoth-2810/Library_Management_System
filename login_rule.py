import json


def get_Studentjson():
    with open("./static/LoginData.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def Write_Studentjson(updata):
    data = json.dumps(updata, indent=1)
    with open("./static/LoginData.json", "w") as write_it:
        write_it.write(data)
        write_it.close()


def auth_Login(data):
    base = get_Studentjson()
    user = str(data['username']).lower()
    if str(data["Role"]) == "student":
        if user in base[0]["Email"]:
            pwd = user.split("@")[0]
            if str(data["password"]) == pwd:
                return ["Success", data["Role"]]
            else:
                return ["Fail", data["Role"]]
        else:
            return ["Fail", data["Role"]]
    else:
        if user in base[1]["Email"]:
            pwd = base[1]["pwd"]
            if str(data["password"]) == pwd:
                return ["Success", data["Role"]]
            else:
                return ["Fail", data["Role"]]
        else:
            return ["Fail", data["Role"]]


def add_auth(email):
    data = get_Studentjson()
    data[0]["Email"].append(email)
    Write_Studentjson(data)
