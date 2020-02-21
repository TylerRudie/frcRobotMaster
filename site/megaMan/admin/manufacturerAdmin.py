from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import manufacturer
mod = modelParser(manufacturer)


class manufacturerResource(resources.ModelResource):
    class Meta:
        model = manufacturer
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['manufacturerID']
        fields = mod

@admin.register(manufacturer)
class manufacturerAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = manufacturerResource

    fields = mod

    readonly_fields = ['manufacturerID']

    list_display = ['manufacturerID',
                    'name',
                    'isSponsor',
                    ]

    ordering = ['name']

    list_filter = ['isSponsor']

    list_editable = ['name',
                     'isSponsor'
                     ]

    search_fields = ['manufacturerID',
                     'name',
                     ]

    actions = []