import json
import globalVariable


def get_json():
    with open("./static/Books.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def write_json(data):
    with open("./static/Books.json", "w") as write_it:
        write_it.write(data)
        write_it.close()


def get_audjson():
    with open("./static/AudioBook.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def write_audjson(data):
    with open("./static/AudioBook.json", "w") as write_it:
        write_it.write(data)
        write_it.close()


def get_cate(cate):
    newdata = []
    data = get_json()
    for i in data:
        if i["_Category"].lower() == cate.lower():
            newdata.append(i)
        else:
            pass
    return newdata


def get_audCate(cate):
    newdata = []
    data = get_json()
    if cate.lower() == "all":
        for i in data:
            if i["_Audio"].lower() == "yes":
                newdata.append(i)
    else:
        for i in data:
            if (i["_Category"].lower() == cate.lower()) and (i["_Audio"] == "Yes"):
                newdata.append(i)
            else:
                pass
    return newdata


def get_aud(book):
    data = get_audjson()
    for i in data:
        if i["BookId"] == book:
            return i


def issued_book(bookid):
    data = get_json()
    for i in data:
        if i["_BookId"] == bookid.upper():
            i["_PresentAvail"] = str(int(i["_PresentAvail"]) - 1)
        else:
            pass
    updated_data = json.dumps(data, indent=13)
    write_json(updated_data)
    data2 = globalVariable.get_generaljson()
    print(data2)
    data2[1]["TotalIssueCount"] = str(
        int(data2[1]["TotalIssueCount"]) + 1).zfill(5)
    globalVariable.write_generaljson(data2)


def return_book(bookid):
    data = get_json()
    for i in data:
        if i["_BookId"] == bookid:
            i["_PresentAvail"] = str(int(i["_PresentAvail"]) + 1)
        else:
            pass
    updated_data = json.dumps(data, indent=13)
    write_json(updated_data)


def uniq_book():
    data = get_json()
    count = str(len(data)).zfill(5)
    return count


def total_book():
    data = get_json()
    count = 0
    for i in data:
        count = count + int(i["_TotalAvail"])
    return (str(count).zfill(5))


def addbooks(add_data):
    data = get_json()
    audData = get_audjson()
    new_dic = {}
    if add_data['Check it'] == "Yes":
        new_dic["_BookId"] = add_data["BookId"]
        new_dic["_BookTitle"] = add_data["BookName"]
        new_dic["_BookAuthor"] = add_data["Author"]
        new_dic["_Category"] = add_data["Category"]
        new_dic["_Description"] = add_data["BookDesp"]
        new_dic["_Edition"] = add_data["Edition"]
        new_dic["_ImgSrc"] = add_data["ImgSource"]
        new_dic["_ISBN"] = add_data["ISBN"]
        new_dic["_Location"] = add_data["Location"]
        new_dic["_TotalAvail"] = add_data["TotalAvail"]
        new_dic["_PresentAvail"] = add_data["TotalAvail"]
        new_dic["_Publications"] = add_data["Publication"]
        new_dic["_Year"] = add_data["Year"]
        new_dic["_Audio"] = add_data["Audio"]
        data.append(new_dic)
        updated_data = json.dumps(data, indent=13)
        write_json(updated_data)
        globalVariable.BookUpdate("Add")
        if add_data["Audio"] == "Yes":
            keys = list(data.keys())[6:-11]
            aud_dic = {}
            aud_dic["BookId"] = add_data["BookId"]
            aud_dic["BookTitle"] = add_data["BookName"]
            aud_dic["BookDescription"] = add_data["BookDesp"]
            aud_dic["BookAuthor"] = add_data["Author"]
            aud_dic["ImgSrc"] = add_data["ImgSource"]
            aud_dic["Category"] = add_data["Category"]
            if add_data["SingleFile"] == "Yes":
                aud_dic["ChapterWise"] = "No"
                aud_dic["SingleFile"] = "Yes"
            else:
                aud_dic["ChapterWise"] = "Yes"
                aud_dic["SingleFile"] = "No"
            audio = {}
            for i in range(0, add_data("Counts")):
                audio[add_data[keys[i +
                                    add_data("Counts")]]] = add_data[keys[i]]
            aud_dic["AudioFile"] = audio
            audData.append(aud_dic)
            update_data = json.dumps(audData, indent=5)
            write_audjson(update_data)

        return "Success"
    else:
        return "Failure"


def dropbooks(dropdata):
    data = get_json()
    audData = get_audjson()
    for i in data:
        if i["_BookId"] == dropdata["BookId"]:
            data.remove(i)
            break
        else:
            pass
    for i in audData:
        if i["BookId"] == dropdata["BookId"]:
            audData.remove(i)
            break
        else:
            pass
    updated_data = json.dumps(data, indent=5)
    write_json(updated_data)
    update_data = json.dumps(audData, indent=5)
    write_audjson(update_data)
    globalVariable.BookUpdate("Drop")
    return "Success"


def editbooks(editdata):
    data = get_json()
    for i in data:
        if i["_BookId"] == editdata["BookId"]:
            i["_BookId"] = editdata["BookId"]
            i["_BookTitle"] = editdata["BookName"]
            i["_BookAuthor"] = editdata["Author"]
            i["_Category"] = editdata["Category"]
            i["_Description"] = editdata["BookDesp"]
            i["_Edition"] = editdata["Edition"]
            i["_ImgSrc"] = editdata["ImgSource"]
            i["_ISBN"] = editdata["ISBN"]
            i["_Location"] = editdata["Location"]
            i["_TotalAvail"] = editdata["TotalAvail"]
            i["_PresentAvail"] = editdata["TotalAvail"]
            i["_Publications"] = editdata["Publication"]
            i["_Year"] = editdata["Year"]
            i["_Audio"] = editdata["Audio"]
        else:
            pass

    updated_data = json.dumps(data, indent=5)
    write_json(updated_data)
    globalVariable.BookUpdate("Edit")
    return "Success"
