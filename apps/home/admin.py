# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from .models import Upload, User, SparePartGood, SparePartOutRecord, SparePartOutRequest


admin.site.register(User)
admin.site.register(SparePartGood)
admin.site.register(Upload)
admin.site.register(SparePartOutRecord)
admin.site.register(SparePartOutRequest)