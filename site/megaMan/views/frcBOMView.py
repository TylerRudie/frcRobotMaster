from django.views.generic.detail import DetailView
from django_xhtml2pdf.views import PdfMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from megaMan.models import location


class frcBOMView(PermissionRequiredMixin, DetailView):
    permission_required = 'megaMan.change_location'
    login_url = '/admin/login/'
    model = location
    template_name = 'util/frcBOM.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#        context['billOfMaterials'] = location.frcBOM_fullListing
        return context
