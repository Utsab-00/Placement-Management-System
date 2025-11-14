def user_context(request):
    return {
        'is_logged_in': request.session.get('logged_in', False),
        'user_type': request.session.get('user_type', None),
        'user_email': request.session.get('email', None),
    }