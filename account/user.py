# import secrets
# import uuid

# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils.translation import ugettext_lazy as _

# from accounts.managers import CustomUserManager
# from painless.utils.models.mixins import Sku_Mixin
# from painless.utils.models.validations import PersianPhoneNumberValidator


# class CustomUser(Sku_Mixin, AbstractUser):
#     username = None
#     phone_number_validator = PersianPhoneNumberValidator()
#     phone_number = models.CharField(
#         _('phone number'),
#         unique=True,
#         max_length=15,
#         validators=[phone_number_validator],
#         error_messages={
#             'unique': _("A user with that phone number already exists."),
#         },
#     )
#     email = models.EmailField(
#         _('email address'),
#         null=True,
#         unique=True,
#         blank=True
#     )
#     secret = models.UUIDField(default=uuid.uuid4, editable=False)
#     is_phone_confirmed = models.BooleanField(
#         _('Is phone confirmed'),
#         default=False
#     )
#     is_email_confirmed = models.BooleanField(
#         _('Is email confirmed'),
#         default=False
#     )

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.phone_number

#     def save(self, *args, **kwargs):
#         if not self.sku:
#             self.sku = secrets.token_urlsafe(16)
#         if self.email == '':
#             self.email = None
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = _('User')
#         verbose_name_plural = _('Users')



#we can create Profile model and user our customuser
