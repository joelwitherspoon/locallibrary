import datetime
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm


# Create your views here.

#@login_required
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
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Detail view of a book"""
    model = Book


class AuthorListView(generic.ListView):
    """Author list"""
    model = Author
    # context_object_name  = 'my_book_list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    template_name = 'books/book_list.html'
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
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
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        """Restricts to on loan"""
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context=context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author


class AuthorCreate(CreateView):
    """Create an Author"""
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2019'}


class AuthorUpdate(UpdateView):
    """Update existing Author"""
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    """Deletes and Author"""
    model = Author
    success_url = reverse_lazy('authors')


from catalog.models import Book

class BookCreate(CreateView):
    """Create Book"""
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    """Update Book"""
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    """Delete Book"""
    model = Book
    success_url = reverse_lazy('book-detail')