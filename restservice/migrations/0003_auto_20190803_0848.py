# Generated by Django 2.2.2 on 2019-08-03 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restservice', '0002_auto_20190803_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('pkid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='departments',
            name='institute_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='institute_department', to='restservice.Institute'),
            preserve_default=False,
        ),
    ]
