from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm, BlogExplanationForm, SearchForm
from .models import Blog, BlogExplanation
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    blog = Blog.objects.all()
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('title')
            searched = Blog.objects.filter(title__icontains=search)
            return render(request, 'index.html', {'blog': blog, 'searched':searched, 'form':form})
    form = SearchForm(request.POST)
    print(form)
    return render(request, 'index.html', {'blog':blog, 'form': form})


@login_required
def home(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'home.html', {'myblogs': blogs})


def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            img = form.cleaned_data.get('img')
            description = form.cleaned_data.get('description')

            blog = Blog.objects.create(user=request.user, title=title, img=img, description=description)
            blog.slug_save()
            return redirect('blog:blog-details', slug=blog.slug)

    form = BlogForm(request.POST, request.FILES)
    return render(request, 'create_blog.html', {'form': form})


def blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        form = BlogExplanationForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img')
            caption = form.cleaned_data.get('caption')
            blog_exp = BlogExplanation(user=request.user, slug=blog, img=img, caption=caption)
            blog_exp.save()
            return redirect('blog:blog-details', slug=slug)

    form = BlogExplanationForm()

    try:
        blog_extraa = BlogExplanation.objects.filter(slug__slug=slug)
        print(blog_extraa)
        return render(request, 'blog.html', {'blog': blog, 'blog_extraa': blog_extraa, 'form':form})
    except:
        print("blog Extraa data not found")

    return render(request, 'blog.html', {'blog': blog, 'form':form})



