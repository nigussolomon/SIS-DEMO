# Generated by Django 4.2.2 on 2023-06-13 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm_base', '0003_level_remove_student_batch_year_delete_studentbatch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='academictimeline',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pm_base.level'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pm_base.level'),
            preserve_default=False,
        ),
    ]
