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
            jsony = response.get_json()
            game_id = jsony['gameId']

            self.assertEqual(response.status_code, 200)
            self.assertIn('gameId', jsony)
            self.assertTrue(games[game_id])
            # write a test for this route
            # Test that:
            # the route returns JSON with a string game id, and a list-of-lists for the board
            # the route stores the new game in the games dictionary

    def test_api_score_word(self):
        with self.client as client:
            response = client.get('/api/new-game')
            jsony = response.get_json()
            game_id = jsony['gameId']
            board = [
                ["C", "A", "T", "B", "B"],
                ["C", "A", "F", "B", "B"],
                ["C", "A", "P", "B", "B"],
                ["B", "A", "T", "B", "B"],
                ["R", "A", "T", "B", "B"]
            ]
            games[game_id].board = board
            game = games[game_id]
            post_req = client.post('/api/score-word',
                                   json={"gameId": game_id,
                                         "word": "CAT"})

            self.assertEqual(post_req.status_code, 200)
            self.assertEqual(post_req.get_json(), {"result": "ok"})
            self.assertTrue(games[game_id])
            self.assertTrue(game.is_word_in_word_list("CAT"))
            self.assertTrue(game.check_word_on_board("CAT"))
            self.assertFalse(game.is_word_in_word_list("cat"))
            self.assertFalse(game.is_word_in_word_list("CATIPUS"))
            self.assertFalse(game.check_word_on_board("HELLO"))
