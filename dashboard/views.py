from re import X
from django.shortcuts import get_object_or_404, redirect, render
from instaloader import Post
from jmespath import search
from matplotlib.pyplot import text
from matplotlib.style import context
from .models import Notes, Homework, Todo
from .forms import ConversionForm, ConversionLengthForm, ConversionMassForm, HomeworkForm, NotesForm, TodoForm, YoutubeForm
from django.contrib import messages
from youtubesearchpython import VideosSearch
import requests
import wikipedia
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home_view(request):
    context = {}
    return render(request, "dashboard/home.html", context)

@login_required
def notes_view(request):
    form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("/notes")
        messages.success(request, f"Notes added from {request.user.username} successfully")
    else:
        form = NotesForm()
    context={
        "notes" : notes,
        "form" : form
    }
    return render(request, "dashboard/notes.html", context)

def Note_delete_view(request, id):
    Notes.objects.get(id=id).delete()
    return redirect("notes")

def Note_detail(request, id):
    obj = Notes.objects.get(id=id)
    context = {
        "obj" : obj
    }
    return render(request, "dashboard/notes_detail.html", context)

@login_required
def homework_view(request):
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    homework_form = HomeworkForm()
    if request.method == "POST":
        homework_form = HomeworkForm(request.POST or None)
        if homework_form.is_valid():
            try:
                finished = request.POST["Is_Finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework_form.instance.user = request.user
            homework_form.save()
            return redirect("homework")
        messages.success(request, f"Homework added from {request.user.username} successfully")
    else:
        homework_form = HomeworkForm()
    context = {
        "homework":homework,
        "homeworkdone":homework_done,
        "homeworkforms":homework_form
    }
    return render(request, "dashboard/homework.html", context)

def update_homework(request, id):
    homework = Homework.objects.get(id=id)
    if homework.Is_Finished == True:
        homework.Is_Finished = False
    else:
        homework.Is_Finished = True
    homework.save()
    return redirect("homework")

def delete_homework(request, id):
    Homework.objects.get(id=id).delete()
    return redirect("homework")

def youtube_view(request):
    if request == "POST":
        youtubeform = YoutubeForm(request.POST or None)
        search = request.POST['search']
        video = VideosSearch(search,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':search,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['search']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                "form":youtubeform,
                "results":result_list
            }
        return render(request, "dashboard/youtube.html", context)
    else:
        youtubeform = YoutubeForm()
    context = {
        "form":youtubeform,
    }
    return render(request, "dashboard/youtube.html", context)

@login_required
def todo_view(request):
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    form = TodoForm()
    if request.method == "POST":
        form = TodoForm(request.POST or None)
        if form.is_valid():
            try:
                finished = request.POST["Is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            form.instance.user = request.user
            form.save()
            return redirect("todo")
        messages.success(request, f"Todo added from {request.user.username} successfully")
    else:
        form = TodoForm()
    context= {
        "todo":todo,
        "forms":form,
        "todo_done":todo_done
    }
    return render(request, "dashboard/todo.html", context)

def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    if todo.Is_finished == True:
        todo.Is_finished = False
    else:
        todo.Is_finished = True
    todo.save()
    return redirect("todo")

def todo_delete(request, id):
    Todo.objects.get(id=id).delete()
    return redirect("todo")

@login_required
def books_view(request):
    if request == "POST":
        bookform = YoutubeForm(request.POST)
        search = request.POST['search']
        url = "https://www.googleapis.com/books/v1/volumes?q="+search
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo']['title'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')    
            }
            result_list.append(result_dict)
            context = {
                "forms":bookform,
                "results":result_list
            }
        return render(request, "dashboard/books.html", context)
    else:
        bookform = YoutubeForm()
    context = {
        "forms":bookform,
    }
    return render(request, "dashboard/books.html", context)

@login_required
def dictionary_view(request):
    if request == "POST":
        dictionaryform = YoutubeForm(request.POST)
        search = request.POST['search']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+search
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['search']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['phonetics'][0]['defintions'][0]['synonyms']
            context = {
                'forms':dictionaryform,
                'input':search,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'forms':dictionaryform,
                'input':''
            }
        return render(request, "dashboard/dictionary.html", context)
    else:
        dictionaryform = YoutubeForm()
        context = {
        'forms':dictionaryform
    }
    return render(request, "dashboard/dictionary.html", context)

def wiki_views(request):
    if request.method == 'POST':
        search = request.POST['search']
        form = YoutubeForm(request.POST or None)
        try:
            searchs = wikipedia.page(search)
        except wikipedia.exceptions.DisambiguationError as e:
            smell = random.choice(e.options)
            searchs = wikipedia.page(smell)
        searchs = wikipedia.page(search)
        context = {
            'form':form,
            'title':searchs.title,
            'link':searchs.url,
            'details':searchs.summary
        }
        return render(request, "dashboard/wiki.html", context)
    else:
        form = YoutubeForm()
        context = {
            'form': form
        }
    return render(request, "dashboard/wiki.html", context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measure_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measure_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measurement1']
                second = request.POST['measurement2']
                input = request.POST['input']
                answer = ""
                if input and int(input) >= 0:
                    if first == 'yard' and second =='foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second =='yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'answer':answer,
                    'm_form':measure_form,
                    'input':True
                }
        if request.POST['measurement'] == 'mass':
            measure_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measure_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measurement1']
                second = request.POST['measurement2']
                input = request.POST['input']
                answer = ""
                if input and int(input) >= 0:
                    if first == 'pound' and second =='kilogram':
                        answer = f'{input} pound = {int(input)*0.454} kilogram'
                    if first == 'kilogram' and second =='pound':
                        answer = f'{input} foot = {int(input)*2.20462} yard'
                context = {
                    'form':form,
                    'answer':answer,
                    'm_form':measure_form,
                    'input':True
                }                    
    else:
        form = ConversionForm()
        context = {
            'form':form,
            'input':''
        }
    return render(request, 'dashboard/conversion.html', context)

@login_required
def profile_view(request):
    homework = Homework.objects.filter(Is_Finished = False, user = request.user)
    todo = Todo.objects.filter(Is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    context= {
        "homework":homework,
        "todo":todo,
        "homework_done":homework_done,
        "todo_done":todo_done
    }
    return render(request, 'dashboard/profile.html', context)