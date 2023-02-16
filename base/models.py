import datetime
import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=31,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=7,
        decimal_places=2,
    )
    discount = models.IntegerField(
        verbose_name=_("Discount"),
    )

    def __str__(self):
        return self.name


class UserTypeManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class UserType(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        _("Name"),
        max_length=31,
        unique=True,
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("Permissions"),
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Date Created"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Date Updated"),
        auto_now=True,
        editable=False,
    )

    objects = UserTypeManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


# A few helper functions for User creation.
def get_user_avatar(user, filename):
    return f"{user.id}/avatars/{filename}"


def get_default_avatar():
    return "default/dummy_image.png"


def get_email_verified_value():
    if settings.DEBUG:
        return True
    return False


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = "get_%s_permissions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, "has_perm"):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, "has_module_perms"):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("User must have an email address.")
        if not name:
            raise ValueError("User must have a name.")
        user = self.model(
            email=self.normalize_email(email=email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_email_verified = True
        user.save(using=self._db)
        return user

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError("backend must be a dotted import path string (got %r)." % backend)
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=127,
        unique=True,
        error_messages={
            "null": _("Email field is required."),
            "unique": _("An account with that email already exists. Please login to continue."),
            "invalid": _("Enter a valid email address."),
        },
    )
    name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=255,
        null=True,
        blank=True,
    )
    usertype = models.ForeignKey(
        UserType,
        on_delete=models.SET_NULL,
        related_name="usertype",
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        default=get_default_avatar,
        upload_to=get_user_avatar,
    )
    is_email_verified = models.BooleanField(
        verbose_name=_("Email Verification Status"),
        default=get_email_verified_value,
        help_text=_("Designates whether this user is verified or not."),
    )
    is_active = models.BooleanField(
        verbose_name=_("Active Status"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this field instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        verbose_name=_("Staff Status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(
        _("Superuser Status"),
        default=False,
        help_text=_("Designates that this user has all permissions without explicitly assigning them."),
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("Permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="permission_set",
        related_query_name="user",
    )
    last_login = models.DateTimeField(
        verbose_name=_("Last Login"),
        auto_now=True,
    )
    date_joined = models.DateTimeField(
        verbose_name=_("Date Joined"),
        auto_now_add=True,
        editable=False,
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-date_joined",)

    def __str__(self):
        return self.email

    def get_avatar_name(self):
        return str(self.avatar)[str(self.avatar).index(f"{self.id}/avatars/") :]

    def get_fields_and_values(self):
        user = [
            ("email", self.email),
            ("name", self.name),
            ("avatar", self.avatar),
            ("is_active", self.is_active),
            ("last_login", self.last_login),
            ("date_joined", self.date_joined),
        ]
        return user

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "user")

    def get_usertype_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        usertypes. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, "usertype")

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, "all")

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class Token(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        editable=False,
    )
    token = models.CharField(
        verbose_name=_("Token"),
        max_length=256,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Date Created"),
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.user.name

    @property
    def is_expired(self):
        return self.created_at.replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(
            minutes=10,
        ) < datetime.datetime.now(datetime.timezone.utc)
