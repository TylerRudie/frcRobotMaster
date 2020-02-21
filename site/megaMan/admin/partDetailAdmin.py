from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import partDetail, item
mod = modelParser(partDetail)


class partDetailResource(resources.ModelResource):
    class Meta:
        model = partDetail
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['partID']
        fields = mod


class itemTabularInline(admin.TabularInline):
    model = item
    extra = 0
    show_change_link = True
    readonly_fields = ['inFRC_BOM',
                       'totalWeight',
                       'totalPrice'
                       ]


@admin.register(partDetail)
class partDetailAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = partDetailResource

    fields = mod

    readonly_fields = ['partID']

    list_display = ['partID',
                    'name',
                    'manufacturer',
                    'manufacturerPartNumber',
                    'marketPrice',
                    'laborPrice',
                    'weight',
                    'measurement',
                    'cots',
                    'material',
                    'category',
                    ]

    ordering = ['name']

    list_filter = ['manufacturer',
                   'category']

    list_editable = ['name',
                     'manufacturer',
                     'manufacturerPartNumber',
                     'marketPrice',
                     'laborPrice',
                     'weight',
                     'measurement',
                     'cots',
                     'material',
                     'category',
                     ]

    search_fields = ['partID',
                     'name',
                     'shortDescription',
                     'longDescription'
                     ]

    actions = []
    inlines = [itemTabularInline]