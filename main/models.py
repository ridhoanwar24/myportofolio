import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Education(models.Model):
    EDUCATION_CHOICES = [
        ('elementary-school', 'Elementary-School'),
        ('junior-high-school', 'Junior-High-School'),
        ('high-school', 'High-School'),
        ('university', 'University'), 
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=EDUCATION_CHOICES, default='')
    thumbnail = models.URLField(blank=True, default='')
    year_started = models.IntegerField()
    year_ended = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.institution_name

    @property
    def is_ongoing(self):
        return self.year_ended is None