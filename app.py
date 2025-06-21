from flask import Flask, render_template, request, redirect, url_for, session
from google_sheet import get_all_books, add_book, update_book, delete_book
from auth import get_user_role
import os
app = Flask(__name__, template_folder='templates', static_folder='styles')

app.secret_key = 'super-secret-key'  

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        role = get_user_role(username)
        if role == 'admin':
            return redirect(url_for('admin', user=username))
        elif role == 'user':
            return redirect(url_for('user', user=username))
        else:
            return render_template('login.html', error="Unauthorized user.")
    return render_template('login.html')

@app.route('/admin/<user>', methods=['GET', 'POST'])
def admin(user):
    message = ""
    books = get_all_books()

    if request.method == 'POST':
        action = request.form['action']
        book = request.form['book']

        if action == 'confirm_increase':
            try:
                count = int(request.form['count'])
            except ValueError:
                count = 0

            for b in books:
                if b['Book'].lower() == book.lower():
                    new_count = b['Availability'] + count
                    update_book(book, new_count)
                    message = f"Availability of '{book}' increased to {new_count}."
                    break

        else:
            try:
                count = int(request.form['count'])
            except ValueError:
                count = 0

            existing = next((b for b in books if b['Book'].lower() == book.lower()), None)

            if action == 'add':
                if existing:
                    session['pending_book'] = book
                    message = f"'{book}' already exists. Enter how many more to add and click Confirm."
                elif action =='go_back':
                    return render_template('admin.html')
                else:
                     added = add_book(book, count)
                     message = f"Book '{book}' added." if added else "❌ Invalid Input"

            elif action == 'update':
                updated = update_book(book, count)
                message = f"Book '{book}' updated." if updated else "❌ Book not found or Invalid Input."

            elif action == 'delete':
                success = delete_book(book)
                message = f"Book '{book}' deleted." if success else "❌ Book not found."

    
        books = get_all_books()

    return render_template(
        'admin.html',
        user=user,
        books=books,
        message=message,
        pending_book=session.pop('pending_book', None) if 'pending_book' in session else None
    )
@app.route('/user/<user>', methods=['GET', 'POST'])
def user(user):
    message = ""
    if 'borrowed_books' not in session:
        session['borrowed_books'] = {}

    borrowed_books = session['borrowed_books']
    books = get_all_books()

    if request.method == 'POST':
        book = request.form['book']
        action = request.form['action']

        for b in books:
            if b['Book'].lower() == book.lower():
                if action == 'borrow':
                    if b['Availability'] > 0:
                        update_book(book, b['Availability'] - 1)
                        borrowed_books[book] = borrowed_books.get(book, 0) + 1
                        session['borrowed_books'] = borrowed_books

                        message = f"You borrowed '{book}'."
                    else:
                        message = f"'{book}' is currently not available."
                

                elif action == 'return':
                    if borrowed_books.get(book, 0) > 0:
                        update_book(book, b['Availability'] + 1)

                        borrowed_books[book] -= 1
                        if borrowed_books[book] == 0:
                            del borrowed_books[book]
                        session['borrowed_books'] = borrowed_books

                        message = f"You returned '{book}'."
                    else:
                        message = "You cannot return a book you haven't borrowed."
                break
        else:
            message = "Book not found."

        books = get_all_books()

    return render_template(
        'user.html',
        user=user,
        books=books,
        message=message,
        borrowed=borrowed_books
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)