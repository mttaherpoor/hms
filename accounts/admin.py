from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'age', 'is_staff',]

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields':('age',)}),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        extra_fields = {
            "Personal info": ["age",],
        }

        new_fieldsets = []

        for name, opts in fieldsets:
            extra_fields = extra_fields.get(name, [])

            current_fields = list(opts.get("fields", ()))

            for field in extra_fields:
                if field not in current_fields:
                    current_fields.append(field)

            opts = {
                **opts,
                "fields": tuple(current_fields),
            }
            new_fieldsets.append((name, opts))

        return new_fieldsets    
