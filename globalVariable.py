import time
import json
import dbms
import datetime


def get_generaljson():
    with open("./static/GeneralData.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def write_generaljson(data):
    updated = json.dumps(data, indent=8)
    with open("./static/GeneralData.json", "w") as write_it:
        write_it.write(updated)
        write_it.close()


def get_ConstIdjson():
    with open("./static/Returned_ConstID.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def Write_ConstIdjson(updata):
    data = json.dumps(updata, indent=2)
    with open("./static/Returned_ConstID.json", "w") as write_it:
        write_it.write(data)
        write_it.close()


def get_time():
    CurrentTime = {}
    Cur_Time = time.ctime().split(" ")
    # Cur_Time.remove('')
    CurrentTime['Day'] = Cur_Time[0]
    CurrentTime['Date'] = Cur_Time[2]
    CurrentTime['Month'] = Cur_Time[1]
    CurrentTime['Year'] = Cur_Time[4]
    CurrentTime['Cur_Time'] = Cur_Time[3]
    return CurrentTime


def get_Month():
    curtime = get_time()
    Months = ["Month", "Jan", "Feb", "Mar", "Apr", "May",
              "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return Months.index(curtime['Month'])


def updatejson():
    data = get_generaljson()
    today = get_time()['Day']
    if data[0]["Today"] != today:
        data[0]["Today"] = today
        data[0]["PrevIssueCount"] = data[0]["IssueCount"]
        data[0]["IssueCount"] = "0".zfill(5)
        data[0]["PrevReturnCount"] = data[0]["ReturnCount"]
        data[0]["ReturnCount"] = "0".zfill(5)
        write_generaljson(data)
    else:
        pass


def get_incr(token):
    updatejson()
    data = get_generaljson()
    today = get_time()['Day']
    if data[0]["Today"] == today:
        if token == 1:
            data[0]["IssueCount"] = str(
                int(data[0]["IssueCount"]) + 1).zfill(5)
            data[0]["Const_Issue_Id"] = str(
                int(data[0]["Const_Issue_Id"])+1).zfill(7)
            write_generaljson(data)
            return data[0]["IssueCount"]
        else:
            data[0]["ReturnCount"] = str(
                int(data[0]["ReturnCount"]) + 1).zfill(5)
            write_generaljson(data)
            return data[0]["ReturnCount"]


def generate_IssueId():
    data = get_time()
    month = get_Month()
    ids = 'ISE/' + data["Year"] + '/' + \
        str(month).zfill(2) + '/' + data["Date"]+"/" + get_incr(1)
    return ids


def generate_ReturnId():
    data = get_time()
    month = get_Month()
    ids = 'RTN/' + data["Year"] + '/' + \
        str(month).zfill(2) + '/' + data["Date"]+"/" + get_incr(0)
    return ids


def get_datetime():
    data = get_time()
    datetime = data["Date"] + '/' + data["Month"] + \
        '/' + data["Year"]+" " + data["Cur_Time"]
    return datetime


def get_DateTime():
    data = get_time()
    datetime = data["Month"] + ' ' + data["Date"] + \
        ', ' + data["Year"]+" " + data["Cur_Time"]
    return datetime


def get_dues():
    Returning_Dues = 15
    current_date = datetime.date.today()
    return str(current_date + datetime.timedelta(days=Returning_Dues))


def update_fines(rtndate):
    fines = 2
    date = get_time()
    retrndate = rtndate.split("-")
    rtrndate = datetime.datetime(int(retrndate[0]), int(
        retrndate[1]), int(retrndate[2]), 0, 0, 0)
    Current = datetime.datetime(int(date["Year"]), int(
        get_Month()), int(date["Date"]), 0, 0, 0)
    if int(date["Date"]) != int(retrndate[2]) and int(get_Month()) != int(retrndate[1]):
        remains = float(str(rtrndate - Current).split(",")[0].split(" ")[0])
    else:
        remains = 0.0

    if remains < 0:
        FineAmount = fines * remains * (-1)
    else:
        FineAmount = 0.0
    return str(FineAmount)


def get_dic(data):
    constid = get_ConstIdjson()
    dic = {}
    dic["Issue_id"] = generate_IssueId()
    dic["Const_Issue_Id"] = get_generaljson()[0]["Const_Issue_Id"]
    if dic["Const_Issue_Id"] not in constid[0]["Not_Yet"]:
        constid[0]["Not_Yet"].append(dic["Const_Issue_Id"])
    else:
        pass
    Write_ConstIdjson(constid)
    dic["Return_id"] = "Not Yet"
    dic["BookId"] = str(data["BookId"])
    dic["RollNo"] = str(data["RollNo"])
    dic["IssuedTime"] = get_datetime()
    dic["ReturningTime"] = get_dues()
    dic["ReturnedTime"] = "Not Yet"
    dic["Fines_Charges"] = "0.0"
    return dic


def get_rtrnUpdate(data, base):
    constid = get_ConstIdjson()
    BookID = str(data["BookId"])
    Roll = str(data["RollNo"])
    fine = 0.0
    for i in base:
        if i["Return_id"] == "Not Yet" and i["BookId"] == BookID and i["RollNo"] == Roll:
            i["ReturnedTime"] = get_datetime()
            i["Fines_Charges"] = update_fines(str(i["ReturningTime"]))
            i["Return_id"] = generate_ReturnId()
            constid[0]["Not_Yet"].remove(i["Const_Issue_Id"])
            constid[0]["Returned"].append(i["Const_Issue_Id"])
            Write_ConstIdjson(constid)
            fine = float(i["Fines_Charges"])
            break
        else:
            pass
    return base, fine


def Update_total():
    updatejson()
    data = get_generaljson()
    data[1]["Total_Books"] = dbms.total_book()
    data[1]["Unique_Books"] = dbms.uniq_book()
    write_generaljson(data)


def BookUpdate(Msg):
    data = get_generaljson()
    if Msg == "Add":
        data[2]["LastAddon"] = get_DateTime()
    elif Msg == "Edit":
        data[2]["LastModify"] = get_DateTime()
    elif Msg == "Drop":
        data[2]["LastDrop"] = get_DateTime()
    else:
        pass
    write_generaljson(data)


def getlastseen():
    return get_generaljson()[2]
