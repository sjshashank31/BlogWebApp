from django.db import models
import random, string,itertools
from django.conf import settings
from django.utils.text import slugify


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to='images/blogs/%y-%m-%d')
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def _generate_slug(self):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        value = self.title + res
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Blog.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def slug_save(self, *args, **kwargs):
        self._generate_slug()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class BlogExplanation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.ForeignKey(Blog, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/blogs/extra/%y-%m-%d')
    caption = models.TextField()

    def __str__(self):
        return self.slug.slug

