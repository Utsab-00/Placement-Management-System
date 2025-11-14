from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100, default="Unknown Student")
    student_id = models.CharField(max_length=50, unique=True, default="000000")
    email = models.EmailField(null=True, unique=True, blank=True, default="student@example.com")
    phone_number = models.CharField(max_length=16, null=True, blank=True, default="0000000000")
    branch = models.CharField(max_length=100, null=True, blank=True, default="Unknown Branch")
    year_of_study = models.CharField(max_length=20, null=True, blank=True, default="First Year")
    cgpa = models.FloatField(null=True, blank=True, default=0.0)
    skills = models.TextField(null=True, blank=True, default="No skills listed")
    resume_link = models.URLField(null=True, blank=True, default="https://example.com")
    password = models.CharField(max_length=128, null=True, blank=True, default="password")  # hashed password
    verified = models.BooleanField(default=False)
    class Meta:
        db_table = 'student'

    def save(self, *args, **kwargs):
        """Only hash the password if it's not already hashed."""
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'argon2$', 'bcrypt$', 'sha1$')):  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Verify the password when logging in."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name


class Company(models.Model):
    company_name = models.CharField(max_length=100, default="Unknown Company")
    company_website = models.URLField(null=True, blank=True, default="https://example.com")
    industry = models.CharField(max_length=100, null=True, blank=True, default="Unknown Industry")
    company_address = models.TextField(null=True, blank=True, default="No address provided")
    contact_name = models.CharField(max_length=100, default="Unknown Contact")
    company_email = models.EmailField(default="company@example.com")
    company_phone = models.CharField(max_length=16, null=True, blank=True, default="0000000000")
    job_profiles = models.TextField(null=True, blank=True, default="No job profiles listed")
    location = models.CharField(max_length=100, null=True, blank=True, default="Unknown Location")
    eligibility = models.TextField(null=True, blank=True, default="No eligibility criteria")
    selection_process = models.TextField(null=True, blank=True, default="No selection process")
    ctc = models.CharField(max_length=50, null=True, blank=True, default="Not specified")
    internship = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    other_info = models.TextField(null=True, blank=True, default="No additional info")
    password = models.CharField(max_length=128, null=True, blank=True, default="password")  # Increased for hashed passwords
    verified = models.BooleanField(default=False)
    class Meta:
        db_table = 'company'

    def save(self, *args, **kwargs):
        """Only hash the password if it's not already hashed."""
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'argon2$', 'bcrypt$', 'sha1$')):  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Verify the password when logging in."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.company_name


class Admin(models.Model):
    admin_name = models.CharField(max_length=100, default="Admin Name")
    admin_id = models.CharField(max_length=50, unique=True, default="unknown")
    admin_email = models.EmailField(unique=True, default="admin@example.com")
    admin_phone = models.CharField(max_length=16, null=True, blank=True, default="0000000000")
    department = models.CharField(max_length=100, default="Unknown Department")
    role = models.CharField(
        max_length=20,
        choices=[('Placement Head', 'Placement Head'), 
                 ('Placement Officer', 'Placement Officer'), 
                 ('Coordinator', 'Coordinator')],
        default='Coordinator'
    )
    experience = models.PositiveIntegerField(null=True, blank=True, default=0)
    password = models.CharField(max_length=128, default="password")
    verified = models.BooleanField(default=False)
    class Meta:
        db_table = 'admin'

    def save(self, *args, **kwargs):
        """Only hash the password if it's not already hashed."""
        if not self.password.startswith(('pbkdf2_sha256$', 'argon2$', 'bcrypt$', 'sha1$')):  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Verify the password when logging in."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.admin_name
