from django.contrib import admin
# Register your models here.
from monitor.models import Machine, Crash, AuthInformation, Testcase, Issue, OnetimeToken, AlertInfoUser

def exceptfield(list_display, fields=[]):
	# Remove fields that you won't show.
	if len(fields) == 0:
		return 0;
	for field in fields:
		list_display.remove(field)

class MachineAdmin(admin.ModelAdmin):
    list_display = Machine._meta.get_all_field_names() 
admin.site.register(Machine, MachineAdmin)

class CrashAdmin(admin.ModelAdmin):
    list_display = Crash._meta.get_all_field_names()
    exceptfield(list_display,["crashlog", "comment", "link", "crash_file", "crash_hash"])
admin.site.register(Crash, CrashAdmin)

class TestcaseAdmin(admin.ModelAdmin):
    list_display = Testcase._meta.get_all_field_names()
admin.site.register(Testcase,TestcaseAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = Issue._meta.get_all_field_names()
admin.site.register(Issue, IssueAdmin)

# Register information of fuzzer
class AuthInformationAdmin(admin.ModelAdmin):
    list_display = AuthInformation._meta.get_all_field_names()
    exceptfield(list_display,["password"])
admin.site.register(AuthInformation, AuthInformationAdmin)


class OnetimeTokenAdmin(admin.ModelAdmin):
    list_display = OnetimeToken._meta.get_all_field_names()
admin.site.register(OnetimeToken, OnetimeTokenAdmin)

class AlertInfoUserAdmin(admin.ModelAdmin):
    list_display = AlertInfoUser._meta.get_all_field_names()
admin.site.register(AlertInfoUser, AlertInfoUserAdmin)
