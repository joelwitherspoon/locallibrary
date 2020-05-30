from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


# Register your models here.

class BooksInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


# Book admin class
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    inlines = [BooksInstanceInLine]


# register
# admin.site.register(Book, BookAdmin)


# Author admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fieldsets = (
        (None, {
            'fields': [('first_name', 'last_name')]
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': ('date_of_birth', 'date_of_death')
        })
    )

    inlines = [BooksInline]
    # register the class


# admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)


# Book Instance class
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """ Book Instance"""
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'borrower', 'due_back')
        })
    )

# admin.site.register(BookInstance, BookInstanceAdmin)
