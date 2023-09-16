import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days_offset, days_end=None):
    """
    The function creates a question object with a specified question text
    and publication date, and optionally an end date.

    :param question_text
    :param days_offset
    :param days_end
    :return: The function `create_question` returns a `Question` object.
    """
    publish_date = timezone.now() + datetime.timedelta(days=days_offset)
    if days_end is not None:
        end_date = timezone.now() + datetime.timedelta(days=days_end)
        return Question.objects.create(question_text=question_text,
                                       pub_date=publish_date,
                                       end_date=end_date)
    return Question.objects.create(question_text=question_text,
                                   pub_date=publish_date)


class QuestionModelTests(TestCase):
    def test_future_question(self):
        """
        The function tests if a future question was published recently.
        """
        publish_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=publish_date)
        self.assertIs(future_question.was_published_recently(), False)

    def test_old_question(self):
        """
        The function tests if a question was published recently by checking
        its publishing date.
        """
        publish_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=publish_date)
        self.assertIs(old_question.was_published_recently(), False)

    def test_recent_question(self):
        """
        The function tests if a question was published recently.
        """
        publish_date = timezone.now() - datetime.timedelta(hours=23,
                                                           minutes=59,
                                                           seconds=59)
        recent_question = Question(pub_date=publish_date)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_published_question(self):
        """
        The function tests whether a question is published or not.
        """
        question = create_question("", -4)
        self.assertIs(question.is_published(), True)

    def test_unpublished_question(self):
        """
        The function tests whether an unpublished question is correctly
        identified as not published.
        """
        question = create_question("", 4)
        self.assertIs(question.is_published(), False)

    def test_can_vote_on_voting_period(self):
        """
        The function tests whether a question can be voted on during
        a voting period.
        """
        question_with_end_date = create_question("", 0, 10)
        self.assertIs(question_with_end_date.can_vote(), True)

        question_without_end_date = create_question("", 0)
        self.assertIs(question_without_end_date.can_vote(), True)

    def test_can_not_vote_after_end_date(self):
        """
        The function tests whether a question can be voted on after its
        end date has passed.
        """
        question = create_question("", -10, -1)
        self.assertIs(question.can_vote(), False)

    def test_can_not_vote_on_unpublished_poll(self):
        """
        The function tests whether a question can be voted on if
        it is unpublished.
        """
        question = create_question("", 2)
        self.assertIs(question.can_vote(), False)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        The function tests if there are no questions available in the polls
        and verifies that the response status code is 200, the response
        contains the message "No polls are available", and the
        latest_question_list is empty.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertIs(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        The function tests if a past question is displayed in the latest
        question list.
        """
        question = create_question(question_text="Past question",
                                   days_offset=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],
                                 [question])

    def test_future_question(self):
        """
        The function tests if a future question is displayed correctly on
        the index page.
        """
        create_question(question_text="Future question.", days_offset=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        The function tests that only past questions are displayed on the
        index page.
        """
        past_question = create_question(question_text="Past question.",
                                        days_offset=-30)
        create_question(question_text="Future question.", days_offset=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [past_question])

    def test_two_past_questions(self):
        """
        The function tests if the latest question list is displayed correctly
        in reverse chronological order.
        """
        question1 = create_question(question_text="Past question 1.",
                                    days_offset=-30)
        question2 = create_question(question_text="Past question 2.",
                                    days_offset=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 [question2, question1])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The function tests if a future question redirects to the detail page.
        """
        future_question = create_question(question_text='Future question.',
                                          days_offset=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The function tests if a past question is displayed correctly on the
        detail page.
        """
        past_question = create_question(question_text='Past Question.',
                                        days_offset=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_results_view_for_past_question(self):
        """
        The function tests the view for displaying the results of a past
        question.
        """
        past_question = create_question("Past Question", days_offset=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_results_view_for_future_question(self):
        """
        The function tests the view for displaying the results of a future
        question.
        """
        future_question = create_question("Future Question", days_offset=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')
