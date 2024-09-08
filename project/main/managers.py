from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError as e:
            return ValueError(_('Invalid email address'))

    def create_user(self, email, username, name, mobile_no, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('The Email is required'))

        if not username:
            raise ValueError(_('The username is required'))

        if not name:
            raise ValueError(_('The name is required'))
        
        if not mobile_no:
            raise ValueError(_('The mobile_no is required'))

        user = self.model(
            email=email,
            username=username,
            name=name,
            mobile_no=mobile_no
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, mobile_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_verified') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email, username, name, mobile_no,
                                password, **extra_fields)
        user.save(using=self._db)
        return user
    
    def verify_user(self, email):
        user = self.get(email=email)
        user.is_verified = True
        user.save()
        return user
