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
            '-pub_date')


class DetailView(generic.DetailView):
    """View for displaying each question's detail.

    :param: Primary key of the question
    :return: Rendered template with question details
    """
    model = Question
    template_name = "polls/detail.html"
    object: Question

    def get_queryset(self):
        """Get questions that are already published.

        :return: Queryset of published questions
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Retrieve the specified question and display its details.

        :param request: The incoming request from the user.
        :param args: Additional arguments.
        :param kwargs: Keyword arguments, typically containing the question's
        primary key.
        :return: The rendered template showing the question's details.
        """
        try:
            self.object = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request,
                           f"Poll with ID {kwargs['pk']} is not found.")
            return redirect("polls:index")
        try:
            user_vote = self.object.choice_set.filter(
                vote__user=request.user).last()
        except TypeError:
            user_vote = None
        context = self.get_context_data(object=self.object,
                                        user_vote=user_vote)
        if not self.object.can_vote():
            messages.error(request,
                           f"The poll '{self.object}' "
                           f"has concluded and voting is closed.")
            return redirect("polls:index")
        return self.render_to_response(context)


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
        return redirect("login")  # Redirect to the login page if not logged in
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return redirect("polls:detail", pk=question.id)
    this_user = request.user
    """if the user has a vote for this question, update the vote for
    selected_choice save it"""
    try:
        current_vote = Vote.objects.get(user=this_user,
                                        choice__question=question)
        current_vote.choice = selected_choice
    except Vote.DoesNotExist:
        current_vote = Vote(user=this_user, choice=selected_choice)
    current_vote.save()

    # Add a success message after saving the vote
    messages.success(request, f'Your vote for '
                              f'{selected_choice.choice_text} has been saved.')
    return HttpResponseRedirect(reverse(
        'polls:results', args=(question.id,)))
