# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    comment = models.CharField(max_length=256)
    created_time = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    student = models.ForeignKey('Student', models.DO_NOTHING)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'comment'


class Student(models.Model):
    student_name = models.CharField(max_length=16)
    student_password = models.CharField(max_length=16)
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student_name

    class Meta:
        db_table = 'student'


class Teacher(models.Model):
    teacher_name = models.CharField(max_length=16)
    teacher_password = models.CharField(max_length=16)
    crouse = models.CharField(max_length=16)
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.teacher_name

    class Meta:
        db_table = 'teacher'
