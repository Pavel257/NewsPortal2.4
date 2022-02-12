from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.core.mail import mail_managers
from .models import Post, Category, PostCategory


# создаём функцию обработчик с параметрами под регистрацию сигнала
# запускает выполнение кода при каком-либо действии пользователя, в нашем случае -
# сохранение в БД модели Post записи
# from news.models import Post, Category



@receiver(m2m_changed, sender=PostCategory)
def send_sub_mail(sender, instance, **kwargs):
    print()
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')


    sub_text = instance.text
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).postCategory.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    post = instance

    # для удобства вывода инфы в консоль, никакой важной функции не несет
    print('Адреса рассылки:')
    for zzz in subscribers:
        print(zzz.email)

    print()
    print()
    print()
    for subscriber in subscribers:
        # для удобства вывода инфы в консоль, никакой важной функции не несет
        print('**********************', subscriber.email, '**********************')
        print()
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='st3p.pavel@yandex.ru',
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')

        # для удобства вывода инфы в консоль
        print()
        print(html_content)
        print()

        # код ниже временно заблокирован, чтоб пока в процессе отладки не производилась реальная рассылка писем
        msg.send()

    return redirect('/news/')


@receiver(post_delete, sender=Post)
def del_sub_mail(sender, instance, **kwargs):
    subject = f'{instance.subscriber.username} отменил встречу!'
    mail_managers(
        subject=subject,
        message=f'Отменено назначение на {instance.date.strftime("%d %m %Y")}',
    )

    print(subject)

# Первый способ отправки сообщений подписчику
    # def post(self, request, *args, **kwargs):
    #     form = NewsForm(request.POST)
    #     # postCategory_pk = request.POST['postCategory'] # либо так можно, либо как ниже
    #     category_pk = request.POST.get('postCategory')
    #     sub_text = request.POST.get('text')
    #     sub_title = request.POST.get('title')
    #     category = Category.objects.get(pk=category_pk)
    #     subscribers = category.subscribers.all()
    #     host = request.META.get('HTTP_HOST')
    #
    #
    #     # валидатор - чтоб данные в форме были корректно введены, без вредоносного кода от хакеров и прочего
    #     if form.is_valid():
    #         news = form.save(commit=False)
    #         news.save()
    #         print('Статья:', news)
    #
    #     for subscriber in subscribers:
    #         # print('Адреса рассылки:', subscriber.email)
    #
    #
    #         html_content = render_to_string(
    #             'mail_sender.html', {'user': subscriber, 'text': sub_text[:50], 'post': news, 'host': host})
    #
    #
    #         msg = EmailMultiAlternatives(
    #             # Заголовок письма, тема письма
    #             subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
    #             # Наполнение письма
    #             body=f'{sub_text[:50]}',
    #             # От кого письмо (должно совпадать с реальным адресом почты)
    #             from_email='st3p.pavel@yandex.ru',
    #             # Кому отправлять, конкретные адреса рассылки, берем из переменной, либо можно явно прописать
    #             to=[subscriber.email],
    #         )
    #
    #         msg.attach_alternative(html_content, "text/html")
    #         print(html_content)
    #         msg.send()
    #
    # return redirect('/news/')


# @receiver(post_save, sender=Post)
# def send_sub_mail(sender, instance, created, **kwargs):
#     print('Сигнал - начало')
#     send_mail_for_sub(instance)
#     print('Сигнал - конец')