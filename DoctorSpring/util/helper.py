# coding: utf-8
__author__ = 'jeremyxu'


def get_name(user):
    if user is None:
        return ''

    if user.name is not None:
        return user.name

    if user.email is not None:
        return user.email

    if user.phone is not None:
        return user.phone


