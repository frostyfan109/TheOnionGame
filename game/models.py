from django.db import models
from common.util import toPercentString

class Article(models.Model):
    THRESHOLD_GUESSES = 50
    THRESHOLD_PERCENT = .8

    title = models.TextField(
        help_text = "Title of the article"
    )
    real = models.BooleanField(
        help_text = "Whether or not the article is real (not from The Onion) or fake (from The Onion)"
    )
    url = models.URLField(
        default = "",
        help_text = "URL of the article (may be left empty to signify that it lacks one)"
    )
    correctlyGuessed = models.PositiveIntegerField(default = 0)
    incorrectlyGuessed = models.PositiveIntegerField(default = 0)

    def guess(self,guess):
        value = guess == self.real

        if value:
            self.correctlyGuessed += 1
        else:
            self.incorrectlyGuessed += 1

        deleted = False
        total = self.correctlyGuessed + self.incorrectlyGuessed
        if total >= Article.THRESHOLD_GUESSES and self.getPercentIncorrect >= Article.THRESHOLD_PERCENT:
            print("Deleting entry: "+self)
            self.delete()
            deleted = True

        return (value,deleted)

    def getPercentIncorrect(self):
        if self.correctlyGuessed + self.incorrectlyGuessed == 0:
            #division by zero error
            return 0
        else:
            return self.correctlyGuessed / (self.correctlyGuessed + self.incorrectlyGuessed)


    def __str__(self):
        return "("+toPercentString(self.getPercentIncorrect())+") "+self.title


# "EPA Head Says He Needs to Fly First Class Because People Are Mean to Him in Coach":{"real":"true","likes":0,"correct":0,"incorrect":0}
