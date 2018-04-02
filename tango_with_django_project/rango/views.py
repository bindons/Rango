from django.shortcuts import render

# Create your views here.

#from django.http import HttpResponse
from rango.models import Category,Page
from rango.forms import  CategoryForm,PageForm


def index(request):
    #return HttpResponse('Rango says hey there partner!')
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'pages':page_list}
    return render(request,'rango/index.html',context=context_dict)


def about(request):
    #return HttpResponse('Rango says here is the about page!')
    context_dict = {'your_name':'dongjie'}
    return render(request,'rango/about.html',context=context_dict)


def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=True)
            print(category, category.slug)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})

