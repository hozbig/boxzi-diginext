from django.contrib import admin

from . import models


class ContentOrderInline(admin.TabularInline):
    model = models.ContentOrder
    extra = 1
    autocomplete_fields = ['content']


class CollectionOrderInline(admin.TabularInline):
    model = models.CollectionOrder
    extra = 1
    autocomplete_fields = ['collection']


class ContentAdmin(admin.ModelAdmin):
    list_display = ["title", "medals", "accelerator", "uuid"]
    list_filter = ["subjects"]
    search_fields = ["title"]
    filter_horizontal = ("subjects",)
    autocomplete_fields = ["accelerator"]

    class Meta:
        model = models.Content

admin.site.register(models.Content, ContentAdmin)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "exam", "type", "accelerator", "uuid"]
    list_filter = ["exam", "type", "created_time", "last_update_time"]
    search_fields = ["name"]
    filter_horizontal = ("subjects",)
    autocomplete_fields = ["exam", "accelerator"]
    inlines = (ContentOrderInline,)

    class Meta:
        model = models.Collection

admin.site.register(models.Collection, CollectionAdmin)


class WatchedContentAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "__str__"]
    search_fields = ["user__username", "content__title", "content__uuid"]
    list_filter = ["user", "content"]

    def delete_model(self, request, obj):
        request.user.received_medals -= obj.content.medals
        request.user.save()
        super().delete_model(request, obj)

admin.site.register(models.WatchedContent, WatchedContentAdmin)


class ContentOrderAdmin(admin.ModelAdmin):
    list_display = ["collection", "content", "row_number"]
    search_fields = ["collection__name", "content__title", "content__uuid", "row_number"]
    list_filter = ["collection", "content"]
    autocomplete_fields = ['collection', 'content']

admin.site.register(models.ContentOrder, ContentOrderAdmin)


class RoadAdmin(admin.ModelAdmin):
    list_display = ["name", "accelerator", "uuid"]
    list_filter = ["accelerator", "created_time", "last_update_time"]
    search_fields = ["name"]
    autocomplete_fields = ["accelerator"]
    inlines = (CollectionOrderInline,)

    class Meta:
        model = models.Road

admin.site.register(models.Road, RoadAdmin)


class RoadFundAdmin(admin.ModelAdmin):
    list_display = ["road"]
    list_filter = ["created_time", "last_update_time"]
    search_fields = ["road__name"]
    autocomplete_fields = ["road"]

    class Meta:
        model = models.RoadFund

admin.site.register(models.RoadFund, RoadFundAdmin)