from django.contrib import admin
# Register your models here.
from monitor.models import Profile, Machine, Crash, AuthInformation, Testcase, Issue, OnetimeToken, TelegramBot

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

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner') # Hide field
		return fields
	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user # set owner
		instance.save()
		form.save_m2m()
		return instance
admin.site.register(Machine, MachineAdmin)

class CrashAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Crash)
	exceptfield(list_display,["crashlog", "comment", "link", "crash_file", "crash_hash"])
	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields
		
	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner') # Hide field
		return fields
	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user # set owner
		instance.save()
		form.save_m2m()
		return instance
admin.site.register(Crash, CrashAdmin)

class TestcaseAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Testcase)
	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields
		
	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner') # Hide field
		return fields
	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user # set owner
		instance.save()
		form.save_m2m()
		return instance

admin.site.register(Testcase,TestcaseAdmin)

class IssueAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Issue)
	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner') # Hide field
		return fields
	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user # set owner
		instance.save()
		form.save_m2m()
		return instance

admin.site.register(Issue, IssueAdmin)

# Register information of fuzzer
class AuthInformationAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(AuthInformation)
	exceptfield(list_display,["password"])
admin.site.register(AuthInformation, AuthInformationAdmin)


class OnetimeTokenAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(OnetimeToken)
admin.site.register(OnetimeToken, OnetimeTokenAdmin)

class TelegramBotAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(TelegramBot)
	exceptfield(list_display, ["profile"])

	def profile(self, obj):
		return len(Profile.objects.filter(telegram=obj))

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user, is_public=True)
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner') # Hide field
		return fields
	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user # set owner
		instance.save()
		form.save_m2m()
		return instance

admin.site.register(TelegramBot, TelegramBotAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Profile)
	# print(list_display)
	exceptfield(list_display,["id", "public_key"])
	def telegram(self, obj):
		return "asd"

	readonly_fields = ('userkey',)

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner') # Hide field
		return fields

	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user # set owner
		instance.save()
		form.save_m2m()
		return instance

admin.site.register(Profile, ProfileAdmin)
