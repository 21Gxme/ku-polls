import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    A model representing a question for poll.

    Attributes:
        question_text : The text of the question.
        pub_date : The date and time when the question was published.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        """
        The function checks if the publication date of an object is within the last 24 hours.
        :return: a boolean value.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """
        The function returns the question text as a string.
        :return: The `__str__` method is returning the `question_text` attribute of the object.
        """
        return self.question_text


class Choice(models.Model):
    """
    A model representing a choice for a question in poll.

    Attributes:
        question : The question to which this choice belongs.
        choice_text : The text of the choice.
        votes : The number of votes received for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        The above function returns the choice text as a string.
        :return: The `__str__` method is returning the `choice_text` attribute of the object.
        """
        return self.choice_text
