from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'age', 'user_type', 'is_staff',]

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields':('age',)}),
        (None, {'fields':('user_type',)}),
    )

    radio_fields = {
        'user_type': admin.HORIZONTAL,
    }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        inject_config  = {
            "Personal info": ["age",'user_type'],
        }

        new_fieldsets = []

        for name, opts in fieldsets:
            extra_fields = inject_config .get(name, [])

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
