
import factory
from . import models

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.VulnTrackAccounts

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'password123')