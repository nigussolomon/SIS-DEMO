from django.contrib import admin
from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'entry_year', 'level','is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'level', 'entry_year')
    search_fields = ('first_name', 'last_name')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name','is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff',)
    search_fields = ('first_name', 'last_name')


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('programme_name', 'code',)

@admin.register(ProgrammeType)
class ProgrammeTypeAdmin(admin.ModelAdmin):
    list_display = ('programme_type_name', 'code',)

@admin.register(ProgrammeLevel)
class ProgrammeLevelAdmin(admin.ModelAdmin):
    list_display = ('programme_level_name', 'code',)


@admin.register(AcademicProgramme)
class AcademicProgrammeAdmin(admin.ModelAdmin):
    list_display = ('programme', 'programme_level', 'programme_type', 'duration')
    list_filter = ('programme__programme_name', 'programme_level__programme_level_name', 'programme_type__programme_type_name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'credit_hours', 'academic_programme')


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('code', 'year', 'is_current',)
    list_filter = ('is_current',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('code', 'semester_name', 'is_current',)
    list_filter = ('is_current',)

@admin.register(AcademicTimeLine)
class AcademicTimeLineAdmin(admin.ModelAdmin):
    list_display = ('academic_programme', 'level',  'academic_year', 'semester', 'start_date', 'end_date', 'mid_exam_start_date', 'final_exam_start_date')
    list_filter = ('academic_year__year', 'semester__semester_name', 'level__level_name',)

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'academic_year', 'course_status')
    list_filter = ('semester__semester_name', 'academic_year__year', 'course_status',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_name',)

@admin.register(StudentGrade)
class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'continous_assesment', 'mid_exam', 'final_exam', 'total', 'grade_letter',)

@admin.register(PaymentInformation)
class ProjectInformationAdmin(admin.ModelAdmin):
    list_display = ('student', 'payment_reference', 'amount', 'payment_date', 'status')

@admin.register(CourseEligibility)
class CourseEligibilityAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_courses', 'academic_time_line',)
    def get_courses(self, obj):
        return ", ".join([str(c) for c in obj.course.all()])

    get_courses.short_description = "Courses"
