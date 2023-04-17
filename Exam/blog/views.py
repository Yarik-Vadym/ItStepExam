from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib import messages
from django.core.exceptions import ValidationError


def index(request):
    get_blog = Blog.objects.all()[::-1]
    return render(request, 'blog/index.html', {'data_blog': get_blog})


def blog(request, pk):
    get_blog = Blog.objects.get(pk=pk)
    last_five_blogs = Blog.objects.all()[:5]
    last_five_blogs_reverse = reversed(last_five_blogs)
    return render(request, 'blog/blog.html', {'data_blog': get_blog, 'last_five_blogs': last_five_blogs_reverse})


def edit_blog(request, pk):
    get_blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=get_blog)
        if form.is_valid():
            form.save()
            return redirect('blog', pk=get_blog.pk)
    else:
        form = BlogForm(instance=get_blog)
    return render(request, 'blog/create_blog.html', {'form': form})


def create_blog(request):
    if not request.user.is_staff:
        raise ValidationError('Шо?')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.save()
            name.save()
            messages.success(request, 'Блог был успешно опубликован!')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})