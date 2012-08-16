from django.contrib import admin

from django_base_model.models import AttributeModel


class AttributeModelInline(admin.TabularInline):
    model = AttributeModel


class BaseModelAdmin(admin.ModelAdmin):
    """
    Defines a BaseModelAdmin based off of Django's ModelAdmin that supports any
    model built with the BaseModel class so that we're able to save the user
    information of whoever is modifying the object through the admin site.

    This requires that the model you are associating with the ModelAdmin object
    inherits from BaseModel.
    """

    inlines = [AttributeModelInline, ]

    readonly_fields = (
        'last_modified_by',
        'time_created',
        'time_modified'
    )

    def last_modified_by_name(self, obj):
        """
        Method for use in the list_display tuple.
        """

        return obj.last_modified_by.get_full_name()
    last_modified_by_name.short_description = 'Last Modified By'

    def last_edited(self, obj):
        """
        Method for use in the list_display tuple.
        """

        return obj.time_modified.strftime('%m/%d/%Y %I:%M %p')
    last_edited.short_description = 'Last Edited'

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'last_modified_by') and hasattr(request, 'user'):
            obj.last_modified_by = request.user

        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if hasattr(instance, 'last_modified_by') and hasattr(request, 'user'):
                instance.last_modified_by = request.user

            instance.save()

        formset.save_m2m()

admin.site.register(AttributeModel)
