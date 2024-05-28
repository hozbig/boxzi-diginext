from django.contrib import admin
from .models import Company, Product, Center


class InlineProduct(admin.StackedInline):
    model = Product
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "domain",  "logo_preview"]
    search_fields = ["name", "domain"]
    list_filter = ["domain"]
    inlines = [InlineProduct,]


admin.site.register(Company, CompanyAdmin)


class CenterAdmin(admin.ModelAdmin):
    list_display = ["name", "state", "type", "activity", "logo_preview"]
    search_fields = ["name", "domain", "activity"]
    list_filter = ["state", "type"]
    filter_horizontal = ["teams", "mentors"]


admin.site.register(Center, CenterAdmin)