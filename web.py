from flask import *
import dbms
import booksmanage
import globalVariable
import login_rule
import search

web = Flask(__name__)
web.secret_key = "LMSServices"

BookCategory = ["Programming", "Automotion",
                "Computer Science", "Math", "Fiction", "Economics", "Engineering", "Physics", "Business", "Environment", "Chemistry", "Biology", "History", "Motivational"]
BookCategory.sort()


@web.route("/")
def home():
    return render_template('index.html')


@web.route("/dashboard")
def dashbrd():
    return render_template('dashboard.html', state="Fail", role="Not")


@web.route('/login', methods=['post'])
def login():
    dic = {}
    datum = request.form
    dic['username'] = datum["username"]
    dic['password'] = datum["password"]
    dic['Role'] = datum["Role"]
    ret = login_rule.auth_Login(dic)
    if ret[0] == "Fail":
        return render_template('autherror.html')
    else:
        return render_template('success.html', content=["books", " Let's Get in ", "You authenticated successfully and you can continue it.", ret[0]], role=ret[1])


@web.route("/books")
def books():
    bookCount = booksmanage.get_total()
    data = dbms.get_json()
    return render_template('books.html', book=data, Cate="All", Count=bookCount, cate=BookCategory)


@web.route("/books/search", methods=['POST'])
def opensearch():
    fdata = request.form
    bookCount = booksmanage.get_total()
    data = search.getBooks(fdata)
    return render_template('books.html', book=data, Cate="All", Count=bookCount, cate=BookCategory)


@web.route("/books/<id>")
def catebook(id):
    if id == "All":
        data = dbms.get_json()
    else:
        data = dbms.get_cate(id)
    bookCount = booksmanage.get_total()
    return render_template('books.html', book=data, Cate=id, Count=bookCount, cate=BookCategory)


@web.route("/returnbooks")
def rtrn():
    return render_template('return.html')


@web.route("/issuebooks")
def issue():
    return render_template('issued.html')


@web.route("/issuebooks/done", methods=['POST'])
def issuedone():
    data = request.form
    booksmanage.Update_data(data)
    dbms.issued_book(str(data["BookId"]))
    return redirect(url_for('issue'))


@web.route("/returnbooks/done", methods=['POST'])
def rtrndone():
    data = request.form
    dbms.return_book(str(data["BookId"]))
    booksmanage.rtrnUpdate(data)
    return redirect(url_for('rtrn'))


@web.route("/modifybooks")
def modify():
    data = globalVariable.getlastseen()
    return render_template('modify.html', lastseen=data)


@web.route("/modifybooks/add")
def addbooks():
    return render_template('addbooks.html', cate=BookCategory)


@web.route("/modifybooks/remove")
def removebooks():
    return render_template('dropbooks.html')


@web.route("/modifybooks/edit")
def editbooks():
    return render_template('editbooks.html', cate=BookCategory)


@web.route("/modifybooks/add/success", methods=['POST'])
def adddone():
    data = request.form
    # return data
    # return render_template('addbooks.html', cate=BookCategory)
    result = dbms.addbooks(data)
    if result == "Success":
        res = "Book information was updated successfully"
    else:
        res = "Book information was not updated successfully"
    return render_template('success.html', content=["modify", "Go to modify page", res, result], role="admin")


@web.route("/modifybooks/remove/success", methods=['POST'])
def removedone():
    data = request.form
    result = dbms.dropbooks(data)
    if result == "Success":
        res = "Book was removed successfully"
    else:
        res = "Book was not removed successfully"

    return render_template('success.html', content=["modify", "Go to modify page", res, result], role="admin")


@web.route("/modifybooks/edit/success", methods=['POST'])
def editdone():
    data = request.form
    # return jsonify(data)
    result = dbms.editbooks(data)
    if result == "Success":
        res = "Book information was updated successfully"
    else:
        res = "Book information was not updated successfully"

    return render_template('success.html', content=["modify", "Go to modify page", res, result], role="admin")


@web.route("/audiobooks")
def audiobooks():
    data = dbms.get_audCate("All")
    return render_template('audiobooks.html', book=data, Cate="All", cate=BookCategory)


@web.route("/audiobooks/<id>")
def audcatebook(id):
    if id == "All":
        data = dbms.get_audCate("All")
    else:
        data = dbms.get_audCate(id)
    return render_template('audiobooks.html', book=data, Cate=id, cate=BookCategory)


@web.route("/audiobooks/book-<id>")
def audiobook(id):
    data = dbms.get_aud(id)
    return render_template('audiopage.html', book=data)


if __name__ == "__main__":
    web.run(host='0.0.0.0', debug=True)
