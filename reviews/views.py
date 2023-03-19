from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import sessions
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView
import os
import time
from  reviews.process import normal_method, improved_method
from django.http import HttpResponse
from django.template import loader


from .models import UserProfile

def store_file(file):
    with open("temp/queryImageLocal.jpg", "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)

# Create your views here.
def review(request):
    if request.method == 'POST':
        global qNumVal
        queryNum = request.POST['queryNo']
        def qNumVal():
            return queryNum
        queryName = request.FILES['image']
        store_file(queryName)
        print(f'The File Name is : {queryName}')
        # queryPath = os.path.abspath("queryImageLocal.jpg") 
        queryPath = 'temp\queryImageLocal.jpg'
        print(f'The Query Number is : {queryPath}')
        print(f'The Query Number is : {queryNum}')
        

        # ML
        start = time.time()
        result_old = normal_method(queryPath,queryNum)
        end = time.time()
        oldTime = round(end - start, 4)
        global oldTimeVal
        def oldTimeVal():
            return oldTime
        print(f"Old Time: {oldTime}\npath: {result_old}")

        start = time.time()
        result_new = improved_method(queryPath,queryNum)
        end = time.time()
        newTime =  round(end - start, 4)
        global newTimeVal
        def newTimeVal():
            return newTime
        global newTimeResult
        def newTimeResult():
            return result_new
        print(f"New Time: {newTime}\npath: {result_new}")

        return HttpResponseRedirect("compare")
        # return render(request, "reviews/thank-you.html")
        # we dont do this since POST req's job isn't to render page, so we re-direct ro different page and that page fill have to render the new html page
    
    return render(request, "reviews/review.html")

def compare(request):
    qNum = qNumVal()
    oTime = oldTimeVal()
    nTime = newTimeVal()
    newRes = newTimeResult()
    improv = round(((oTime - nTime)/oTime) * 100, 3)
    # improv_s = f"{improv:3f}"
    # print("\n", improv_s, "\n")
    # template = loader.get_template('')


    return render(request, "reviews/comapre.html", {'queryNum': qNum, 'oTime': oTime,'nTime': nTime, 'improv' : improv, 'newRes': newRes})


# class CreateProfileView(CreateView):
#     template_name = "reviews/review.html"
#     model = UserProfile
#     fields = "__all__"
#     success_url = "/compare"

# class ProfilesView(ListView):
#     model = UserProfile
#     template_name = "reviews/compare.html"
#     context_object_name = "profiles"