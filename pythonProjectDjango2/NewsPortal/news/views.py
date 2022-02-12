from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django_filters import DateFilter

from .models import Post, Category, Author, Category
from .forms import NewsForm
from .filters import NewsFilter, CategoryFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.loader import render_to_string


# from django.views.generic import TemplateView
# from django.utils.decorators import method_decorator

class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    queryset = Category.objects.all()
    context_object_name = 'Category'


    def get_filter(self):
        return CategoryFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['filter'] = CategoryFilter(self.request.GET, queryset=self.get_queryset())

        return context


        # and DateFilter(self.request.GET, queryset=self.get_queryset())

        # def news_list(request):
        #     f = NewsFilter(request.GET, queryset=Post.objects.all())
        #     return render(request, 'news/news_search.html', {'filter': f})






class AuthorList(ListView):
    model = Author
    template_name = 'authors.html'
    queryset = Author.objects.all()
    context_object_name = 'Authors'
    ordering = ['-ratingAuthor']

    # paginate_by = 5
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()

        return context


class NewsList(ListView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'Posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['date_filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())

        # context['posts'] = Post.objects.all()
        # context['form'] = NewsForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
    #     return {
    #         **super().get_context_data(*args, **kwargs),
    #         'filter': self.get_filter(),
    #     }
    #


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'Posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())
        # and DateFilter(self.request.GET, queryset=self.get_queryset())

        # def news_list(request):
        #     f = NewsFilter(request.GET, queryset=Post.objects.all())
        #     return render(request, 'news/news_search.html', {'filter': f})

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['date_filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())
        return context
        # context['posts'] = Post.objects.all()
        # context['form'] = NewsForm()


#
#     # def get_context_data(self, *args, **kwargs):
#     #     return {
#     #         **super().get_context_data(*args, **kwargs),
#     #         'filter': self.get_filter(),
# #     #     }
# class DateFilter(DateFilter):
#     model = Post
#     template_name = 'news2.html'
#
#     def get_filter(self):
#         return DateFilter(self.request.GET, queryset=super().get_queryset())


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        aaa = Category.objects.filter(pk=Post.objects.get(pk=id).postCategory.name).values("subscribers__username")
        context['is_not_subscribe'] = not aaa.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = aaa.filter(subscribers__username=self.request.user).exists()
        return context


# @login_required
# def add_subscribe(request, pk,):
#     user = request.user
#     sub_user = User.objects.get(id=user.pk)
#     category_object = PostCategory.objects.get(postThrough=pk)
#     category_object_name = category_object.categoryThrough
#
#     print('Пользователь', user, 'добавлен в подписчики категории:', category_object_name)
#     category_object_name.subscribers.add(sub_user)
#
#     return redirect('/news/')
#
#
# # функция отписки от группы
# @login_required
# def del_subscribe(request, pk):
#     user = request.user
#     sub_user = User.objects.get(id=user.pk)
#     category_object = PostCategory.objects.get(postThrough=pk)
#     category_object_name = category_object.categoryThrough
#     print('Пользователь', user, 'удален из подписчиков категории:', category_object_name)
#     category_object_name.subscribers.remove(sub_user)
#     return redirect('/news/')
@login_required
def subscribe_me(request, news_category_id):
    user = request.user
    my_category = Category.objects.get(id=news_category_id)
    sub_user = User.objects.get(id=user.pk)
    if my_category.subscribers.filter(id=user.pk):
        my_category.subscribers.remove(sub_user)
        return redirect(f'/news')
    else:
        my_category.subscribers.add(sub_user)
        return redirect(f'/news')


# def subscribe_me(request, news_category_id):
#     user = request.user
#     my_category = Category.objects.get(id=news_category_id)
#     sub_user = User.objects.get(id=user.pk)
#     if my_category.subscribers.filter(id=user.pk):
#         my_category.subscribers.remove(sub_user)
#         return redirect('/news/')
#     else:
#         my_category.subscribers.add(sub_user)
#         return redirect('/news/')

# @login_required
# def add_subscribe(request, pk, **kwargs):
#     pk = request.GET.get['pk']
#     print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
#     Category.objects.get(pk=pk).subscribers.add(request.user)
#     return redirect('/news/')
#
#
# # # функция отписки от группы
# @login_required
# def del_subscribe(request, **kwargs):
#     pk = request.GET.get['pk']
#     print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
#     Category.objects.get(pk=pk).subscribers.remove(request.user)
#     return redirect('/news/')
# #


class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/news/'


# дженерик для редактирования объекта
# @method_decorator(login_required, name='dispatch')


class NewsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/news/'

    def get_object(self, **kwargs):  # (4)
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AddNews(PermissionRequiredMixin, NewsCreateView):
    permission_required = ('news.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsUpdateView):
    permission_required = ('news.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDeleteView):
    permission_required = ('news.delete_post',)

# class PostsDetail(DetailView):
#     model = Post
#     template_name = 'sample_app/news2.html'
#     context_object_name = 'Post'
#     queryset = Post.objects.order_by('-dateCreation')
#
#
#    def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()
#         context['value1'] = None
#         return context
# def send_mail_for_sub(instance, ):
#     print()
#     print()
#     print('====================ПРОВЕРКА СИГНАЛОВ===========================')
#     print()
#     print('задача - отправка письма подписчикам при добавлении новой статьи')
#
#     sub_text = instance.text
#     category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).postCategory.pk)
#     print()
#     print('category:', category)
#     print()
#     subscribers = category.subscribers.all()
#
#     post = instance
#
#     # для удобства вывода инфы в консоль, никакой важной функции не несет
#     print('Адреса рассылки:')
#     for zzz in subscribers:
#         print(zzz.email)
#
#     print()
#     print()
#     print()
#     for subscriber in subscribers:
#         # для удобства вывода инфы в консоль, никакой важной функции не несет
#         print('**********************', subscriber.email, '**********************')
#         print()
#         print('Адресат:', subscriber.email)
#
#         html_content = render_to_string(
#             'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})
#
#         sub_username = subscriber.username
#         sub_useremail = subscriber.email
#
#         # msg = EmailMultiAlternatives(
#         #     subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
#         #     from_email='st3p.pavel@yandex.ru',
#         #     to=[subscriber.email]
#         # )
#
#         # msg.attach_alternative(html_content, 'text/html')
#
#         # для удобства вывода инфы в консоль, никакой важной функции не несет
#         print()
#         print(html_content)
#         print()
#
#         # код ниже временно заблокирован, чтоб пока в процессе отладки не производилась реальная рассылка писем
#         # msg.send()
#
#     return redirect('/news/')
