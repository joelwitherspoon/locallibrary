"""Models for the catalog app"""
from django.db import models
import uuid  # Required for book instances
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


# Create your models here.


class Genre(models.Model):
    """Genre Model - Represents a Book Genra"""

    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction")')

    def __str__(self):
        """Represents Genre"""
        return self.name


class BookInstance(models.Model):
    """Book Instance Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across '
                                                                          'whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        app_label = 'catalog'
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing Model object."""
        return f'{self.id} ({self.book.title})'

    def book_language(self):
        """Displays Book language"""
        book_language = self.book.language
        return f'{book_language}'

        book_language.short_description = 'Language'

    @property
    def is_overdue(self):
        """Is it overdue"""
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Book(models.Model):
    """Book Model"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Characters <a href="https://www.isbn-international'
                                                             '.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this book')
    iso_639_1 = (('ab', 'Abkhaz'),
                 ('aa', 'Afar'),
                 ('af', 'Afrikaans'),
                 ('ak', 'Akan'),
                 ('sq', 'Albanian'),
                 ('am', 'Amharic'),
                 ('ar', 'Arabic'),
                 ('an', 'Aragonese'),
                 ('hy', 'Armenian'),
                 ('as', 'Assamese'),
                 ('av', 'Avaric'),
                 ('ae', 'Avestan'),
                 ('ay', 'Aymara'),
                 ('az', 'Azerbaijani'),
                 ('bm', 'Bambara'),
                 ('ba', 'Bashkir'),
                 ('eu', 'Basque'),
                 ('be', 'Belarusian'),
                 ('bn', 'Bengali'),
                 ('bh', 'Bihari'),
                 ('bi', 'Bislama'),
                 ('bs', 'Bosnian'),
                 ('br', 'Breton'),
                 ('bg', 'Bulgarian'),
                 ('my', 'Burmese'),
                 ('ca', 'Catalan; Valencian'),
                 ('ch', 'Chamorro'),
                 ('ce', 'Chechen'),
                 ('ny', 'Chichewa; Chewa; Nyanja'),
                 ('zh', 'Chinese'),
                 ('cv', 'Chuvash'),
                 ('kw', 'Cornish'),
                 ('co', 'Corsican'),
                 ('cr', 'Cree'),
                 ('hr', 'Croatian'),
                 ('cs', 'Czech'),
                 ('da', 'Danish'),
                 ('dv', 'Divehi; Maldivian;'),
                 ('nl', 'Dutch'),
                 ('dz', 'Dzongkha'),
                 ('en', 'English'),
                 ('eo', 'Esperanto'),
                 ('et', 'Estonian'),
                 ('ee', 'Ewe'),
                 ('fo', 'Faroese'),
                 ('fj', 'Fijian'),
                 ('fi', 'Finnish'),
                 ('fr', 'French'),
                 ('ff', 'Fula'),
                 ('gl', 'Galician'),
                 ('ka', 'Georgian'),
                 ('de', 'German'),
                 ('el', 'Greek, Modern'),
                 ('gn', 'Guaraní'),
                 ('gu', 'Gujarati'),
                 ('ht', 'Haitian'),
                 ('ha', 'Hausa'),
                 ('he', 'Hebrew (modern)'),
                 ('hz', 'Herero'),
                 ('hi', 'Hindi'),
                 ('ho', 'Hiri Motu'),
                 ('hu', 'Hungarian'),
                 ('ia', 'Interlingua'),
                 ('id', 'Indonesian'),
                 ('ie', 'Interlingue'),
                 ('ga', 'Irish'),
                 ('ig', 'Igbo'),
                 ('ik', 'Inupiaq'),
                 ('io', 'Ido'),
                 ('is', 'Icelandic'),
                 ('it', 'Italian'),
                 ('iu', 'Inuktitut'),
                 ('ja', 'Japanese'),
                 ('jv', 'Javanese'),
                 ('kl', 'Kalaallisut'),
                 ('kn', 'Kannada'),
                 ('kr', 'Kanuri'),
                 ('ks', 'Kashmiri'),
                 ('kk', 'Kazakh'),
                 ('km', 'Khmer'),
                 ('ki', 'Kikuyu, Gikuyu'),
                 ('rw', 'Kinyarwanda'),
                 ('ky', 'Kirghiz, Kyrgyz'),
                 ('kv', 'Komi'),
                 ('kg', 'Kongo'),
                 ('ko', 'Korean'),
                 ('ku', 'Kurdish'),
                 ('kj', 'Kwanyama, Kuanyama'),
                 ('la', 'Latin'),
                 ('lb', 'Luxembourgish'),
                 ('lg', 'Luganda'),
                 ('li', 'Limburgish'),
                 ('ln', 'Lingala'),
                 ('lo', 'Lao'),
                 ('lt', 'Lithuanian'),
                 ('lu', 'Luba-Katanga'),
                 ('lv', 'Latvian'),
                 ('gv', 'Manx'),
                 ('mk', 'Macedonian'),
                 ('mg', 'Malagasy'),
                 ('ms', 'Malay'),
                 ('ml', 'Malayalam'),
                 ('mt', 'Maltese'),
                 ('mi', 'Māori'),
                 ('mr', 'Marathi (Marāṭhī)'),
                 ('mh', 'Marshallese'),
                 ('mn', 'Mongolian'),
                 ('na', 'Nauru'),
                 ('nv', 'Navajo, Navaho'),
                 ('nb', 'Norwegian Bokmål'),
                 ('nd', 'North Ndebele'),
                 ('ne', 'Nepali'),
                 ('ng', 'Ndonga'),
                 ('nn', 'Norwegian Nynorsk'),
                 ('no', 'Norwegian'),
                 ('ii', 'Nuosu'),
                 ('nr', 'South Ndebele'),
                 ('oc', 'Occitan'),
                 ('oj', 'Ojibwe, Ojibwa'),
                 ('cu', 'Old Church Slavonic'),
                 ('om', 'Oromo'),
                 ('or', 'Oriya'),
                 ('os', 'Ossetian, Ossetic'),
                 ('pa', 'Panjabi, Punjabi'),
                 ('pi', 'Pāli'),
                 ('fa', 'Persian'),
                 ('pl', 'Polish'),
                 ('ps', 'Pashto, Pushto'),
                 ('pt', 'Portuguese'),
                 ('qu', 'Quechua'),
                 ('rm', 'Romansh'),
                 ('rn', 'Kirundi'),
                 ('ro', 'Romanian, Moldavan'),
                 ('ru', 'Russian'),
                 ('sa', 'Sanskrit (Saṁskṛta)'),
                 ('sc', 'Sardinian'),
                 ('sd', 'Sindhi'),
                 ('se', 'Northern Sami'),
                 ('sm', 'Samoan'),
                 ('sg', 'Sango'),
                 ('sr', 'Serbian'),
                 ('gd', 'Scottish Gaelic'),
                 ('sn', 'Shona'),
                 ('si', 'Sinhala, Sinhalese'),
                 ('sk', 'Slovak'),
                 ('sl', 'Slovene'),
                 ('so', 'Somali'),
                 ('st', 'Southern Sotho'),
                 ('es', 'Spanish; Castilian'),
                 ('su', 'Sundanese'),
                 ('sw', 'Swahili'),
                 ('ss', 'Swati'),
                 ('sv', 'Swedish'),
                 ('ta', 'Tamil'),
                 ('te', 'Telugu'),
                 ('tg', 'Tajik'),
                 ('th', 'Thai'),
                 ('ti', 'Tigrinya'),
                 ('bo', 'Tibetan'),
                 ('tk', 'Turkmen'),
                 ('tl', 'Tagalog'),
                 ('tn', 'Tswana'),
                 ('to', 'Tonga'),
                 ('tr', 'Turkish'),
                 ('ts', 'Tsonga'),
                 ('tt', 'Tatar'),
                 ('tw', 'Twi'),
                 ('ty', 'Tahitian'),
                 ('ug', 'Uighur, Uyghur'),
                 ('uk', 'Ukrainian'),
                 ('ur', 'Urdu'),
                 ('uz', 'Uzbek'),
                 ('ve', 'Venda'),
                 ('vi', 'Vietnamese'),
                 ('vo', 'Volapük'),
                 ('wa', 'Walloon'),
                 ('cy', 'Welsh'),
                 ('wo', 'Wolof'),
                 ('fy', 'Western Frisian'),
                 ('xh', 'Xhosa'),
                 ('yi', 'Yiddish'),
                 ('yo', 'Yoruba'),
                 ('za', 'Zhuang, Chuang'),
                 ('zu', 'Zulu'),)
    language = models.CharField(
        max_length=2,
        choices=iso_639_1,
        blank=True,
        default='en',
        help_text='Languages'
    )

    def __str__(self):
        """Represents Book"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model"""
        return reverse('catalog:book-detail', args=[str(self.id)])

    def display_genre(self):
        """Creates a 3 char string for genre"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class Author(models.Model):
    """Authors Model"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance"""
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the model object"""
        return f'{self.last_name}, {self.first_name}'
