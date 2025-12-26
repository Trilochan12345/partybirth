from django.shortcuts import render

def party(request):
    return render(request,'index.html')