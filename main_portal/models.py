from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserApproval(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status_type = [(1, 'APPROVE'), (2, 'NOT APPROVED')]
    status = models.IntegerField(choices=status_type, default=2)
    def __str__(self):
        return f"{self.student.first_name}  | {self.status} "


class Update(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_posted.date()} | {self.student.first_name} | {self.title} "
