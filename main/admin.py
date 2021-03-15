from django.contrib import admin

from main.models import Course, CourseImage, Category, Comment


class CourseImageInline(admin.TabularInline):
    model = CourseImage
    max_num = 10
    min_num = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseImageInline, ]



admin.site.register(Category)
admin.site.register(Comment)
