from __future__ import unicode_literals

from django import forms

from .models import Project


class ProjectQuickCreateForm(forms.ModelForm):
    repository_url = forms.URLField(required=False)

    class Meta:
        model = Project
        fields = [
            "name",
            "slug",
            "description",
            "repository_url",
        ]

    def save(self):
        instance = super(ProjectQuickCreateForm, self).save()
        instance.add_repository_from_url(self.cleaned_data["repository_url"])
        return instance