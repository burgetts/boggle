from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['DEBUG_TB_HOSTS'] ='dont-show-debug-toolbar'
class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        app.config['SECRET_KEY'] = 'secret'

    def test_homepage(self):
        """Test homepage is rendered correctly"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p> Ready to start? </p>', html)

    def test_board_rendered(self):
        """Test board is rendered"""
        with app.test_client() as client:
            resp = client.get('/play-boggle')
            html = resp.get_data(as_text=True)
            self.assertIn("""<div class="game-letter">""", html)
    

    def test_not_word_response(self):
        """Test that not-word guess is handled correnctly"""
        with app.test_client() as client:
            resp = client.get('/check-guess?guess=asdgksdlgkdg')
            self.assertEqual(resp.json['result'], 'not-word')

    def test_not_on_board_response(self):
        """Test that not-on-board guess is handled correnctly"""
        with app.test_client() as client:
            resp = client.get('/check-guess?guess=Baalitical')
            self.assertEqual(resp.json['result'], 'not-on-board')
    
    # NOT WORKING
    # def test_ok_response(self): 
    #   """Test that ok guess is handled correctly"""
    #         with app.test_client() as client:
    #             client.get('/play-boggle')
    #             with client.session_transaction() as sess:
    #                 sess['board'] = [['T','E','S','T','A'], 
    #                                 ['A','A','A','A','A'],
    #                                 ['A','A','A','A','A'],
    #                                 ['A','A','A','A','A'],
    #                                 ['A','A','A','A','A']]
    #                 session['board'] = sess['board']
    #                 sess.modified = True
    #             resp = client.get('/check-guess?guess=test')
    #             print(session['board'])
    #             self.assertEqual(resp.json['result'], 'ok')


    def test_win_stats_page(self):
        """ Test that win stats page is rendered correctly """
        with app.test_client() as client:
            resp = client.get('/stats/win')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p> Nice job! You now have the record-breaking score of', html)

    def test_lose_stats_page(self):
        """ Test that lose stats page is rendered correctly"""
        with app.test_client() as client:
            resp = client.get('/stats/lose')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p> Sorry, you did not beat the high score of', html)

            
