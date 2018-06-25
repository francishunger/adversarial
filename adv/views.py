# Create your views here.
# https://django-versatileimagefield.readthedocs.io/en/latest/

# dieser view greift zurück auf templates/home.html
# definiert in ../urls definiert als path(r'', home, name='home'),
from django.shortcuts import render, redirect

from django.core.files.storage import FileSystemStorage
from .models import adv, Document
from .forms import DocumentForm


def home(request):
    # Http Session
    if not request.session.session_key:
        request.session.save()
    sessionkey = request.session.session_key

    # Form Handling
    if request.method == 'POST' and request.FILES['somefile']:

        form = DocumentForm(request.POST or None)

        fs = FileSystemStorage()
        myfile = request.FILES['somefile']
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        context = {
            'uploaded_file_url': uploaded_file_url,
            'form': form,
            'sessionkey': sessionkey
        }

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            text = request.POST['text']
            sessionkey = request.session.session_key

            m = adv(title=title, text=text, sessionkey=sessionkey)

            m.document = form.cleaned_data['image']
            m.save()

            return redirect("index.html")

    #   Noch ohne Post – Nur Form anzeigen
    else:
        form = DocumentForm()

        context = {
            'form': form,
            'sessionkey': sessionkey
        }  # Variablen, die in index.html gerendert wird

    return render(request, "index.html", context)


# dieser view greift zurück auf urls.py
# definiert in ../urls als url(r'^adv/', include('adv.urls'), name='adv')
# benötigt adv/urls.py

# Übersichtsseite alle Objekte (10) übergeben
def index(request):
    advs = adv.objects.all()[:10]  # [:10] wie viele übernommen werden sollen
    context = {
        'advs': advs
    }  # Variablen, die in index.html gerendert wird

    return render(request, "adv/index.html", context)


# Detail
def details(request, id):
    adva = adv.objects.get(id=id)

    context = {
        'adva': adva
    }  # Variablen, die in details.html gerendert wird

    return render(request, "adv/details.html", context)


# Add
def add(request):
    if (request.method == 'POST'):
        title = request.POST['title']
        text = request.POST['text']

        out = adv(title=title, text=text)
        out.save()

        return redirect('/adv/')
    else:
        return render(request, "adv/add.html")
