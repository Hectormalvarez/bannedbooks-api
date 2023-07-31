# Generated by Django 4.1.7 on 2023-07-31 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_ban', models.CharField(max_length=50)),
                ('secondary_author', models.CharField(blank=True, max_length=100, null=True)),
                ('illustrator', models.CharField(blank=True, max_length=100, null=True)),
                ('translator', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=100)),
                ('date_of_challenge_removal', models.CharField(max_length=50)),
                ('origin_of_challenge', models.CharField(max_length=100)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bans', to='books.book')),
            ],
        ),
    ]
