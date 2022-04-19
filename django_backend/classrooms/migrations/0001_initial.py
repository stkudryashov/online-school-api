# Generated by Django 4.0.4 on 2022-04-19 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название группы')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='Дата начала учебы')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Дата завершения учебы')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='classrooms', to='courses.course', verbose_name='Название курса')),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classrooms', to=settings.AUTH_USER_MODEL, verbose_name='Ментор')),
            ],
            options={
                'verbose_name': 'Учебная группа',
                'verbose_name_plural': 'Учебные группы',
            },
        ),
        migrations.CreateModel(
            name='StudentClassroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Закончил обучение')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classrooms.classroom', verbose_name='Группа')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Учебная группа ученика',
                'verbose_name_plural': 'Учебные группы учеников',
                'ordering': ['classroom'],
            },
        ),
        migrations.AddConstraint(
            model_name='studentclassroom',
            constraint=models.UniqueConstraint(fields=('classroom', 'student'), name='unique_student_classroom'),
        ),
    ]
