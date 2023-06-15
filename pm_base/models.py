from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.db import models



class Level(models.Model):
    level_name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.level_name}"
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def add_to_group(self, user, group_name):
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    def remove_from_group(self, user, group_name):
        group = Group.objects.get(name=group_name)
        user.groups.remove(group)

    def is_in_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists()

class Student(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    entry_year = models.IntegerField(default=2023)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

class Teacher(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

class Programme(models.Model):
    code = models.CharField(max_length=20, unique=True)
    programme_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.code} - {self.programme_name}"
    
class ProgrammeType(models.Model):
    code = models.CharField(max_length=20, unique=True)
    programme_type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.code} - {self.programme_type_name}"

class ProgrammeLevel(models.Model):
    code = models.CharField(max_length=20, unique=True)
    programme_level_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.code} - {self.programme_level_name}"

class AcademicProgramme(models.Model):
    duration = models.IntegerField()
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    programme_type = models.ForeignKey(ProgrammeType, on_delete=models.CASCADE)
    programme_level = models.ForeignKey(ProgrammeLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.programme_level.programme_level_name} - {self.programme.programme_name} - {self.programme_type.programme_type_name} - {self.duration} years"
    

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    credit_hours = models.FloatField()
    ects = models.FloatField()
    lecture_hours = models.FloatField()
    lab_hours = models.FloatField()
    academic_programme = models.ForeignKey(AcademicProgramme, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"
    
class CourseFee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.code}"
    
    
class AcademicYear(models.Model):
    code = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}"
    
    @staticmethod
    def get_current_year():
        try:
            return AcademicYear.objects.get(is_current=True)
        except AcademicYear.DoesNotExist:
            return None
    
class Semester(models.Model):
    code = models.CharField(max_length=20, unique=True)
    semester_name = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.semester_name}"
    
    @staticmethod
    def get_current_semester():
        try:
            return Semester.objects.get(is_current=True)
        except Semester.DoesNotExist:
            return None
    
class AcademicTimeLine(models.Model):
    academic_programme = models.ForeignKey(AcademicProgramme, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    start_date = models.DateField()
    mid_exam_start_date = models.DateField()
    final_exam_start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.academic_year} - {self.semester}"
    
class CourseRegistration(models.Model):
    Passed = 'passed'
    Failed = 'failed'
    Pending = 'pending'
    Stalled = 'stalled'
    STATUSES = (
        (Passed, 'Passed'),
        (Failed, 'Failed'),
        (Pending, 'Pending'),
        (Stalled, 'Stalled'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    course_status = models.CharField(max_length=20, choices=STATUSES, default=Pending)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.email} - {self.course} - {self.academic_year} - {self.semester} - {self.course_status}"
    
class StudentGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    continous_assesment = models.IntegerField()
    mid_exam = models.IntegerField()    
    final_exam = models.IntegerField()
    total = models.IntegerField()
    grade_letter = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.student.email} - {self.grade_letter}"
    
class PaymentInformation(models.Model):
    Complete = 'Complete'
    Incomplete = 'Incomplete'
    FirstInstallmentComplete = 'First Installment Complete'
    Stalled = 'stalled'
    STATUSES = (
        (Complete, 'Complete'),
        (Incomplete, 'Incomplete'),
        (FirstInstallmentComplete, 'First Installment Complete'),
        (Stalled, 'Stalled'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_reference = models.CharField(max_length=100)
    amount = models.IntegerField()
    with_penality = models.BooleanField(default=False)
    payment_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUSES, default=Incomplete)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.email} - {self.amount} - {self.payment_date}"

class CourseEligibility(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name="courses")
    academic_time_line = models.ForeignKey(AcademicTimeLine, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.email}"