from unittest import TestCase
from app import app, games
import json

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<button class="word-input-btn">Go</button>', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.get('/api/new-game')
            jsony = response.get_data(as_text=True)
            obj = json.loads(jsony)
            game_id = obj['gameId']

            self.assertEqual(response.status_code, 200)
            self.assertIn('gameId', jsony)
            self.assertTrue(games[game_id])
            # write a test for this route
            # Test that:
            # the route returns JSON with a string game id, and a list-of-lists for the board
            # the route stores the new game in the games dictionary
