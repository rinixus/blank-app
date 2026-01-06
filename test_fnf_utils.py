
import unittest
from fnf_utils import generate_fnf_json

class TestFnFUtils(unittest.TestCase):
    def test_generate_fnf_json(self):
        song_name = "Test Song"
        bpm = 120
        speed = 2.0
        p1 = "bf"
        p2 = "dad"
        gf = "gf"

        # 1 section, 1 note at start for opponent left (0), 1 note at step 4 for player right (7)
        section1_grid = [[0]*8 for _ in range(16)]
        section1_grid[0][0] = 1 # Opponent Left at step 0
        section1_grid[4][7] = 1 # Player Right at step 4

        sections = [
            {
                "mustHitSection": True,
                "grid": section1_grid
            }
        ]

        result = generate_fnf_json(song_name, bpm, speed, p1, p2, gf, sections)

        # Verify structure
        self.assertIn("song", result)
        self.assertEqual(result["song"]["song"], song_name)
        self.assertEqual(result["song"]["bpm"], bpm)
        self.assertEqual(len(result["song"]["notes"]), 1)

        section = result["song"]["notes"][0]
        self.assertTrue(section["mustHitSection"])
        self.assertEqual(len(section["sectionNotes"]), 2)

        # Verify timings
        # BPM 120 -> 500ms per beat -> 125ms per step
        step_ms = 125.0

        # Note 1: Step 0 -> 0ms
        n1 = section["sectionNotes"][0]
        self.assertAlmostEqual(n1[0], 0.0)
        self.assertEqual(n1[1], 0) # Col 0

        # Note 2: Step 4 -> 4 * 125 = 500ms
        n2 = section["sectionNotes"][1]
        self.assertAlmostEqual(n2[0], 500.0)
        self.assertEqual(n2[1], 7) # Col 7

if __name__ == "__main__":
    unittest.main()
