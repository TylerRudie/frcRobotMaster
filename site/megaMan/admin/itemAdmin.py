from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import item
mod = modelParser(item)


class itemResource(resources.ModelResource):
    class Meta:
        model = item
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['itemID']
        fields = mod


@admin.register(item)
class itemAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = itemResource

    fields = mod

    readonly_fields = ['itemID',
                       'inFRC_BOM',
                       'totalWeight',
                       'totalPrice']

    list_display = ['itemID',
                    'location',
                    'details',
                    'serialNumber',
                    'purchasedPrice',
                    'purchasedDate',
                    'kop',
                    'quantity',
                    'get_measurement',
                    'totalPrice',
                    ]

    ordering = ['location']

    list_filter = ['location',
                   'details',
                   'kop']

    search_fields = ['itemID',
                     'serialNumber'
                     ]

    list_editable = ['location',
                     'details',
                     'kop',
                     'serialNumber',
                     'purchasedDate',
                     'purchasedPrice',
                     'quantity']

    actions = []

    def get_measurement(self, obj):
        if obj.details is not None:
            return obj.details.measurement
        else:
            return '----'
    get_measurement.short_description = 'Measurement'

