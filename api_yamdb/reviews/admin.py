from django.contrib import admin
from reviews.models import Title, Genre, Category, Comment, Review


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = ('name', 'year', 'description', 'category')
    search_fields = ('pk', 'name', 'year', 'description', 'category')
    list_filter = ('name', 'year', 'description', 'category')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Review)

