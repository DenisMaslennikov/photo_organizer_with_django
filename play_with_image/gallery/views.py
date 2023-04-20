from math import ceil
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404
from .settings import GALLERY_DEFAULT_SETTINGS
# from .image_manage import scan_dirs, bulk_image_tags
from .models import Tag, Image
from .forms import AddImageForm

# scan_dirs()
# bulk_image_tags()


def tag_view(request: HttpRequest,
             tag: str = '',
             page: int = 1) -> HttpResponse:
    if request.GET.get('page'):
        try:
            page = int(request.GET['page'])
        except ValueError:
            raise Http404

    if request.method == 'POST' and request.POST.get('per_page'):
        try:
            request.session['per_page'] = int(request.POST['per_page'])
        except ValueError:
            pass

    if request.method == 'POST' and request.POST.get('tag'):
        tags = request.POST['tag'].split(',')
        for new_tag in tags:
            select_tag = Tag.objects.get_or_create(tag=new_tag)[0]
            for key, value in request.POST.items():
                if key.isdigit() and value == 'on':
                    Image.objects.get(pk=key).tags.add(select_tag.pk)

    image_per_page: int = (request.session
                           .get('per_page',
                                GALLERY_DEFAULT_SETTINGS['image_per_page']))
    template_name: str = 'gallery/gallery.html'

    first_image: int = image_per_page * (page - 1)
    last_image: int = image_per_page * page

    if (tag == ''):
        max_page: int = ceil(Image.objects.all().count() / image_per_page)
        images = Image.objects.all()[first_image:last_image]
        title = f'Фото органайзер. Страница {page} из {max_page}'
    else:
        max_page: int = ceil(Image.objects.filter(
            tags__tag=tag).count() / image_per_page)

        images = Image.objects.filter(tags__tag=tag)[first_image:last_image]
        title = f'Просмотр тега - "{tag}". Страница {page} из {max_page}'

    if page > max_page:
        raise Http404

    tags = Tag.objects.all()

    if not images[0]:
        raise Http404

    context: dict = {
        'images': images,
        'tag': tag,
        'tags': tags,
        'max_page': max_page,
        'title': title,
        'page': page,
        'per_page': image_per_page,
        'pagination': range(1, max_page + 1),
    }
    return render(request, template_name, context)


def image_view(request: HttpRequest, image_id: int) -> HttpResponse:
    template_name = 'gallery/detail.html'
    image = get_object_or_404(Image, pk=image_id)
    title = f'Просмотр изображения {image.image_name}'
    related = Image.objects.none()
    for tag in image.tags.all():
        related = (related | tag.image_set.exclude(pk=image_id)[:8])
        if related.count() > 8:
            break
    context = {
        'image': image,
        'title': title,
        'related': related[:8],

    }
    return render(request, template_name, context)


def about(request: HttpRequest) -> HttpResponse:
    template_name: str = 'gallery/about.html'
    title: str = 'О проекте'
    context: dict = {
        'title': title,
    }
    return render(request, template_name, context)


def add_image(request: HttpRequest) -> HttpResponse:
    template_name: str = 'gallery/add_image.html'
    title: str = 'Новое изображение'
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = AddImageForm()

    context: dict = {
        'title': title,
        'form': form,
    }
    return render(request, template_name, context)
