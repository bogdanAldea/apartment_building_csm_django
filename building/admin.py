from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Building)
admin.site.register(Utility)
admin.site.register(MainUtil)