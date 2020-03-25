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

    def build_sub_domain_url(self, organization, team):
        sub_domain = slugify("{0}-{1}".format(organization, team))
        url = self._build_full_url(sub_domain)
        exists = self._sub_domain_exists(url)
        if exists:
            url = self._random_sub_domain(sub_domain)
        return url

    def _random_sub_domain(self, sub_domain):
        url = self._suffixed_sub_domain(sub_domain)
        if not url:
            url = self._numbered_sub_domain(sub_domain)
        return url

    def _build_full_url(self, sub_domain):
        return "{0}{1}.{2}".format(settings.BASE_PROTOCOL, sub_domain, settings.BASE_DOMAIN_URL)

    def _sub_domain_exists(self, url):
        return Team.objects.filter(sub_domain_url=url).exists()

    def _suffixed_sub_domain(self, sub_domain):
        suffixes = random.sample(SubDomainBuilder.COMPANY_SUFFIXES, len(SubDomainBuilder.COMPANY_SUFFIXES))
        for suffix in suffixes:
            sub_domain_with_suffix = "{0}-{1}".format(sub_domain, suffix)
            url = self._build_full_url(sub_domain_with_suffix)
            exists = self._sub_domain_exists(url)
            if not exists:
                return url
        return None

    def _numbered_sub_domain(self, sub_domain):
        count = 1
        while True:
            sub_domain_with_suffix = "{0}-{1}".format(sub_domain, count)
            url = self._build_full_url(sub_domain_with_suffix)
            if not self._sub_domain_exists(url):
                return url
            count += 1
