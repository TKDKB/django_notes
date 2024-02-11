from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet

from .models import Note, Tag
from registration.models import User


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'mod_time', 'tags_func', 'user', 'img']
    search_fields = ['title']
    date_hierarchy = 'created_at'
    list_filter = ['user__username', 'user__email', 'tags__name']
    filter_horizontal = ["tags"]

    @admin.display(description="tags")
    def tags_func(self, obj: Note):
        tags = list(obj.tags.all())
        text = ""
        for tag in tags:
            text += f"<span class=\"badge text-bg-dark me-2\">{tag}</span>"

        return mark_safe(text)


    @admin.display(description="content")
    def short_content(self, obj: Note):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content


    @admin.display(description="img")
    def img(self, obj: Note):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" height="128">')
        return "X"

    def get_queryset(self, request):
        return (
            Note.objects.all()
            .select_related("user")
            .prefetch_related("tags")
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("username", "first_name", "last_name", "is_active", "notes_amount")

    actions = ["deactivate_users", "activate_users"]

    @admin.display(description="Notes Amount")
    def notes_amount(self, obj: User):
        return len(list(Note.objects.filter(user__username=obj.username)))



    @admin.action(description="Deactivate user(s)")
    def deactivate_users(self, form, queryset: QuerySet[User]):
        queryset.update(is_active=False)

    @admin.action(description="Activate user(s)")
    def activate_users(self, form, queryset: QuerySet[User]):
        queryset.update(is_active=True)


