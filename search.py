import json


def get_json():
    with open("./static/Books.json", "r") as read_it:
        data = json.load(read_it)
        read_it.close()
        return data


def getBooks(form_data):
    data = get_json()
    search_result = []
    exception = ["the", "of", "a", "an", "or", "for", "than", "and", "so", "i", "you", "are", "is", "to", "it",
                 "were", "was", "had", "have", "has", "will", "shall", "should", "would", "could", "can", "in", "on"]

    for i in data:
        if form_data["SearchBy"] == "Title":
            ByData = (i["_BookTitle"].lower()).split(" ")
            search = (form_data["SearchText"].lower()).split(" ")

        elif form_data["SearchBy"] == "Author":
            ByData = (i["_BookAuthor"].lower()).split(" ")
            search = (form_data["SearchText"].lower()).split(" ")

        elif form_data["SearchBy"] == "Publications":
            ByData = (i["_Publications"].lower()).split(" ")
            search = (form_data["SearchText"].lower()).split(" ")

        elif form_data["SearchBy"] == "ISBN":
            ByData = (i["_ISBN"].lower()).split(",")
            search = (form_data["SearchText"].lower()).split(",")

        elif form_data["SearchBy"] == "Edition":
            ByData = (i["_Edition"].lower())
            search = (form_data["SearchText"].lower()).split(" ")

        else:
            pass
        if " " in search:
            search.remove(" ")
        for index in search:
            if index in exception:
                search.remove(index)
        for see in ByData:
            if see in search:
                search_result.append(i)
                break
    return search_result
