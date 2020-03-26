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
        exists = self._subdomain_exists(subdomain)
        if exists:
            subdomain = self._random_subdomain(subdomain)
        return subdomain

    def _random_subdomain(self, subdomain):
        suffixed_subdomain = self._suffixed_subdomain(subdomain)
        if not suffixed_subdomain:
            suffixed_subdomain = self._numbered_subdomain(subdomain)
        return suffixed_subdomain

    def _subdomain_exists(self, url):
        return Team.objects.filter(subdomain=url).exists()

    def _suffixed_subdomain(self, subdomain):
        suffixes = random.sample(SubDomainBuilder.COMPANY_SUFFIXES, len(SubDomainBuilder.COMPANY_SUFFIXES))
        for suffix in suffixes:
            subdomain_with_suffix = "{0}-{1}".format(subdomain, suffix)
            exists = self._subdomain_exists(subdomain_with_suffix)
            if not exists:
                return subdomain_with_suffix
        return None

    def _numbered_subdomain(self, subdomain):
        count = 1
        while True:
            subdomain_with_suffix = "{0}-{1}".format(subdomain, count)
            if not self._subdomain_exists(subdomain_with_suffix):
                return subdomain_with_suffix
            count += 1
