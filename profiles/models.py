from django.db import models

from authentication.models import CustomUser



class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_registered = models.BooleanField(default=False)
    is_startup = models.BooleanField(default=True)
    person_position = models.CharField(max_length=50)
    official_name = models.CharField(max_length=255)
    common_info = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    edrpou = models.IntegerField()
    founded = models.SmallIntegerField()
    service_info = models.TextField()
    product_info = models.TextField()
    address = models.TextField()
    startup_idea = models.TextField()
    is_deleted = models.BooleanField(default=False)
    person_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)


class ProfilesActivity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class ProfilesCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

class ProfilesProfileActivities(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_id = models.ForeignKey('ProfilesActivity', on_delete=models.CASCADE)


class ProfilesImage(models.Model):
    id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

class ProfilesRegion(models.Model):
    name_en = models.CharField(max_length=128)
    name_ua = models.CharField(max_length=128)

class ProfilesProfileRegion(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    region = models.ForeignKey('ProfilesRegion', on_delete=models.CASCADE)
    is_official = models.BooleanField(default=False)

class ProfilesProfileCategories(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    category = models.ForeignKey('ProfilesCategory', on_delete=models.CASCADE)


class SavedCompany(models.Model):
    id = models.BigAutoField(primary_key=True)
    added_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_list')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_list_items')


class ViewedCompany(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'company'),)
