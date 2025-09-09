from django.db import models
from django.contrib.auth.models import User


class Registration(models.Model):
    input_skill = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    user_role = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Job_prediction(models.Model):
    input_skill = models.CharField(max_length=200, null=True)
    rec_job_title = models.CharField(max_length=200, null=True)
    rec_company = models.CharField(max_length=200, null=True)
    rec_location = models.CharField(max_length=200, null=True)
    rec_work_type = models.CharField(max_length=200, null=True)
    rec_similarity_score = models.CharField(max_length=200, null=True)
    rec_description = models.TextField(max_length=600, null=True)
    prd_reg = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True)


class Job_post(models.Model):
    designation = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    age_range = models.CharField(max_length=200, null=True)
    skills_needed = models.CharField(max_length=200, null=True)
    pst_reg = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True)