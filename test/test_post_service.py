import unittest

from service import PostRepository
from service.post_service import PostService


class TestPostService(unittest.TestCase):
    def test_(self):
        svc = PostService(repository=dummyRepository, mailer=DumymMailer())
