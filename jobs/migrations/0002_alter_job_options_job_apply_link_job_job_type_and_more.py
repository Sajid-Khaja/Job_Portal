# Generated by Django 5.1.6 on 2025-03-04 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-posted_on']},
        ),
        migrations.AddField(
            model_name='job',
            name='apply_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Remote', 'Remote'), ('Contract', 'Contract')], default='Full-time', max_length=20),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
