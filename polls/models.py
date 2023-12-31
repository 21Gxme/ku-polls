import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """
    A model representing a question for poll.

    Attributes:
        question_text: The text of the question.
        pub_date: The date and time when the question was published.
        end_date: The date and time when the question was ended.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', null=True, blank=True,
                                    default=None)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def is_published(self):
        """
        The function checks if the publication date of an object is in
        the past.
        :return: a boolean value.
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """
        The function checks if a voting event is currently open for voting.
        :return: a boolean value.
        """
        if self.end_date is None:
            return self.is_published()
        else:
            return self.is_published() and self.end_date >= timezone.now()

    def was_published_recently(self):
        """
        The function checks if the publication date of an object is within the
        last 24 hours.
        :return: a boolean value.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """
        The function returns the question text as a string.
        :return: return the `question_text` attribute of the object.
        """
        return self.question_text


class Choice(models.Model):
    """
    A model representing a choice for a question in poll.

    Attributes:
        question: The question to which this choice belongs.
        choice_text: The text of the choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """
        The function returns the number of votes for a choice.
        :return: an integer value.
        """
        return self.vote_set.count()

    def __str__(self):
        """
        The above function returns the choice text as a string.
        :return: return the `choice_text` attribute of the object.
        """
        return self.choice_text

    def get_vote_count(self):
        """
        The function returns the number of votes for a choice.
        :return: an integer value.
        """
        return self.votes


class Vote(models.Model):
    """
    Record a vote for a choice in a particular question.
    """
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
