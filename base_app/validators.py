from django.forms import ValidationError

def UsernameMinMaxLengthValidator(value):
    if len(value) > 20:
        raise ValidationError('Username must be less than 20 symbols.')
    elif len(value) < 2:
        raise ValidationError('Username must be 2 or more symbols.')

