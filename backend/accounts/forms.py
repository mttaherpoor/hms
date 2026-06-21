from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .constants import UserType
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm): 
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'age', 'user_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_type'].choices = [
            c for c in UserType.choices
            if c[0] != UserType.ADMIN
        ]


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
