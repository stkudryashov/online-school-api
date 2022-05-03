# Generated by Django 4.0.4 on 2022-05-03 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='Название курса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='CourseModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.PositiveIntegerField(verbose_name='Порядок модуля в курсе')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='modules.module', verbose_name='Модуль')),
            ],
            options={
                'verbose_name': 'Модуль курса',
                'verbose_name_plural': 'Модули курса',
                'ordering': ['course', 'order_number'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='modules',
            field=models.ManyToManyField(through='courses.CourseModule', to='modules.module', verbose_name='Модули курса'),
        ),
    ]