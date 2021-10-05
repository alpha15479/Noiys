from django.views import View
from .forms import CommentForm, PositionForm
from django.http import request 
from django.db import transaction
from django.urls.base import reverse
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import redirect
from .models import Task
from .models import *
from django.utils import timezone


def post_list(request):
    querysets = Task.objects.all().order_by('-created_at')
    return render(request, 'home/post_list.html', {'qs': querysets})  


def post_detail(request, id):
    task = get_object_or_404(Task, id=id)
    comments = Comment.objects.filter(task=task).order_by('-id')
    stuff = get_object_or_404(Task, id=id)
    total_likes = stuff.total_likes()

    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(task=task, name=request.user, content=content)
            comment.save()
            return HttpResponseRedirect(task.get_absolute_url())
    else:
        comment_form = CommentForm()
    
    context = {'task': task, 'comments': comments, 'comment_form': comment_form, 'total_likes':total_likes, 'liked':liked, }


    return render(request, 'home/post_detail.html', context)


def LikeView(request, id):
    task = get_object_or_404(Task, id=id)
    liked = False

    if task.likes.filter(id=request.user.id).exists():
        task.likes.remove(request.user)
        liked = False
    else:
        task.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(id)]))

    
class CustomLoginView(LoginView):
    template_name = 'home/login.html'
    fields = '_all_'
    redirect_authenticated_user = True

    def get_success_url(self):
        #return reverse_lazy('tasks')
        return reverse_lazy('post_list')


class RegisterPage(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

 
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains=search_input)
        
        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'home/task.html'
 

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))


def postdetail(request):
    return render(request, 'home/postdetail.html')

def signup(request):
    return render(request, 'home/signup.html')

def about(request):
    return render(request, 'home/about.html')