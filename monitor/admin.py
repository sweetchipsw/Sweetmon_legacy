from django.contrib import admin
from django.conf import settings
from monitor.models import Profile, Machine, Crash, Testcase, OnetimeToken, TelegramBot, EmailBot
from django.db.models import Q


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

	readonly_fields = ('crash_count', 'testcase', 'reg_date', 'pub_ip', 'pri_ip', 'token')

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner')
		return fields

	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user
		instance.save()
		form.save_m2m()
		return instance


class CrashAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Crash)
	exceptfield(list_display,["crashlog", "comment", "crash_file", "crash_hash"])

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields
		
	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner')
		fields[0][1]['fields'].remove('fuzzer')
		return fields

	def save_model(self, request, instance, form, change):
		user = request.user
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user
		instance.save()
		form.save_m2m()
		return instance


class TestcaseAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Testcase)

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(owner_id=request.user)
		return fields
		
	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner')
		return fields

	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user
		instance.save()
		form.save_m2m()
		return instance


class OnetimeTokenAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(OnetimeToken)


class EmailBotAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(EmailBot)
	exceptfield(list_display, ['email_pw_enc', 'email_pw', 'profile'])

	# DEPRECATED
	def profile(self, obj):
		return len(Profile.objects.filter(emailbot=obj))

	def get_queryset(self, request):
		# Get only current user's information or public id
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(Q(owner_id=request.user) | Q(is_public=True))
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner')
		fields[0][1]['fields'].remove('email_pw_enc')
		return fields

	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user
		instance.save()
		form.save_m2m()
		return instance


class TelegramBotAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(TelegramBot)
	exceptfield(list_display, ["profile"])

	def profile(self, obj):
		return len(Profile.objects.filter(telegram=obj))

	def get_queryset(self, request):
		fields = super(self.__class__, self).get_queryset(request)
		fields = fields.filter(Q(owner_id=request.user) | Q(is_public=True))
		return fields

	def get_fieldsets(self, request, obj=None):
		fields = super(self.__class__, self).get_fieldsets(request, obj)
		fields[0][1]['fields'].remove('owner')
		return fields

	def save_model(self, request, instance, form, change):
		user = request.user 
		instance = form.save(commit=False)
		if not change or not instance.owner:
			instance.owner = user
		instance.save()
		form.save_m2m()
		return instance



class ProfileAdmin(admin.ModelAdmin):
	list_display = get_all_field_names(Profile)
	exceptfield(list_display,["id"])

	def telegram(self, obj):
		return "asd"

	def profile_image(self, obj):
		return "asd1"

	readonly_fields = ('userkey',)

	if settings.USE_EMAIL_ALERT == False:
		readonly_fields += ('test_email', 'use_email_alert',)

	if settings.USE_TELEGRAM_ALERT == False:
		readonly_fields += ('test_telegram', 'use_telegram_alert', )

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

# admin.site.register(Machine, MachineAdmin)
# admin.site.register(Crash, CrashAdmin)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Testcase,TestcaseAdmin)
admin.site.register(EmailBot, EmailBotAdmin)
admin.site.register(TelegramBot, TelegramBotAdmin)
