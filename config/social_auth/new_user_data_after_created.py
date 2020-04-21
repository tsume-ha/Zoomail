def register_user_data(strategy, details, backend, user, *args, **kwargs):
    if user:
        user.receive_email = user.email
        user.save()