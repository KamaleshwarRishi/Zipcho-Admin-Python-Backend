from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email  :
            raise ValueError("The Email must be set")
        if not password : 
            raise ValueError("The Password must be set")
        
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,password,**extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        #extra_fields.setdefault('role', 1)
        #f extra_fields.get('role') != 1 :
        #    raise ValueError('Superuser must have a role of Admin')
        return self.create_user(email, password, **extra_fields)
