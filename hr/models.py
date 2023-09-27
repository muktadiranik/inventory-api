from django.db import models
from inventory.common.models import *
from inventory.common.models import *
from django.utils.translation import gettext_lazy as _
from month.models import MonthField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from inventory.common.validators import *


MARITAL_STATUS = (
    ('MARRIED', 'Married'),
    ('UNMARRID', 'Unmarrid',),
)

GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female',),
)

BLOOD_GROUP = (
    ('A+', '(A+)',),
    ('A-', '(A-)',),
    ('B+', '(B+)',),
    ('B-', '(B-)',),
    ('O+', '(O+)',),
    ('O-', '(O-)',),
    ('AB+', '(AB+)',),
    ('AB-', '(AB-)',),
)

LEAVE_STATUS = (
    ('APPROVED', 'Approved',),
    ('PENDING', 'Pending',),
    ('REJECTED', 'Rejected',),
)

ATTENDANCE_STARUS = (
    ('P', 'Present',),
    ('A', 'Absent'),
    ('LP', 'Late Present')
)

LEAVE_TYPE = (
    ('CL', 'Casual leave',),
    ('SL', 'Sick leave',),
    ('PH', 'Public holiday',),
    ('ML', 'Maternity leave',),
    ('PL', 'Paternity leave',),
    ('BL', 'Bereavement leave',),
    ('FML', 'Family and medical leave',),
    ('RL', 'Religious leave',),
    ('UL', 'Unpaid leave',),
    ('SL', 'Study leave',),
    ('OL', 'Other leave',),
)

JOB_TYPE = (
    ('FULL_TIME', 'Full Time',),
    ('PART_TIME', 'Part Time',),
    ("FULL_TIME_REMOTE", "Full Time Remote"),
    ("PART_TIME_REMOTE", "Part Time Remote"),
    ('CONTRACTUAL', 'Contractual',),
    ('TEMPORARY', 'Temporary',),
    ('INTERNSHIP', 'Internship',),
)

JOB_CIRCULAR_STATUS = (
    ("PUBLISHED", "Published"),
    ("UNPUBLISHED", "Unpublished"),
)

JOB_APPLICATION_STATUS = (
    ("PENDING", "Pending"),
    ("DECLINED", "Declined"),
    ("INTERVIEW", "Interview"),
    ("APPROVED", "Approved"),
    ("REJECTED", "Rejected"),
)


class Employee(models.Model):
    first_name = models.CharField(max_length=50, validators=[alphanumeric])
    last_name = models.CharField(max_length=50, validators=[alphanumeric])
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(validators=[email_regex])
    phone = models.CharField(max_length=15, unique=True, validators=[phone_regex, MinLengthValidator(11)])
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, validators=[alphanumeric])
    zip_code = models.CharField(max_length=50, validators=[zip_regex])
    department = models.ForeignKey('Department', on_delete=models.CASCADE,  null=True)
    job_title = models.ForeignKey('JobPosition', on_delete=models.CASCADE,  null=True)
    salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    resume = models.FileField(upload_to='employee/resume/', blank=True, null=True, validators=[validate_file_extension])
    date_of_joining = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.full_name == None:
            return self.first_name
        return self.full_name

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = str(self.first_name) + " " + str(self.last_name)
            
        if self.first_name and not self.last_name:
            self.full_name = str(self.first_name)

        if not self.first_name and self.last_name:
            self.full_name = str(self.last_name)
            
        super(Employee, self).save(*args, **kwargs)


class EmployeePrivateInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True)
    father_name = models.CharField(max_length=50, validators=[alphanumeric])
    mother_name = models.CharField(max_length=50, validators=[alphanumeric])
    gender = models.CharField(max_length=50, choices=GENDER)
    marital_status = models.CharField(max_length=50, choices=MARITAL_STATUS)
    spouse_name = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    children = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=50, choices=BLOOD_GROUP)
    dob = models.DateField(verbose_name='Date of birth', null=True)
    religion = models.CharField(max_length=50, validators=[alphanumeric])
    nationality = models.CharField(max_length=50, validators=[alphanumeric])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Private Info'
        verbose_name_plural = _('Private Informations')

    def __str__(self):
        return str(self.employee)


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class JobPosition(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Job Position'
        verbose_name_plural = _('Job Positions')


class JobCircular(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, null=True)
    salary = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    job_responsibilities = models.TextField()
    job_requirements = models.TextField()
    job_location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255, choices=JOB_TYPE)
    experience = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    deadline = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=255, choices=JOB_CIRCULAR_STATUS, default='UNPUBLISHED')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Job Circular'
        verbose_name_plural = _('Job Circulars')


class JobApplication(models.Model):
    first_name = models.CharField(max_length=50, validators=[alphanumeric])
    last_name = models.CharField(max_length=50, validators=[alphanumeric])
    email = models.EmailField(validators=[email_regex])
    phone = models.CharField(max_length=15, unique=True, validators=[phone_regex, MinLengthValidator(11)])
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, validators=[alphanumeric])
    zip_code = models.CharField(max_length=50, validators=[zip_regex])
    position = models.ForeignKey(JobPosition, on_delete=models.SET_NULL, null=True)
    circular = models.ForeignKey(JobCircular, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    resume = models.FileField(upload_to='application/resume/', null=True, validators=[validate_file_extension])
    career_objective = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    linkedin_profile = models.URLField(max_length=2555, null=True, blank=True)
    github_profile = models.URLField(max_length=2555, null=True, blank=True)
    status = models.CharField(max_length=255, choices=JOB_APPLICATION_STATUS, default='PENDING')

    def __str__(self):
        return str(self.position) + ' - ' + str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        verbose_name = 'Job Application'
        verbose_name_plural = _('Job Applications')


class Leave(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=LEAVE_STATUS, default='PENDING', blank=True, null=True)

    def __str__(self):
        return str(self.employee.full_name)


class Attendance(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ATTENDANCE_STARUS, default='A', null=True)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    @property
    def hours(self):
        end_minutes = self.time_out.hour*60 + self.time_out.minute
        start_minutes = self. time_in.hour*60 + self.time_in.minute
        return round((end_minutes - start_minutes) / 60, 2)

    def clean_fields(self, exclude=None):
        if self.time_in > self.time_out:
            raise ValidationError('Time in should be less than time out')

    def __str__(self):
        return str(self.employee.full_name)


class Payroll(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    month_year = MonthField("Month / Year", null=True)
    basic_salary = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False, default=0)
    conveyance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    house_rent_allowance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    medical_allowance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    special_allowance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return str(self.employee.full_name)

    def save(self, *args, **kwargs):
        self.total = self.basic_salary + self.conveyance + self.house_rent_allowance + self.medical_allowance + self.special_allowance
        super(Payroll, self).save(*args, **kwargs)
