from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
from dirtyfields import DirtyFieldsMixin
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token

from .utils import compress_image


class UserProfile(models.Model, DirtyFieldsMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                verbose_name=_('User'))
    phone_number = models.CharField(max_length=15, blank=True, null=True,
                                    verbose_name=_('Phone Number'))
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Address'))
    about = models.TextField(max_length=200, blank=True, null=True, verbose_name=_('About'))
    photo = models.ImageField(upload_to='profile/', blank=True, null=True, verbose_name=_('Photo'))
    
    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def delete_old_image(self):
        if self.pk:
            old_instance = UserProfile.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                old_instance.photo.delete(save=False)
    
    def save(self, *args, **kwargs) -> None:
        self.delete_old_image()
        
        if not self.pk or 'photo' in self.get_dirty_fields():
            if self.photo:
                compressed_buffer = compress_image(self.photo, 20)
                self.photo.save(self.photo.name, ContentFile(compressed_buffer.getvalue()), save=False)
            
        super().save(*args, **kwargs)
    
    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        self.photo.delete(save=False)
        return super().delete(using, keep_parents)


class UserView(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_view',
                                verbose_name=_('User'))
    pages = models.TextField(max_length=300, verbose_name=_('Pages'))
    reports = models.TextField(max_length=300, verbose_name=_('Reports'))
    tables = models.TextField(max_length=1200, verbose_name=_('Tables'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Is Admin'))
    
    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = _('User View')
        verbose_name_plural = _('User Views')


class ActiveUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='last_seen',
                                verbose_name=_('User'))
    last_seen = models.DateTimeField(default=timezone.now, verbose_name=_('Last Seen'))
    
    @property
    def online(self):
        try:
            token = Token.objects.get(user=self.user)
            return timezone.now() - self.last_seen < timedelta(minutes=1)
        except Token.DoesNotExist:
            return False
    
    def __str__(self):
        return f'{self.user.username}: {"Online" if self.online else "Offline"}'
    
    class Meta:
        verbose_name = _('Active User')
        verbose_name_plural = _('Active Users')