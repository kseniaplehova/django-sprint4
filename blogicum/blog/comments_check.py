from django.shortcuts import render


def render_comment_template(request, comment, form):
    template = "blog/comment.html"
    context = {
        "comment": comment,
        "post": comment.post,
    }
    if form is not None:
        context["form"] = form
    return render(request, template, context)
