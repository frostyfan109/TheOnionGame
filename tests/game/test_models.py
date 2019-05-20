""" Model unit tests """
from game.models import *

import pytest



@pytest.mark.django_db
def test_article():
    article = Article(title="EPA Head Says He Needs to Fly First Class Because People Are Mean to Him in Coach",real=True,url="http://google.com")
    article.guess(True)
    article.save()
    assert article.title == "EPA Head Says He Needs to Fly First Class Because People Are Mean to Him in Coach"
    assert article.real == True
    assert article.url == "http://google.com"
    assert article.correctlyGuessed == 1
    assert article.incorrectlyGuessed == 0
