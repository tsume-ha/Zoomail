def register_user_data(strategy, details, backend, user, *args, **kwargs):
    user.receive_email = user.email
    user.save()