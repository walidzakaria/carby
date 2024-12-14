from django.core.exceptions import ValidationError


def validate_pdf(file):
    """ Validator to ensure only PDF files are allowed """
    if not file.name.endswith('.pdf'):
        raise ValidationError('Only .pdf files are allowed!')

