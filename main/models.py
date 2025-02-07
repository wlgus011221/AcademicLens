from django.db import models
from django.conf import settings
from django.utils import timezone

class Affiliation(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'affiliation'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Author(models.Model):
    name = models.CharField(max_length=200)
    affiliation = models.TextField()

    class Meta:
        managed = False
        db_table = 'author'


class Country(models.Model):
    name = models.TextField()
    alpha_2 = models.CharField(max_length=2)
    alpha_3 = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'country'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Keyword(models.Model):
    keyword_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'keyword'


class Paper(models.Model):
    search = models.CharField(max_length=50)
    title = models.TextField()
    url = models.TextField(unique=True)
    date = models.DateField()
    citations = models.IntegerField()
    publisher = models.CharField(max_length=20)
    abstract = models.TextField()
    saved_count = models.IntegerField(default=0)  # 기본값을 0으로 설정

    class Meta:
        managed = False
        db_table = 'paper'


class PaperAffiliation(models.Model):
    paper = models.ForeignKey(Paper, models.DO_NOTHING)
    affiliation = models.ForeignKey(Affiliation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'paper_affiliation'


class PaperAuthor(models.Model):
    paper = models.ForeignKey(Paper, models.DO_NOTHING)
    author = models.ForeignKey(Author, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'paper_author'


class PaperCountry(models.Model):
    paper = models.ForeignKey(Paper, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'paper_country'


class PaperKeyword(models.Model):
    paper = models.ForeignKey(Paper, models.DO_NOTHING)
    keyword = models.ForeignKey(Keyword, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'paper_keyword'
        
        
class SavedPaper(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    

class RecentPaper(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)  # 논문 조회 시간

    class Meta:
        ordering = ['-viewed_at']  # 최신 순으로 정렬


class SearchKeyword(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.keyword