from django.contrib import admin

from .models import *


admin.site.register(PolicyCategory)
admin.site.register(PolicyCriterion)
admin.site.register(Institution)
admin.site.register(SocialMediaLink)
admin.site.register(InstitutionEmail)
admin.site.register(InstitutionPolicy)
admin.site.register(MessageTemplate)
