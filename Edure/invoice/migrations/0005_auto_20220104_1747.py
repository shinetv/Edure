# Generated by Django 3.2.3 on 2022-01-04 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_stud_reg_stud_idd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stud_reg',
            name='End_date',
        ),
        migrations.RemoveField(
            model_name='stud_reg',
            name='Join_date',
        ),
    ]
