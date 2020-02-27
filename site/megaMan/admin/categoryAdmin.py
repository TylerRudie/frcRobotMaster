from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import category


class categoryResource(resources.ModelResource):
    class Meta:
        model = category
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['categoryID']
        fields = ('categoryID',
                  'name'
                  )


@admin.register(category)
class categoryAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = categoryResource

    fields = ['categoryID',
              'name']
    readonly_fields = ['categoryID']
    list_display = ['name']
    ordering = ['name']
    list_filter = []
    search_fields = ['categoryID',
                     'name'
                     ]
    actions = []