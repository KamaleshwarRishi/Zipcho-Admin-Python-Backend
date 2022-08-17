from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from zipchoAdmin.models import ( interest, language, category, 
                                 gender, country )

from .managers import CustomUserManager

class User(AbstractUser):

    ZIPCHO_ADMIN = '1'
    CONTESTANT = '2'

    ROLE_CHOICES = (
        (ZIPCHO_ADMIN , 'Zipcho_Admin'),
        (CONTESTANT, 'Contestant')
    )
    
    email=models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    mobileNumber = models.CharField(max_length=13, blank=True, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES,
                            default=CONTESTANT, )
    termsAgreed = models.BooleanField(default=False)
    emailVerified = models.BooleanField(default=False)
    mobileNumberVerified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []   
    objects = CustomUserManager()
    def __str__(self):
        return self.email 


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, null=True)
    profileImage = models.ImageField(upload_to='profileImages',default='default.jpg')
    gender = models.ForeignKey(gender, null=True, on_delete=models.PROTECT)
    country = models.ForeignKey(country,null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def create_user_profile(sender, instance ,created, **kwargs):
    if created:
        print(f"Creating an empty profile for user ... {instance}")
        profile.objects.create(user=instance)

