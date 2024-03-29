from django.core.exceptions import ValidationError
import os

def validate_svg(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path & filename
    valid_extensions = ['.jpg', '.png', '.svg'] # populate with the extensions that you allow / want
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')