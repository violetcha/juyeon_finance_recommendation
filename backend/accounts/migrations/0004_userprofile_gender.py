from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(
                blank=True,
                choices=[
                    ('unknown', '선택 안 함'),
                    ('male', '남성'),
                    ('female', '여성'),
                ],
                default='unknown',
                max_length=20,
            ),
        ),
    ]
