from django.db import models
from django_multitenant import fields as tenant_fields
from django_multitenant import models as tenant_models
from django.contrib.auth.models import User

class College(tenant_models.TenantModel):
    tenant_id = "id"
    name = models.CharField(
        help_text="name of the college",
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)


    is_active = models.BooleanField(
        help_text="identify if the organisation is active currently or not",
        default=True,
    )
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    



class Student(tenant_models.TenantModel):
    tenant_id = "college_id"
    college = models.ForeignKey(College, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.CASCADE)