# Generated by Django 4.2.6 on 2023-10-22 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(default='available', max_length=20)),
                ('capacity', models.PositiveIntegerField(default=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('draws', models.PositiveIntegerField(default=0)),
                ('total_games', models.PositiveIntegerField(default=0)),
                ('rating', models.FloatField(default=50.0)),
                ('last_online', models.DateTimeField(blank=True, null=True)),
                ('current_lobby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.lobby')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.player')),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.lobby')),
            ],
        ),
        migrations.AddField(
            model_name='lobby',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hosted_lobbies', to='base.player'),
        ),
        migrations.AddField(
            model_name='lobby',
            name='members',
            field=models.ManyToManyField(related_name='joined_lobbies', to='base.player'),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.JSONField()),
                ('result', models.JSONField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.lobby')),
                ('players', models.ManyToManyField(to='base.player')),
            ],
        ),
    ]
