from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import Book, User

###########RENDERED WEB PAGES########################
def index(request):
    return render(request, 'login.html')

def all_books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    all_books = Book.objects.all()
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'user' : this_user,
        'books' : all_books,
    }
    return render(request, 'all_books.html', context)

def specific_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'book' : Book.objects.get(id=book_id),
        'user' : User.objects.get(id= request.session['user_id']),
        'users' : User.objects.all(),
    }
    return render(request, 'specific_book.html', context)

def specific_user(request, member_id):
    if 'user_id' not in request.session:
        return redirect('/')
    count = 0
    the_user = User.objects.get(id=member_id)
    for book in the_user.books_uploaded.all():
        count += 1
    context = {
        'number' : count,
        'user' : the_user,
    }
    return render(request, 'specific_user.html', context)
###########RENDERED WEB PAGES########################
###########LOGIN AND REGISTRATION####################
def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    pw_hash = bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
    )
    request.session['user_id'] = new_user.id
    return redirect('/books')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.loginval(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email = request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')
###########LOGIN AND REGISTRATION####################
###########CREATE EDIT AND DELETE BOOKS##############
def create_book(request):
    if request.method == 'POST':
        errors = Book.objects.validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/books')
        curr_user = User.objects.get(id = request.session['user_id'])
        new_book = Book.objects.create(
            title = request.POST['title'],
            author = request.POST['author'],
            description = request.POST['desc'],
            uploaded_by = curr_user,
        )
        new_book.favorited_by.add(curr_user)
        return redirect(f'/books/{new_book.id}')
    return redirect('/')

def edit_book(request, book_id):
    if request.method == 'POST':
        errors = Book.objects.validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect(f'/books/{book_id}')
        curr_book = Book.objects.get(id=book_id)
        curr_book.title = request.POST['title']
        curr_book.author = request.POST['author']
        curr_book.description = request.POST['desc']
        curr_book.save()
        return redirect('/books')
    return redirect(f'/books/{book_id}')

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')
###########CREATE EDIT AND DELETE BOOKS##############
################LIKE & UNLIKE########################

def favorite_book(request, book_id):
    curr_book = Book.objects.get(id=book_id)
    curr_user = User.objects.get(id = request.session['user_id'])
    curr_book.favorited_by.add(curr_user)
    return redirect(f'/books/{book_id}')

def remove_fave(request, book_id):
    curr_book = Book.objects.get(id=book_id)
    curr_user = User.objects.get(id= request.session['user_id'])
    curr_book.favorited_by.remove(curr_user)
    curr_book.save()
    return redirect(f'/books/{book_id}')
################LIKE & UNLIKE########################