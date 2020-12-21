from django.db import models
import re
from django.contrib import messages
import bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must contain 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must contain 2 characters"
        if len(postData['pword']) < 8:
            errors['pword'] = "Password must contain 8 characters"
        if postData['pword'] != postData['pword_confirm']:
            errors['pword_confirm'] = "Passwords do not match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address!")
        return errors
    
    def loginval(self, postData):
        errors = {}
        all_users = User.objects.all()
        all_emails = []
        for user in all_users:
            all_emails.append(user.email)
        if postData['email'] not in all_emails:
            errors['email'] = "Email is not recognized, please register"
        
        if postData['email'] in all_emails:
            user = User.objects.filter(email= postData['email'])
            if bcrypt.checkpw(postData['pword'].encode(), user[0].password.encode()) == False:
                errors['pword'] = "Password is not correct"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}
        books_in_db = Book.objects.all()
        for title in books_in_db:
            if title == postData['title']:
                errors['title'] = "This book is already in the database"
        if len(postData['title']) < 5:
            errors['title'] = "Title must contain 5 characters"
        if len(postData['desc']) < 20:
            errors['desc'] = "Description must contain 20 characters"
        if len(postData['author']) < 5:
            errors['author'] = "Author must contain 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    author = models.CharField(max_length=40, default="Stephen King")
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
