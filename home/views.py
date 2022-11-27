from django.shortcuts import render, redirect
from django.views.generic import CreateView
from myprojects.main1 import *

from django.http import StreamingHttpResponse
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, "home/index.html")


def getList(request):
    return render(request, "home/index.html")


def showList(request):
    word_list = Dictionary("home/deneme.json").word_list

    context = {
        'word_list': word_list
    }
    return render(request, 'home/list_words.html', context)


def delete_word(request):
    word_list = Dictionary("home/deneme.json").word_list
    if request.method == 'POST':
        value = request.POST.get("value")
        if value:
            word_list = Dictionary("home/deneme.json")
            word_list.delete_word(value=value)
            return redirect("show_list")
    return render(request, 'home/delete.html')


def adding_word(request):
    print(11)
    print("gelen istek tipi****", request.method)

    word_list = Dictionary("home/deneme.json").word_list
    if request.method == "POST":
        print(22)
        word = request.POST.get("word")
        meaning = request.POST.get("meaning")
        sample = request.POST.get("sample")
        if word and meaning and sample:
            word_list = Dictionary("home/deneme.json")
            word_list.insert_word(word=word, meaning=meaning, sample=sample)

            return redirect("show_list")

    return render(request, 'home/add_word.html')


def search_word(request):
    if request.method == 'POST':
        value = request.POST.get("value")

        if value:
            meaning_list = Dictionary("home/deneme.json").search_word(value=value)
            context = {
                'meaning_list': meaning_list,
                'value':value
            }
            return render( request, 'home/search_result.html', context)

    return render(request, 'home/search.html')


def update_word(request):
    word_list = Dictionary("home/deneme.json").word_list
    if request.method == 'POST':
        new_value = request.POST.get("new_value")

        if new_value:
            word_list = Dictionary("home/deneme.json")
            word = request.POST.get("word")
            meaning = request.POST.get("meaning")
            new_value = request.POST.get("new_value")
            word_list.edit_word(word=word,meaning=meaning,new_value=new_value)

            return redirect('show_list')

    return render(request, 'home/update.html')



    # gelen valuenin sadece meaningini yazdır
# ya da samplenı yazdır
