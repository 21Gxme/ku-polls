from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Question, Choice, Vote
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set
        to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    The DetailView class is a generic class-based view that displays a single
    object.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        The function checks if a question can be voted on and redirects
        accordingly, displaying an error message if necessary.

        :param request: The `request` parameter represents the HTTP request.
        :return: The code is returning a rendered template with the "question"
        variable passed as context.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exist.")
            return redirect("polls:index")

        if question.can_vote():
            return render(request, self.template_name, {"question": question})
        else:
            messages.error(request, f"That poll is not available to vote.")

            return redirect("polls:index")


class ResultsView(generic.DetailView):
    """
    The ResultsView class is a generic detail view in Python.
    """
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """
        The `get` function retrieves a question object based on its
        primary key, checks if it is a future question, and displays
        an error message if it is not available for voting.

        :param request: The `request` parameter represents the HTTP request.
        :return: The code is returning a rendered HTML template with the
        question and a boolean value.
        """
        question = get_object_or_404(Question, pk=kwargs["pk"])
        is_future_question = not question.can_vote()
        if is_future_question:
            messages.error(request, f"That poll is not available to vote.")
        return render(request, self.template_name, {"question": question,
                                                    "is_future_question":
                                                        is_future_question})


@login_required
def vote(request, question_id):
    """
    The function allows users to vote on a specific question and updates the
    vote count for the selected choice.

    :param request: The request object represents the HTTP request.
    :param question_id: The `question_id` parameter is the unique identifier.
    :return: an HTTP redirect response to the 'polls:results'.
    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        # user must be logged in to vote
        return redirect("login")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    this_user = request.user
    # selected_choice.votes += 1
    # selected_choice.save()
    """if the user has a vote for this question, update the vote for selected_choice save it"""
    try:
        # find the vote for this user and question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # create a new vote object
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()
    # TODO: Use message to display a confirmation on the results page

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
