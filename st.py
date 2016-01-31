from django.contrib.auth.models import User

for u in User.objects.all():
    try:
        u.profile
    except RelatedObjectDoesNotExist:
        u.username
        u.delete()