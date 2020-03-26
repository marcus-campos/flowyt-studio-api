import random

from django.conf import settings
from django.utils.text import slugify

from apps.teams.models import Team


class SubDomainBuilder:
    COMPANY_SUFFIXES = [
        "office",
        "subsidiary",
        "inc",
        "firm",
        "business",
        "group",
        "corp",
        "corporation",
        "comp",
        "company",
        "central",
        "area",
    ]

    def build_subdomain_url(self, organization, team):
        subdomain = slugify("{0}-{1}".format(organization, team))
        url = self._build_full_url(subdomain)
        exists = self._subdomain_exists(url)
        if exists:
            url = self._random_subdomain(subdomain)
        return url

    def _random_subdomain(self, subdomain):
        url = self._suffixed_subdomain(subdomain)
        if not url:
            url = self._numbered_subdomain(subdomain)
        return url

    def _build_full_url(self, subdomain):
        return "{0}{1}.{2}".format(settings.BASE_PROTOCOL, subdomain, settings.BASE_DOMAIN_URL)

    def _subdomain_exists(self, url):
        return Team.objects.filter(subdomain_url=url).exists()

    def _suffixed_subdomain(self, subdomain):
        suffixes = random.sample(SubDomainBuilder.COMPANY_SUFFIXES, len(SubDomainBuilder.COMPANY_SUFFIXES))
        for suffix in suffixes:
            subdomain_with_suffix = "{0}-{1}".format(subdomain, suffix)
            url = self._build_full_url(subdomain_with_suffix)
            exists = self._subdomain_exists(url)
            if not exists:
                return url
        return None

    def _numbered_subdomain(self, subdomain):
        count = 1
        while True:
            subdomain_with_suffix = "{0}-{1}".format(subdomain, count)
            url = self._build_full_url(subdomain_with_suffix)
            if not self._subdomain_exists(url):
                return url
            count += 1
