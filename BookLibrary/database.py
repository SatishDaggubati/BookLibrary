import sqlite3

def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books
        (id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        genre TEXT,
        available INTEGER,
        deleted INTEGER DEFAULT 0,
        borrowed INTEGER DEFAULT 0)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS borrowings
        (brw_id INTEGER PRIMARY KEY,
        book_id INTEGER,
        student_id INTEGER,
        student_name TEXT,
        FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT)
        ''')
    conn.commit()
    conn.close()

def add_book(title, author, genre,available):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO books (title, author, genre,available)
        VALUES (?, ?, ?,?)
    ''', (title, author, genre,available))
    conn.commit()
    conn.close()


def get_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE deleted = 0')
    books = c.fetchall()
    conn.close()
    return books


def search_book(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE deleted = 0 AND (title LIKE ? OR author LIKE ? OR genre LIKE ?)',
              ('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    books = c.fetchall()
    conn.close()
    return books


def view_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    return books

def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE books SET deleted = 1 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def get_all_deleted_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE deleted = 1')
    books = c.fetchall()
    conn.close()
    return books

def retrieve_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE books SET deleted = 0 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def retrieve_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE books SET deleted = 0')
    conn.commit()
    conn.close()


def borrow_book_to_student(student_id, student_name, book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE id=? AND deleted=0', (book_id,))
    book = c.fetchone()
    if book:
        if book[4]>0:
            c.execute('INSERT INTO borrowings (book_id, student_id,student_name) VALUES (?, ?,?)', (book_id, student_id,student_name))
            c.execute('UPDATE books SET borrowed=1,available=available-1 WHERE id=?',(book_id,))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False


def return_book(brw_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE books SET borrowed=0, available=available+1 WHERE id=(SELECT book_id from borrowings where brw_id=?)', (brw_id,))
    c.execute('DELETE FROM borrowings WHERE brw_id=?', (brw_id,))
    conn.commit()
    conn.close()


def get_borrowed_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM borrowings')
    result = c.fetchall()
    conn.close()
    return result

