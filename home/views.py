from django.shortcuts import render


def HomePage(request , *args , **kwargs ) :
    context = {}
    return render(request , "home/homePage.html" , context) 