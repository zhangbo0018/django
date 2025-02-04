# Generated by Django 4.2.3 on 2024-02-04 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("gender", models.BooleanField(default=1)),
                ("password", models.CharField(max_length=100)),
                ("is_admin", models.BooleanField(default=0)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "用户",
                "db_table": "t_user",
            },
        ),
        migrations.CreateModel(
            name="UserCategoryAffinity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("category_name", models.CharField(max_length=100)),
                ("affinity_score", models.FloatField()),
                ("update_time", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.user"
                    ),
                ),
            ],
            options={
                "verbose_name": "用户画像",
                "db_table": "t_category_affinity",
            },
        ),
    ]
