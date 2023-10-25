import json
import globalVariable


def get_IssueRtnjson():
    with open("./static/Issued_Return_Data.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def Write_IssueRtnjson(updata):
    data = json.dumps(updata, indent=9)
    with open("./static/Issued_Return_Data.json", "w") as write_it:
        write_it.write(data)
        write_it.close()


def Update_data(data):
    dic = globalVariable.get_dic(data)
    base = get_IssueRtnjson()
    base.append(dic)
    Write_IssueRtnjson(base)


def rtrnUpdate(data):
    base = get_IssueRtnjson()
    Update_base = globalVariable.get_rtrnUpdate(data, base)
    Write_IssueRtnjson(Update_base)


def get_total():
    globalVariable.Update_total()
    data = globalVariable.get_generaljson()
    Total = str(data[1]["Total_Books"])
    Unique = str(data[1]["Unique_Books"])
    IsCount = str(data[1]["TotalIssueCount"])
    ToIssue = str(data[0]["IssueCount"])
    PrevIssue = str(data[0]["PrevIssueCount"])
    return Total, Unique, IsCount, ToIssue, PrevIssue
