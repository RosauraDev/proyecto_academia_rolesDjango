from django.contrib import admin
from core.models import *


class CourseAdmin(admin.ModelAdmin):
    list_display=('name', 'teacher', 'class_quantity')
    list_filter=('teacher',)
admin.site.register(Course, CourseAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    list_display=('course', 'student', 'enabled')
    list_filter=('course', 'student', 'enabled')
admin.site.register(Registration, RegistrationAdmin)


class AttendenceAdmin(admin.ModelAdmin):
    list_display=('course', 'student', 'date', 'present')
    list_filter=('course', 'student', 'date', 'present')
admin.site.register(Attendance, AttendenceAdmin)


class MarkAdmin(admin.ModelAdmin):
    list_display=('course', 'student', 'mark_1', 'mark_2', 'mark_3', 'average')
    list_filter=('course', 'student')
admin.site.register(Mark, MarkAdmin)