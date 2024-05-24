from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify

from blog.models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    fields = (
        "title",
        "slug",
        "image_preview",
        "actual_version_indicator",
        "number_of_views",
    )


class PostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class PostCreateView(CreateView):
    model = BlogPost
    fields = (
        "title",
        "text_area",
        "image_preview",
    )
    success_url = reverse_lazy("blog:blogpost_list")

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = BlogPost
    fields = (
        "title",
        "text_area",
        "image_preview",
    )
    success_url = reverse_lazy("blog:blogpost_list")

    def get_success_url(self):
        from django.urls import reverse

        return reverse("blog:post", args=[self.kwargs.get("pk")])


class PostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog:blogpost_list")
