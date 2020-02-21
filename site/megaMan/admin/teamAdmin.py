from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import team
mod = modelParser(team)


class teamResource(resources.ModelResource):
    class Meta:
        model = team
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['materialID']
        fields = mod

@admin.register(team)
class teamAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = teamResource

    fields = mod

    readonly_fields = ['teamID']

    list_display = ['teamID',
                    'default',
                    'name',
                    ]

    ordering = ['name']

    list_filter = []

    list_editable = ['name',
                     'default'
                     ]

    search_fields = ['teamID',
                     'name',
                     ]

    actions = []