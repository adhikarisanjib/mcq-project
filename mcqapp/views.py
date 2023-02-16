from django.contrib import messages
from django.shortcuts import redirect, render

from mcqapp.forms import QuestionForm
from mcqapp.models import Questions


def get_question(id):
    try:
        question = Questions.objects.get(id=id)
    except Questions.DoesNotExist:
        question = None
    return question


def home_view(request, *args, **kwargs):
    return render(request, "mcqapp/home.html")


def list_mcq_view(request, *args, **kwargs):
    context = {}

    if request.method == "GET":
        questions = Questions.objects.all()

    if request.method == "POST":
        if "search" in request.POST:
            text = request.POST["search"]
            questions = Questions.objects.filter(question__icontains=text)

    context["questions"] = questions
    return render(request, "mcqapp/mcq_list.html", context)


def create_mcq_view(request, *args, **kwargs):
    context = {}

    form = QuestionForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        else:
            form = form
            messages.error(request, f"Error.")

    context["form"] = form
    context["action"] = "Update"

    return render(request, "mcqapp/mcq_form.html", context)


def update_mcq_view(request, id, *args, **kwargs):
    context = {}

    question = get_question(id=id)
    form = QuestionForm(request.POST or None, instance=question)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        else:
            form = form
            messages.error(request, f"Error.")

    context["form"] = form
    context["action"] = "Update"

    return render(request, "mcqapp/mcq_form.html", context)


def delete_mcq_view(request, id, *args, **kwargs):
    question = get_question(id=id)
    if request.method == "POST":
        question.delete()

    return redirect("mcqapp:home")


def take_exam_view(request, course_id, *args, **kwargs):
    context = {}
    return render(request, "mcqapp/take_exam.html", context)
