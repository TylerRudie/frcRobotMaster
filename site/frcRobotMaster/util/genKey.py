from django.utils.crypto import get_random_string


def genKey(prefix='',
           length=5):

    return prefix + get_random_string(length=length,
                                      allowed_chars='ABCDEFGHJKLMNPQRSTUVXYZ01234567890')
