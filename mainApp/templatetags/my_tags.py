from django import template


register = template.Library()


def through_one(string):
    """
    Переводит каждый нечетный символ в верхний регистр, а четный в нижний
    Mother --> mOtHeR
    """
    new_string = ''
    for i in range(len(string)):
        new_string += string[i].upper() if i % 2 else string[i].lower()
    return new_string

register.filter('through_one', through_one)

if __name__ == '__main__':
    print(through_one('mmmmmmmmm'))