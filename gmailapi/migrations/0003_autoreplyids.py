# Generated by Django 2.2.2 on 2019-06-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gmailapi', '0002_auto_20190609_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoReplyIds',
            fields=[
                ('Reply_id', models.AutoField(primary_key=True, serialize=False)),
                ('Msg_id', models.CharField(max_length=100)),
                ('Label', models.CharField(max_length=100)),
                ('Date', models.CharField(max_length=100)),
                ('From', models.CharField(max_length=100)),
                ('To', models.CharField(max_length=100)),
                ('Subject', models.TextField()),
                ('Message', models.TextField()),
            ],
        ),
    ]
