from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    censor_list = ['дебил',
                   'дурак',
                   'придурок']

    value1 = (str(value)).split()
    for i in censor_list:
        for j in value1:
            if j == i:
                value1.remove(i)
    value = ' '.join(value1)
    return str(value)

    # else:
    #     return f'Нелья писать следующие слова:{censor_list}'

    # if isinstance(value, str) and isinstance(arg, int):
    #     return str(value) * arg  # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    # else:
    #     raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')  #  в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку

#
@register.filter(name='update_page')
def update_page(full_path: str, page: int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param in params_list])
        params.update({'page': page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"
