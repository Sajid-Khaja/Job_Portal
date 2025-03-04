from django.db import models

class Job(models.Model):
    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
        ('Contract', 'Contract'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='Full-time')
    apply_link = models.URLField(blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']  # Show latest jobs first

    def __str__(self):
        return f"{self.title} - {self.company}"
