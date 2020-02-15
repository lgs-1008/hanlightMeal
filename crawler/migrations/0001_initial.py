# Generated by Django 3.0.3 on 2020-02-15 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MealModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(default=0)),
                ('date', models.IntegerField(default=0)),
                ('detail', models.CharField(max_length=150, null=True)),
            ],
        ),
    ]
