from typing import Any, Dict

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView

from .settings import GALLERY_DEFAULT_SETTINGS
from image.models import Image
from tag_anything.models import Tag
from .forms import AddImageForm, AddTags


class ImageListView(ListView):
    model = Image
    template_name = 'gallery/gallery.html'
    context_object_name = 'images'
    paginate_by = GALLERY_DEFAULT_SETTINGS['image_per_page']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if tag := self.kwargs.get('tag_str'):
            context['title'] = f'Просмотр тега - "{tag}"'
        else:
            context['title'] = 'Фото органайзер'

        tag_form = AddTags(self.request.GET)
        if (tag_form.is_valid()):
            select_tag = Tag.objects.get_or_create(**tag_form.cleaned_data)[0]
            for key, value in self.request.GET.items():
                if key.isdigit() and value == 'on':
                    Image.objects.get(pk=key).tags.add(select_tag.pk)

        context['image_per_page'] = self.request.session.get(
            'image_per_page',
            GALLERY_DEFAULT_SETTINGS['image_per_page'])

        context['tag_form'] = tag_form

        return context

    def get_paginate_by(self, queryset) -> int:
        if self.request.GET.get('image_per_page'):
            try:
                self.request.session['image_per_page'] = (
                    int(self.request.GET['image_per_page'])
                )
            except ValueError:
                pass

        return self.request.session.get(
            'image_per_page',
            GALLERY_DEFAULT_SETTINGS['image_per_page']
        )

    def get_queryset(self):
        if tag := self.kwargs.get('tag_str'):
            images = Image.objects.prefetch_related(
                'tags',
                'tags__category'
            ).filter(tags__tag=tag)

        else:
            images = Image.objects.prefetch_related(
                'tags',
                'tags__category'
            ).all()
        return images


class ImageView(DetailView):
    model = Image
    template_name = 'gallery/detail.html'
    pk_url_kwarg = 'image_id'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        related = Image.objects.none()
        for tag in context['image'].tags.all():
            related = (
                related | tag.images.prefetch_related('tags').exclude(
                    pk=context['image'].pk
                )[:GALLERY_DEFAULT_SETTINGS['related_images']])
            if related.count() >= GALLERY_DEFAULT_SETTINGS['related_images']:
                break
        context['related'] = (
            related[:GALLERY_DEFAULT_SETTINGS['related_images']]
        )
        return context

    def get_object(self):
        return get_object_or_404(
            Image.objects.prefetch_related('tags').all(),
            pk=self.kwargs['image_id']
        )


def about(request: HttpRequest) -> HttpResponse:
    template_name: str = 'gallery/about.html'
    title: str = 'О проекте'
    context: dict = {
        'title': title,
    }
    return render(request, template_name, context)


class AddImage(CreateView):
    model = Image
    template_name = 'gallery/add_image.html'
    form_class = AddImageForm

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новое изображение'
        return context
