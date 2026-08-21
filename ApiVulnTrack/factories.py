import factory
from projects.models import Project

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    is_active = True