from cers.core.admin import CersModelAdmin, admin_site
from cers.reports.models import ReportGeneration


class ReportGenerationAdmin(CersModelAdmin):
    fields = ('report_type', ('date_from', 'date_to'), 'company')

    def get_fields(self, request, obj=None):
        if obj:
            return 'report_type', ('date_from', 'date_to'), 'company', 'report_file'
        return super().get_fields(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return 'report_type', 'date_from', 'date_to', 'company', 'report_file'
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_delete_permission(request, obj)


admin_site.register(ReportGeneration, ReportGenerationAdmin)
