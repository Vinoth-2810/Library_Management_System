import requests
from bs4 import BeautifulSoup, Tag

def get_news():
    URL = "https://timesofindia.indiatimes.com/briefs"
    con = requests.get(URL)
    soup = BeautifulSoup(con.text,"html.parser")
    # content = soup.find("div", {"id": "content"})
    content = soup.find(class_="briefs_outer")
    # single = content.find_all("div", {"class": "brief_box"})
    # print(content.prettify())
    header = content.find_all('h2')
    paragraph = content.find_all('p')
    img = content.find_all('img')
    titles = content.find_all('span',{"class":"subsection_card"})
    heading = []
    text = []
    titleList = []
    src = []
    for head,cont,title,imgsrc in zip(header,paragraph,titles,img):
        heading.append(head.text)
        text.append(cont.text)
        src.append(imgsrc['data-src'])
        if title.text == "":
            titleList.append("Others")
        else:
            titleList.append(title.text)

   
    uniq = ["India", "World", "Sports", "Business", "Others"]
    newsContent = {}
    for uniqtitle in uniq:
        dic = {}
        for header,paragraph,title,img in zip(heading,text,titleList,src):
            new = {}
            if title == uniqtitle:
                new['Content'] = paragraph
                new['Imgsrc'] = img
                dic[header] = new
            else:
                pass
        newsContent[uniqtitle] = dic
    return newsContent
