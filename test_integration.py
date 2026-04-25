import unittest
from unittest.mock import MagicMock, patch
import os
import shutil
import database
import generator
import time

class TestMixMovie(unittest.TestCase):

    def setUp(self):
        # Use a test database
        database.DB_FILE = "test_mixmovie.db"
        database.init_db()

        # Ensure generated dir exists
        if not os.path.exists("generated_movies"):
            os.makedirs("generated_movies")

        # Ensure sample video exists (mock it if not downloaded)
        if not os.path.exists("sample_video.mp4"):
            with open("sample_video.mp4", "w") as f:
                f.write("mock")

    def tearDown(self):
        # Cleanup
        if os.path.exists("test_mixmovie.db"):
            os.remove("test_mixmovie.db")

    def test_add_and_retrieve_user(self):
        database.add_user("test@example.com", "Test User")
        import sqlite3
        conn = sqlite3.connect("test_mixmovie.db")
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE email=?", ("test@example.com",))
        result = c.fetchone()
        conn.close()
        self.assertEqual(result[0], "Test User")

    @patch('generator.st')
    def test_generate_and_privacy(self, mock_st):
        # Setup mocks for streamlit
        mock_bar = MagicMock()
        mock_st.progress.return_value = mock_bar

        # 1. Add User
        database.add_user("test@example.com", "Test User")

        # 2. Generate Movie
        # We patch generator.st to avoid actual UI calls
        path = generator.generate_movie("test@example.com", "My Movie", "Sci-Fi", "Noir", "2050")

        self.assertTrue(os.path.exists(path))

        # 3. Check it is private by default
        user_movies = database.get_user_movies("test@example.com")
        self.assertEqual(len(user_movies), 1)
        self.assertEqual(user_movies.iloc[0]['is_public'], 0)

        movie_id = int(user_movies.iloc[0]['id'])

        # 4. Toggle to Public
        database.toggle_visibility(movie_id, False) # Current is False (0)

        # 5. Check Public Gallery
        public_movies = database.get_public_movies()
        self.assertEqual(len(public_movies), 1)
        self.assertEqual(public_movies.iloc[0]['title'], "My Movie")


    def test_icaros_guide_content(self):
        guide = generator.build_icaros_flowey_guide(hero_name="Frisk")
        self.assertIn("Ícaros", guide)
        self.assertIn("Flowey", guide)
        self.assertIn("Frisk", guide)

if __name__ == '__main__':
    unittest.main()
