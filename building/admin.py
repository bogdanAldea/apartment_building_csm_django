from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Tenant)

admin.site.register(Building)
admin.site.register(Apartment)

admin.site.register(Utility)
admin.site.register(MutualUtil)
admin.site.register(IndividualUtil)

admin.site.register(Feature)
admin.site.register(FeatureLinked)