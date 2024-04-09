from django.db import models


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()


class Feature(models.Model):
    feature_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()


class Banner(models.Model):
    banner_id = models.AutoField(primary_key=True)
    tag_ids = models.ManyToManyField(Tag)
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE)
    content = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#     Todo: add __str__
