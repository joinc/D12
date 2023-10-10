import re
from django import template
from NewsPaper.templatetags.words import BANNED_WORDS

######################################################################################################################


register = template.Library()


######################################################################################################################


@register.filter(name='is_author')
def is_author(user):
    return user.groups.filter(name='authors').exists()


######################################################################################################################


@register.filter(name='censor')
def censor(value, arg):
    """
    Функция собственного фильтра, который цензурирует нежелательную лексику в названиях и текстах статей.
    :param value:
    :param arg:
    :return:
    """
    if isinstance(value, str) and isinstance(arg, str):
        content = value.split()
        for index, word in enumerate(value.split()):
            if word.lower() in BANNED_WORDS:
                content[index] = re.sub(word, f'{word[0]}{arg * (len(word) - 1)}', content[index])
        return " ".join(content)
    else:
        raise ValueError()


######################################################################################################################
