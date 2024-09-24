from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import (
    index, about, steps, register, login, logout_view, closed_competitions, competition_ranking, 
    get_competition_list, get_competition_ranking, get_competition_result, profile, update_profile, 
    competition_view, competition_detail_view, vote_rules, success_vote, vote
)


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, about)

    def test_steps_url_resolves(self):
        url = reverse('steps')
        self.assertEqual(resolve(url).func, steps)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_closed_competitions_url_resolves(self):
        url = reverse('closed_competitions')
        self.assertEqual(resolve(url).func, closed_competitions)

    def test_competition_ranking_url_resolves(self):
        url = reverse('competition_ranking', args=[1])
        self.assertEqual(resolve(url).func, competition_ranking)

    def test_get_competition_list_url_resolves(self):
        url = reverse('get_competition_list')
        self.assertEqual(resolve(url).func, get_competition_list)

    def test_get_competition_ranking_url_resolves(self):
        url = reverse('get_competition_ranking', args=[1])
        self.assertEqual(resolve(url).func, get_competition_ranking)

    def test_get_competition_result_url_resolves(self):
        url = reverse('get_competition_result', args=[1])
        self.assertEqual(resolve(url).func, get_competition_result)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)

    def test_update_profile_url_resolves(self):
        url = reverse('update_profile')
        self.assertEqual(resolve(url).func, update_profile)

    def test_competition_view_resolves(self):
        url = reverse('competition_view')
        self.assertEqual(resolve(url).func, competition_view)

    def test_competition_detail_view_resolves(self):
        url = reverse('competition_detail', args=[1])
        self.assertEqual(resolve(url).func, competition_detail_view)

    def test_vote_resolves(self):
        url = reverse('cast_vote', args=[1, 1])
        self.assertEqual(resolve(url).func, vote)

    def test_vote_rules_resolves(self):
        url = reverse('vote')
        self.assertEqual(resolve(url).func, vote_rules)

    def test_success_vote_resolves(self):
        url = reverse('success_vote')
        self.assertEqual(resolve(url).func, success_vote)
