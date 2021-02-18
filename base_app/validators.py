from django.forms import ValidationError


def UsernameMinMaxLengthValidator(value):
    if len(value) > 20:
        raise ValidationError("Username must be less than 20 symbols.")
    elif len(value) < 2:
        raise ValidationError("Username must be 2 or more symbols.")


def WeightHeightNegativeNumberValidator(value):
    if value <= 0:
        raise ValidationError("Please enter a valid number!")


def ChangePasswordValidator(value):
    if len(value) < 8 or len(value) > 20:
        raise ValidationError(
            f"Password must be between 8 and 20 symbols. Current: {len(value)}"
        )
