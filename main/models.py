import os
from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.utils.text import slugify
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from unidecode import unidecode
from .validators import validate_svg





class Genero(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    seotext = models.TextField(max_length=1200, null=True, blank=True)
    genero_image = models.FileField(upload_to="img/generos/", null=True, blank=False, validators=[validate_svg])
    created  = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.id:
            self.created = now()
        self.modified = now() 
        super(Genero, self).save(*args, **kwargs)    

    def get_absolute_url(self):
        return f'/categoria/{self.name}/'



# Create your models here.
class Ebook(models.Model):
    """clase de libro eboko"""
    id = models.IntegerField(primary_key=True)
    autor = models.CharField(max_length=200, null=True)
    genero = models.CharField(max_length=200, null=True)
    categoria = models.ForeignKey(Genero, on_delete=models.CASCADE, default=1)
    idioma = models.CharField(max_length=200, null=True)
    ilink = models.CharField(max_length=200, null=True)
    paginas = models.CharField(max_length=200, null=True)
    publicado = models.CharField(max_length=200, null=True)
    sinopsis = models.CharField(max_length=800, null=True)
    sinopsis_unidecode = models.CharField(max_length=800, null=True)
    titulo = models.CharField(max_length=200, null=True)
    pdf = models.CharField(max_length=200, null=True)
    epub = models.CharField(max_length=200, null=True)
    mobi = models.CharField(max_length=200, null=True)
    precio = models.IntegerField()
    unidecode_titulo = models.CharField(max_length=200, null=True)
    unidecode_genero = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    autor_slug = models.SlugField(max_length=200, null=True, blank=True)
    totalgenero = models.IntegerField(blank=True, null=True)
    tags = models.CharField(max_length=200, null=True)
    created  = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    	


    # pdffile = models.FileField(
    #     upload_to=settings.PDF_MEDIA_URL,
    #     storage=FileSystemStorage(
    #         location=settings.MEDIA_ROOT,
    #         base_url=os.path.join(settings.MEDIA_URL, settings.PDF_MEDIA_URL)
    #     ), null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.titulo) if self.precio else ''



    def __unicode__(self):
        return self.titulo



    def get_count(self):
        genders = Ebook.objects.values_list("genero", flat=True).distinct(
        ).order_by("genero")
        ammount = {}
        for a in genders:
            if a == self.genero:
               count = Ebook.objects.filter(genero = a).count()
               return count




    def save(self, *args, **kwargs):
        # self.slug = slugify(self.titulo)
        # self.pdffile = unidecode(str(self.titulo)) + ".pdf"
        # self.autor = unidecode(str(self.autor))
        # self.unidecode_titulo = unidecode(str(self.titulo))
        # self.unidecode_genero = unidecode(str(self.genero))
        # self.unidecode_sinopsis = unidecode(str(self.sinopsis))
        # self.totalgenero = self.get_count() 
        # Tracker.save(self)
        # self.slug_autor = slugify(self.autor)
        if not self.id:
            self.created = now()
        self.modified = now() 
        super(Ebook, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/descargar-{self.slug}-{self.autor_slug}/{self.id}/'
