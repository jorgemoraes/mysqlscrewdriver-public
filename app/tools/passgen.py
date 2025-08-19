import string
import random


def generate_password(length, include_lowercase, inlcude_uppercase, include_digits, include_punctuation, include_secure_punctuation):
    password = ''
    random_set = ''

    # If include lowercase
    if include_lowercase:
        random_set += string.ascii_lowercase
        password += random.choice(string.ascii_lowercase)

    # If inlcude uppercase
    if inlcude_uppercase:
        random_set += string.ascii_uppercase
        password += random.choice(string.ascii_uppercase)

    # If include digits
    if include_digits:
        random_set += string.digits
        password += random.choice(string.digits)

    # If include punctuation
    if include_punctuation:
        random_set += string.punctuation
        password += random.choice(string.punctuation)

    # If include secure punctuation
    if include_secure_punctuation:
        custom_punctuation = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        random_set += ''.join(custom_punctuation)
        password += random.choice(custom_punctuation)

    for i in range(length-3):
        password += random.choice(random_set)

    password_list = list(password)
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)

    return password
