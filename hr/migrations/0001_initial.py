# Generated by Django 3.2.15 on 2022-12-04 10:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import month.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator(message="Email must be entered in the format: 'yourmail@gamil.com' ", regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')])),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('zip_code', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Zip code must be entered in the format: 999999. Up to 6 digits allowed', regex='^\\d{4,6}$')])),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='employee/resume/')),
                ('date_of_joining', models.DateField()),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.department')),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_year', month.models.MonthField(null=True, verbose_name='Month / Year')),
                ('basic_salary', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('conveyance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('house_rent_allowance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('medical_allowance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('special_allowance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('CL', 'Casual leave'), ('SL', 'Sick leave'), ('PH', 'Public holiday'), ('ML', 'Maternity leave'), ('PL', 'Paternity leave'), ('BL', 'Bereavement leave'), ('FML', 'Family and medical leave'), ('RL', 'Religious leave'), ('UL', 'Unpaid leave'), ('SL', 'Study leave'), ('OL', 'Other leave')], max_length=50, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField()),
                ('status', models.CharField(blank=True, choices=[('APPROVED', 'Approved'), ('PENDING', 'Pending'), ('REJECTED', 'Rejected')], default='PENDING', max_length=50, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
        migrations.CreateModel(
            name='JobPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
            ],
            options={
                'verbose_name': 'Job Position',
                'verbose_name_plural': 'Job Positions',
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator(message="Email must be entered in the format: 'yourmail@gamil.com' ", regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')])),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('zip_code', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='Zip code must be entered in the format: 999999. Up to 6 digits allowed', regex='^\\d{4,6}$')])),
                ('date', models.DateField(auto_now_add=True)),
                ('resume', models.FileField(null=True, upload_to='application/resume/')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.jobposition')),
            ],
            options={
                'verbose_name': 'Job Application',
                'verbose_name_plural': 'Job Applications',
            },
        ),
        migrations.CreateModel(
            name='EmployeePrivateInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('mother_name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=50)),
                ('marital_status', models.CharField(choices=[('MARRIED', 'Married'), ('UNMARRID', 'Unmarrid')], max_length=50)),
                ('spouse_name', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('children', models.CharField(max_length=100)),
                ('blood_group', models.CharField(choices=[('A+', '(A+)'), ('A-', '(A-)'), ('B+', '(B+)'), ('B-', '(B-)'), ('O+', '(O+)'), ('O-', '(O-)'), ('AB+', '(AB+)'), ('AB-', '(AB-)')], max_length=50)),
                ('dob', models.DateField(null=True, verbose_name='Date of birth')),
                ('religion', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('nationality', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z-,-.-_ ]+$', 'Only alphanumeric characters are allowed.')])),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
                ('employee', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.employee')),
            ],
            options={
                'verbose_name': 'Private Info',
                'verbose_name_plural': 'Private Informations',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.jobposition'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('LP', 'Late Present')], default='A', max_length=50, null=True)),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('time_out', models.TimeField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.company')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
    ]
