from django import template


register = template.Library()


BAD_WORDS = ['О', 'Л', 'С', 'П']

@register.filter()
def censor(texts):
    if not isinstance(texts, str):
        raise ValueError('Этот тип переменной нельзя цензурировать')

    texts = texts.split()
    i = 0
    for word in texts:
        for badword in BAD_WORDS:
            if badword in word:
                expletive = badword + word.replace(word, '*****')
                texts[i] = expletive
        i += 1
    texts = ' '.join(texts)
    return f'{texts}'
