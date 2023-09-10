from flask import Flask, render_template, request,session,redirect
from database import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
init_db()

# Define admin username and password
ADMIN_USERNAME = "satish"
ADMIN_PASSWORD = "satish"  # Remember to replace with a secure password

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        session['username'] = username
        return redirect('/')
    else:
        return render_template('login.html', message='Invalid credentials')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('library.html', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='addBook')
    else:
        return redirect('/login')

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    available = request.form['available']

    if not title or not author or not genre or not available:
        return render_template('library.html', message='Please fill in all fields', books=get_all_books(),deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(), active_tab='addBook')
    else:
        add_book(title, author, genre,available)
        return render_template('library.html', message='Book added successfully', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='addBook')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_book(query)
    return render_template('library.html', search_results=results, books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='searchBook')

@app.route('/view_all')
def view_all():
    return render_template('library.html', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='viewAll')

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete(book_id):
    delete_book(book_id)
    return render_template('library.html', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='viewAll')

@app.route('/retrieveBooks')
def retrieveBooks():
    return render_template('library.html', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='retrieveBooks')

@app.route('/retrieve/<int:book_id>', methods=['POST'])
def retrieve(book_id):
    retrieve_book(book_id)
    return render_template('library.html',books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='viewAll')

@app.route('/retrieve_all', methods=['POST'])
def retrieve_all():
    retrieve_all_books()
    return render_template('library.html',books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='viewAll')

@app.route('/borrow', methods=['POST'])
def borrow():
    student_id  = request.form['studentID']
    student_name = request.form['studentName']
    book_id = request.form['bookID']

    if not student_id or not student_name or not book_id:
        return render_template('library.html', message='Please fill in all fields', books=get_all_books(),deleted_books=get_all_deleted_books(), borrowed_books=get_borrowed_books(),active_tab='borrowBook')
    else:
        success = borrow_book_to_student(student_id, student_name, book_id)
        if success:
            message = 'Book borrowed successfully'
        else:
            message = 'Book could not be borrowed'
        return render_template('library.html', message=message, books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),active_tab='borrowBook')


@app.route('/returnBook', methods=['POST'])
def return_book_route():
    return render_template('library.html', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),
                           active_tab='returnBook')

@app.route('/return/<int:brw_id>', methods=['POST'])
def returnbook(brw_id):
    return_book(brw_id)
    return render_template('library.html', books=get_all_books(), deleted_books=get_all_deleted_books(),borrowed_books=get_borrowed_books(),
                           active_tab='returnBook')

if __name__ == '__main__':
    app.run(debug=True)
