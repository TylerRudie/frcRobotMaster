from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import material
mod = modelParser(material)


class materialResource(resources.ModelResource):
    class Meta:
        model = material
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['materialID']
        fields = mod

@admin.register(material)
class materialAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = materialResource

    fields = mod

    readonly_fields = ['materialID']

    list_display = ['materialID',
                    'name',
                    ]

    ordering = ['name']

    list_filter = []

    list_editable = ['name',
                     ]

    search_fields = ['materialID',
                     'name',
                     ]

    actions = []