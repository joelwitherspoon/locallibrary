from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of hte main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of books per genre
    num_nonfiction = Book.objects.filter(genre__name='Non-Fiction').count()
    num_fiction = Book.objects.filter(genre__name='Fiction').count()
    num_satire = Book.objects.filter(genre__name='Satire').count()
    num_anthology = Book.objects.filter(genre__name='Anthology').count()
    num_fantasy = Book.objects.filter(genre__name='Fantasy').count()

    # The 'all' is implied
    num_authors = Author.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_nonfiction': num_nonfiction,
        'num_fiction': num_fiction,
        'num_satire': num_satire,
        'num_anthology': num_anthology,
        'num_fantasy': num_fantasy,
        'num_visits': num_visits,
    }

    # render the HTML template index.html with the correct context variable
    return render(request, 'catalog/index.html', context=context)


class BookListView(generic.ListView):
    """Book list"""
    model = Book
    # context_object_name  = 'my_book_list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # template_name = 'books/book_list.html'
    paginate_by = 3


class BookDetailView(generic.DetailView):
    """Detail view of a book"""
    model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
    """Book list"""
    model = Author
    # context_object_name  = 'my_book_list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # template_name = 'books/book_list.html'
    paginate_by = 3


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view of a book"""
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        """Restricts to on loan"""
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic list view of all on loan books"""
    permission_required = ('catalog.can_mark_returned')
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        """Restricts to on loan"""
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')