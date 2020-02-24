from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from frcRobotMaster.util.modelParser import modelParser

from megaMan.models import location, item
mod = modelParser(location)


class locationResource(resources.ModelResource):
    class Meta:
        model = location
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ['locationID']
        fields = ['locationID',
                  'default',
                  'name',
                  'owner',
                  'partOf',
                  'type',
                  'dropDownWeight']


class itemTabularInline(admin.TabularInline):
    model = item
    show_change_link = True
    can_delete = False
    extra = 0
    readonly_fields = ['totalPrice']


@admin.register(location)
class locationAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    resource_class = locationResource

    fields = mod + ['getFRC_BOM_URL',
                    'FRC_Total',
                    'grandFRC_Total',
                    'totalPrice',
                    'grandTotalPrice',
                    'totalWeight',
                    'grandTotalWeight',

                    ]

    readonly_fields = ['getFRC_BOM_URL',
                       'locationID',
                       'FRC_Total',
                       'totalPrice',
                       'totalWeight',
                       'grandFRC_Total',
                       'grandTotalWeight',
                       'grandTotalPrice']

    list_display = ['locationID',
                    'default',
                    'name',
                    'type',
                    'dropDownWeight',
                    'owner',
                    'partOf',
                    'getFRC_BOM_URL',
                    ]

    ordering = ['location']

    list_filter = ['location',
                   'owner',
                   'type']

    list_editable = ['default',
                     'name',
                     'type',
                     'owner',
                     'dropDownWeight',
                     'partOf']

    search_fields = ['locationID',
                     'name'
                     ]

    actions = []
    inlines = [itemTabularInline]
