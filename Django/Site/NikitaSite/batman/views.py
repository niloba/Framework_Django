from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from.models import *
from .utils import *

class VillainsHome(DataMixin, ListView):
    model = Villains
    template_name = 'batman/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Villains.objects.filter(is_published=True).select_related('cat')

#def index(request):
 #   posts = Villains.objects.all()

  #  context = {
   #     'posts': posts,
   #     'menu': menu,
   #     'title': 'Home Page',
   #     'cat_selected': 0,
    #}

    #return render(request, 'batman/index.html', context=context)


def about(request):
    return render(request, 'batman/about.html', {'menu': menu, 'title': 'About Site'})

class AddArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'batman/addarticle.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Adding article')
        return dict(list(context.items()) + list(c_def.items()))

#def addarticle(request):
    #if request.method =='POST':
        #form = AddPostForm(request.POST, request.FILES)
        #if form.is_valid():
            #print(form.cleaned_data)
           # form.save()
           # return redirect('home')
   # else:
       # form = AddPostForm()

    #return render(request, 'batman/addarticle.html', {'form': form, 'menu': menu, 'title': 'Add article'})

#def contact(request):
 #   return HttpResponse("Feedback")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'batman/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

#def login(request):
 #   return HttpResponse("Login")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Sorry, no Bats today</h1>')


class ShowPost(DataMixin, DetailView):
    model = Villains
    template_name = 'batman/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


#def show_post(request, post_slug):
    #post = get_object_or_404(Villains, slug=post_slug)

    #context = {
        #'post': post,
       # 'menu': menu,
       # 'title': post.title,
       # 'cat_selected': post.cat_id,
   # }

    #return render(request, 'batman/post.html', context=context)

class VillainsCategory(DataMixin, ListView):
    model = Villains
    template_name = 'batman/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Villains.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

#def show_category(request, cat_id):
    #posts = Villains.objects.filter(cat_id=cat_id)

    #if len(posts) == 0:
       # raise Http404()

   # context = {
        #'posts': posts,
        #'menu': menu,
       # 'title': 'View of articles',
       # 'cat_selected': cat_id,
   # }

    #return render(request, 'batman/index.html', context=context)

class RegisterUser (DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'batman/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'batman/login.html'

    def get_user_context(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')