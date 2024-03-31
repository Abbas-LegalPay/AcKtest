from django.contrib.auth.models import AbstractUser, PermissionsMixin, _user_has_perm
from django.db import models
from ..managers import AccuknoxUserManager


class AccuKnoxUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = AccuknoxUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.email:
            return f"{self.email}"
        return f"{self.id}"

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        if self.is_superuser and self.is_staff:
            return True
        has_perm = _user_has_perm(self, perm, obj)
        return has_perm

    class Meta:
        db_table = "accuknox_users_details"
        verbose_name = "AccuKnox User Detail"
        verbose_name_plural = "AccuKnox User Details"
