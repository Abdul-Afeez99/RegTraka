from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager,
                                        AbstractBaseUser, PermissionsMixin)

# Create your models here.
# Custom user manager to manage our users
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_administrator(self, email, password, **extra_fields):
        """
        Create an administrator with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_administrator = True
        user.is_instructor = False
        user.save()
        return user
    
    def create_instructor(self, email, password, **extra_fields):
        """
        Create an instructor with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_administrator = False
        user.is_instructor = True
        user.save()
        

    
#Get all users with the role is_administrator   
class AdministratorManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_administrator=True)

#Get all users with the role is_teacher    
class InstructorManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)

# Custom user model to handle our users 
# Username field is set to user email address   
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    is_superuser = None
    is_staff = None
    first_name = None
    last_name = None
    is_administrator = models.BooleanField(null=True)
    is_instructor = models.BooleanField(null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        
    ]
    
    
    
    objects = CustomUserManager()
    administrator = AdministratorManager()
    instructor = InstructorManager()
        
# Administrator model
class Administrator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    

# Instructors model
class Instructor(models.Model):
    sex = [
        ("MALE", "Male"),
        ("FEMALE", 'Female')
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='school_instructors')
    name = models.CharField(max_length= 50, null=True, blank=True)
    gender = models.CharField(choices=sex, max_length=20, null=True)
    
class Year(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    school = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='school_classes')
    
    
    
# Courses model
class Courses(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)   
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='course_year')
    credit = models.IntegerField(null=True, blank=True)
    school = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='school_courses') 
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="instructor_courses")

       
# Student model
class Student(models.Model):
    sex = [
        ("MALE", "Male"),
        ("FEMALE", 'Female')
    ]
    name = models.CharField(max_length=80, null=True, blank=True)
    school = models.ForeignKey(Administrator, on_delete=models.CASCADE, related_name='student_in_school')
    matric_no = models.CharField(max_length=30, null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="student_in_class")
    gender = models.CharField(choices=sex, max_length=20, null=True)
    image = models.ImageField(upload_to= 'images/')
    courses = models.ManyToManyField(Courses, related_name='student_courses')
    