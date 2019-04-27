# Generated by Django 2.2 on 2019-04-18 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abstract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=255)),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('submissionDeadline', models.DateField()),
                ('reviewDeadline', models.DateField()),
                ('conferenceDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(default='listener', max_length=32)),
                ('cId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(null=True, upload_to='uploads/')),
                ('accepted', models.BooleanField(null=True)),
                ('paperId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='confsite.Abstract')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramCommitteeMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(default='listener', max_length=32)),
                ('cId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.Conference')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='confsite.Login')),
                ('name', models.CharField(max_length=32)),
                ('website', models.CharField(max_length=32)),
                ('affiliation', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='SteeringCommittee',
            fields=[
                ('email', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='confsite.Login')),
                ('name', models.CharField(max_length=32)),
                ('website', models.CharField(max_length=32)),
                ('affiliation', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='borderline', max_length=32)),
                ('paperId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.Paper')),
                ('pcId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.ProgramCommitteeMember')),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('startHour', models.TimeField()),
                ('endHour', models.TimeField()),
                ('roomNumber', models.IntegerField()),
                ('pcId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.ProgramCommitteeMember')),
            ],
        ),
        migrations.CreateModel(
            name='ConferenceAuthorSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conferenceAuthorId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.ConferenceAuthor')),
                ('conferenceSessionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.ConferenceSession')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('abstractId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.Abstract')),
                ('pcId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.ProgramCommitteeMember')),
            ],
        ),
        migrations.AddField(
            model_name='abstract',
            name='authorId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='confsite.ConferenceAuthor'),
        ),
        migrations.AddField(
            model_name='programcommitteemember',
            name='pEmail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.Participant'),
        ),
        migrations.AddField(
            model_name='conferenceauthor',
            name='pEmail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confsite.Participant'),
        ),
    ]