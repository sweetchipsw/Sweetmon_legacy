from django.contrib import admin
# Register your models here.
from monitor.models import Profile, Machine, Crash, AuthInformation, Testcase, Issue, OnetimeToken, AlertInfoUser

def get_all_field_names(Model):
    return [f.name for f in Model._meta.get_fields()]

def exceptfield(list_display, fields=[]):
	# Remove fields that you won't show.
	if len(fields) == 0:
		return 0;
	for field in fields:
		list_display.remove(field)

class MachineAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Machine)
admin.site.register(Machine, MachineAdmin)

class CrashAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Crash)
    exceptfield(list_display,["crashlog", "comment", "link", "crash_file", "crash_hash"])
admin.site.register(Crash, CrashAdmin)

class TestcaseAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Testcase)
admin.site.register(Testcase,TestcaseAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Issue)
admin.site.register(Issue, IssueAdmin)

# Register information of fuzzer
class AuthInformationAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(AuthInformation)
    exceptfield(list_display,["password"])
admin.site.register(AuthInformation, AuthInformationAdmin)


class OnetimeTokenAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(OnetimeToken)
admin.site.register(OnetimeToken, OnetimeTokenAdmin)

class AlertInfoUserAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(AlertInfoUser)
admin.site.register(AlertInfoUser, AlertInfoUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = get_all_field_names(Profile)
admin.site.register(Profile, ProfileAdmin)
