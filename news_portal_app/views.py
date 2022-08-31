from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .filters import PostFilter
from .models import Post, Category
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.views import View
from .tasks import hello, printer, send_mail
from django.http import HttpResponse




class PostsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = not self.request.user.groups.filter(name='Subscribers').exists()
        context['is_subscribers'] = self.request.user.groups.filter(name='Subscribers').exists()
        return context


@login_required
def add_subscribe(request, **kwargs):
    cat_number = int(kwargs['pk'])
    #print('Пользователю', request.user, 'добавлена категория в подписки:', Category.objects.get(pk=pk))
    Category.objects.get(pk=cat_number).subscribers.add(request.user)
    return redirect('/news/')


@login_required
def delete_subscribe(request, **kwargs):
    cat_number = int(kwargs['pk'])
    #print('Пользователю', request.user, 'добавлена категория в подписки:', Category.objects.get(pk=pk))
    Category.objects.post(pk=cat_number).subscribers.pop(request.user)
    return redirect('/news/')


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal_app.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'NW'
        return super().form_valid(form)

        Post.save()


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal_app.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'NW'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверяем количество постов автора за текущие сутки
        limit = settings.DAILY_POST_LIMIT
        context['limit'] = limit
        last_day = timezone.now() - timedelta(days=1)
        posts_day_count = Post.objects.filter(author_post__author_user=self.request.user,date_pub__gte=last_day,).count()
        context['count'] = posts_day_count
        context['post_limit'] = posts_day_count < limit

        return context

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_portal_app.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'AR'
        return super().form_valid(form)

        Post.save()

class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_portal_app.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'AR'
        return super().form_valid(form)


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class AuthorUpdate(LoginRequiredMixin, TemplateView, UpdateView):
    template_name = 'prodected_page.html'


class IndexView(View):
    def get(self, request):
        send_mail.delay()
        return HttpResponse('Hello!')