from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, Recommender, BooksAlreadyRead, BooksWantRead
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date, datetime

# Create your views here.
@login_required
def create(request):
    if request.method == "POST":
        params = {'bookname':request.POST['bookname'],
                          'bookauthor':request.POST['bookauthor']}

        if Book.objects.filter(book_name=request.POST['bookname']).exists():
            params['book_id'] = Book.objects.get(book_name=request.POST['bookname']).id
            params['error_ex'] = "The book has already existed. More info about book"
            return render(request, 'books/create.html',params )

        else:
            if request.POST['bookname'] and request.POST['bookauthor']:
                book = Book()
                book.book_name = request.POST['bookname']
                book.book_author = request.POST['bookauthor']
                book.pub_date = timezone.datetime.now()
                book.user_name = request.user
                book.save()
                return redirect('/books/bookinfo/{}?success=book_created'.format(book.id))
            else:
                params['error'] = 'You need to write all information!'
                return render(request,'books/create.html', params)

    else:
        return render(request,'books/create.html')

vocabulary_home = {'signup':'You signed up successfully!',
                   'login':'You log in successfully!',
                   'addbook':'You added book successfully!'}
def home(request):
    books_list = Book.objects.order_by('-pub_date')

    page = request.GET.get('page', 1)
    paginator = Paginator(books_list, 5)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    params = {'books': books}
    params['success'] = vocabulary_home.get(request.GET.get('success'))
    return render(request,'books/home.html',params)

@login_required
def recommend(request,book_id):
    book = Book.objects.get(pk=book_id)
    if Recommender.objects.filter(book_id=book_id, user_id=request.user.id).exists():
        return redirect('/books/bookinfo/{}?error=already_recommended'.format(book_id))
    else:
        book.recommend_total += 1
        book.save()
        r = Recommender(user=request.user, book=book)
        r.save()
        return redirect('/books/bookinfo/{}?success=recommended'.format(book_id))


answers = {'already_recommended':'Sorry, this book is already recommended by you!',
           'recommended':'Thank you for recommendation!',
           'no_date':'Please, select the date',
           'add_to_already_read':'You\'ve added this book to list "Already read books"!',
           'add_to_want_read':'You\'ve added this book to list "Want to read books"!',
           'book_created':'You added the book! Add it to "Already read books" or "Want to read books" list'
           }
def bookinfo(request, book_id):
    book = Book.objects.get(pk=book_id)
    params = {'book': book}

    params['error'] = answers.get(request.GET.get('error'))
    params['success'] = answers.get(request.GET.get('success'))

    params['alreadyreadstatus'] = BooksAlreadyRead.objects.filter(book_id=book_id, user_id=request.user.id).exists()
    params['wantreadstatus'] = BooksWantRead.objects.filter(book_id=book_id, user_id=request.user.id).exists()
    params['recommended'] = Recommender.objects.filter(book_id=book_id, user_id=request.user.id).exists()
    return render(request, 'books/bookinfo.html', params)


def mybooks(request):
    books_list = Book.objects.filter(booksalreadyread__user=request.user).\
        values('id','book_name', 'book_author', 'book_comment', 'booksalreadyread__read_at').order_by('-booksalreadyread__read_at')


    page = request.GET.get('page', 1)
    paginator = Paginator(books_list, 5)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    for book in books:
        book['read_at_pretty'] = book['booksalreadyread__read_at'].strftime('%b %Y')
    return render(request,'books/mybooks.html', {'books':books})


@login_required
def addAlreadyReadBook(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.POST.get('comment'):
        book.book_comment = request.POST['comment']
        book.save()
    if request.POST['datealreadyread']:
        if BooksAlreadyRead.objects.filter(book_id=book_id, user_id=request.user.id).exists():
            redirect('home')
        else:
            a = BooksAlreadyRead(user=request.user, book=book, read_at=datetime.strptime(request.POST['datealreadyread'], '%Y-%m').date())
            a.save()

            if BooksWantRead.objects.filter(book_id=book_id, user_id=request.user.id).exists():
                BooksWantRead.objects.filter(book_id=book_id, user_id=request.user.id).delete()
            return redirect('/books/bookinfo/{}?success=add_to_already_read'.format(book_id))

    else:
        return redirect('/books/bookinfo/{}?error=no_date'.format(book_id))


@login_required
def add_want_to_read(request, book_id):
    book = Book.objects.get(pk=book_id)
    if BooksAlreadyRead.objects.filter(book_id=book_id, user_id=request.user.id).exists():
        redirect('home')
    else:
        w = BooksWantRead(user=request.user, book=book, priority=request.POST['priority'])
        w.save()
        return redirect('/books/bookinfo/{}?success=add_to_want_read'.format(book_id))



def want_to_read(request):
    books_list = Book.objects.filter(bookswantread__user=request.user).\
        values('id','book_name', 'book_author', 'book_comment', 'bookswantread__priority').order_by('-bookswantread__priority')

    page = request.GET.get('page', 1)
    paginator = Paginator(books_list, 5)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request,'books/wanttoread.html', {'books': books})


