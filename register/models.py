from home.models import Users

def get_all_users():
    return Users.objects.all()
