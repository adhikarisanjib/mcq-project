from django.contrib import admin

from mcqapp.models import Chapter, Course, Exam, Questions, Subject

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Questions)
admin.site.register(Exam)
