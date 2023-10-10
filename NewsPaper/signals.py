from datetime import date
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.conf import settings
from .models import Post, Category
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.models import Site
from NewsPaper.management.commands.runapscheduler import weekly_mail

######################################################################################################################


@receiver(post_save, sender=Post)
def mail_to_subscribers(sender, instance, created, **kwargs):
    try:
        post = instance
        current_site = Site.objects.get_current()
        category = get_object_or_404(Category, name=post.category)
        for subscriber in category.subscribers.all():
            html = render_to_string(
                template_name='mail/new_post.html',
                context={
                    'user': subscriber,
                    'post_url': f"{current_site.name}{reverse('post_show', args=(post.id, ))}",
                    'title': post.title,
                    'text': post.text[:50]
                },
            )
            msg = EmailMultiAlternatives(
                subject=f'Новая статья в разделе "{post.category}"!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email, ],
            )
            msg.attach_alternative(html, mimetype='text/html')

            try:
                msg.send()
            except Exception as e:
                print(e)

    except ObjectDoesNotExist:
        pass


######################################################################################################################


@receiver(weekly_mail)
def weekly_mail(sender, **kwargs):
    category_list = Category.objects.all()
    current_site = Site.objects.get_current()
    for category in category_list:
        subscriber_list = category.subscribers.all()
        post_list = Post.objects.filter(category=category).filter(creation_date_time__week=date.today().isocalendar()[1]-1)
        if post_list.count() > 0:
            for subscriber in subscriber_list:
                title = 'Подборка статей за неделю!'
                hello_text = f'Здравствуй, {subscriber}. Подборка статей за неделю в твоём любимом разделе {category}!'
                html = render_to_string(
                    template_name='account/email/weekly_mail.html',
                    context={
                        'title': title,
                        'hello_text': hello_text,
                        'post_list': post_list,
                        'category': category,
                        'site_link': current_site
                    },
                )
                msg = EmailMultiAlternatives(
                    subject=title,
                    body=hello_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email, ],
                )
                msg.attach_alternative(html, mimetype='text/html')

                try:
                    msg.send()
                except Exception as e:
                    print(e)


######################################################################################################################
