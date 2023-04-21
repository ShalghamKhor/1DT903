isbn = ''
author = ''
title = ''
price = float(0)
subject = ''
subjects = []

def get_isbn():
    return isbn

def set_isbn(val):
    global isbn
    isbn = val

def get_author():
    return author

def set_authotr(val):
    global author
    author = val

def get_title():
    return title

def set_title(val):
    global title
    title = val

def get_price():
    return price

def set_price(val):
    global price
    price = val

def get_subject():
    return subject

def set_subject(val):
    global subject
    subject = val


def get_subjects():
    return subjects

def set_subjects(list):
    global subjects
    subjects.append(list)