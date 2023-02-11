import django_filters

from users.models import User


class UserFilter(django_filters.FilterSet):
    groups = django_filters.ModelMultipleChoiceFilter(field_name='full_name', conjoined=True,
                                                      queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['groups']
