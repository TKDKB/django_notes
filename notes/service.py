from django.core.handlers.wsgi import WSGIRequest
from notes.models import Note, Tag
from django.db.models import QuerySet, Q
from django.db.models import F
from django.contrib.postgres.aggregates import ArrayAgg


def create_note(request: WSGIRequest) -> Note:
    # print(request.FILES)
    note = Note.objects.create(
        title=request.POST["title"],
        content=request.POST["content"],
        user=request.user,
        image=request.FILES.get("noteImage"),
    )
    if 'switch' in request.POST:
        flex_switch_value = request.POST['switch']
        # print("switch value:", flex_switch_value)
        if flex_switch_value == 'on':
            note.is_private = True
            note.save()
        else:
            note.is_private = False
            note.save()

    tags: list = request.POST.get("tags", "").split(",")

    tags = [tag.strip() for tag in tags]
    for tag in tags:
        if tag == '':
            tags.remove(tag)
    print(tags)
    tags_objects = []
    for tag in tags:
        tag_obj, created = Tag.objects.get_or_create(name=tag)
        tags_objects.append(tag_obj)

    note.tags.set(tags_objects)
    return note


def filter_notes(search: str) -> QuerySet:
    if search:
        # notes_queryset = Note.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
        notes_queryset = (Note.objects.filter(Q(title__icontains=search)))

    else:
        notes_queryset = (Note.objects.all())
    print(notes_queryset.query)
    return notes_queryset


def queryset_optimization(queryset: QuerySet) -> QuerySet:
    return (
        queryset
        .select_related("user")
        .prefetch_related("tags")
        .annotate(
            username=F('user__username'),
            tags_list=ArrayAgg("tags__name", distinct=True),
        )
        .values("uuid", "title", "created_at", "mod_time", "is_private", "user__username", "user__id",
                "tags_list")
        .distinct()
        .order_by("-mod_time")
    )
