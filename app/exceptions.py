from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

def base_exception_handler(exc, context):
    # Call DRF's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # check that a ValidationError exception is raised
    if isinstance(exc, ValidationError):
        # here prepare the 'custom_error_response' and
        # set the custom response data on response object
        if response.data.get('username', None):
            response.data = response.data['username'][0]
        elif response.data.get('email', None):
            response.data = response.data['email'][0]
        elif response.data.get('password', None):
            response.data = response.data['password'][0]

    return response
