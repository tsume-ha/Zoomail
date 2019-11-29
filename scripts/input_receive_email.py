from members.models import User

def run():
	for user in User.objects.all():
		user.receive_email = user.get_receive_email()
		user.save()
