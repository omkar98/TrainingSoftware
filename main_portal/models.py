from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserDetail(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    student_class_cat = [(1, 'SY-CSE-A'), (2, 'SY-CSE-B'), (3,'TY-CSE-A'), (4,'TY-CSE-B'), (5,'SY-IT'), (6,'TY-IT'), (7,'SY-EnTC'), (8,'TY-EnTC')]
    student_class = models.IntegerField(choices=student_class_cat, default=0)
    status_type = [(1, 'APPROVE'), (2, 'NOT APPROVED')]
    status = models.IntegerField(choices=status_type, default=2)
    def getClass(self):
        return self.student_class_cat[self.student_class-1][1]
    stud_class = property(getClass)
    def __str__(self):
        return f"{self.student}  | {self.student_class_cat[self.student_class-1][1]} | {self.status_type[self.status-1][1]}"


class Update(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_posted.date()} | {self.student.first_name} | {self.title} "
