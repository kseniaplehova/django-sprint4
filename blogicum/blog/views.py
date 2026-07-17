from blog.comments_check import render_comment_template
from blog.forms import CommentForm, PostForm, ProfileForm, RegisterForm
from blog.mixins import PostCheckMixin, PostMixin
from blog.models import Category, Comment, Post
from blog.utils import get_posts_for_user, get_published_posts_queryset
from core.constants import PAGINATE_COUNT
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect("blog:post_detail", post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if request.user != comment.author:
        raise Http404("Нет прав доступа к этому комментарию!")

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)

    return render_comment_template(request, comment, form)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if request.user != comment.author:
        raise Http404("Нет прав доступа к этому комментарию!")

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)

    return render_comment_template(request, comment, None)


class RegistrationView(FormView):
    template_name = "registration/registration_form.html"
    form_class = RegisterForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileView(ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = PAGINATE_COUNT
    context_object_name = "page_obj"

    def get_queryset(self):
        self.profile_user = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        return get_posts_for_user(self.request.user).filter(
            author=self.profile_user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.profile_user
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "blog/user.html"
    form_class = ProfileForm
    success_url = reverse_lazy("blog:index")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    template_name = "blog/create.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostUpdateView(
    LoginRequiredMixin, PostMixin, PostCheckMixin, UpdateView
):
    template_name = "blog/create.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            "blog:post_detail",
            kwargs={"post_id": self.kwargs[self.pk_url_kwarg]},
        )


class PostDeleteView(
    LoginRequiredMixin, PostMixin, PostCheckMixin, DeleteView
):
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse("blog:index")


class PublishedPostsView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = PAGINATE_COUNT

    def get_queryset(self):
        return get_published_posts_queryset()


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        post_id = self.kwargs.get(self.pk_url_kwarg)
        post = get_object_or_404(Post, pk=post_id)

        if (
            self.request.user.is_authenticated
            and self.request.user == post.author
        ):
            return post

        if (
            post.is_published
            and post.category.is_published
            and post.pub_date <= timezone.now()
        ):
            return post

        raise Http404("Пост недоступен.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.object.author
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related(
            "author"
        ).order_by("created_at")
        return context


class CategoryDetailView(ListView):
    model = Post
    template_name = "blog/category.html"
    paginate_by = PAGINATE_COUNT
    context_object_name = "page_obj"

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs["slug"], is_published=True
        )
        return get_published_posts_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
