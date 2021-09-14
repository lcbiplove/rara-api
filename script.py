from django.contrib.auth import get_user_model

User = get_user_model()

user_data = {
        'email': 'tester@gmail.com',
        'password': 'tester',
        'name': 'Tester',
        'location': 'Kathmandu'
    }
user = User.objects.create_user(**user_data)
user.save()
