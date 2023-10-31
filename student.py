import json
import login_rule


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


def updateborrow(roll, bookid, borrowid):
    datakeys = list(get_Studentjson().keys())
    if roll in datakeys:
        data = get_Studentjson()
        data[roll]["bookBorrow"] = data[roll]["bookBorrow"] + 1
        data[roll]["notReturn"] = data[roll]["notReturn"] + 1
        data[roll]["Books"].append(bookid)
        data[roll]["BorrowID"].append(borrowid)
        write_Studentjson(data)
    else:
        data = get_Studentjson()
        newdata = {
            "email": "-",
            "bookBorrow": 1,
            "bookReturn": 0,
            "notReturn": 1,
            "fines": 0.0,
            "Books": [],
            "BorrowID": []
        }
        newdata["email"] = roll + "@kce.ac.in"
        newdata["Books"].append(bookid)
        newdata["BorrowID"].append(borrowid)
        data[roll] = newdata
        write_Studentjson(data)
        login_rule.add_auth(newdata["email"])


def updatertrn(roll, fines):
    datakeys = list(get_Studentjson().keys())
    if roll in datakeys:
        data = get_Studentjson()
        data[roll]["bookReturn"] = data[roll]["bookReturn"] + 1
        data[roll]["notReturn"] = data[roll]["notReturn"] - 1
        data[roll]["fines"] = data[roll]["fines"] + fines
        write_Studentjson(data)
