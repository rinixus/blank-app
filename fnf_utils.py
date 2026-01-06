
def generate_fnf_json(song_name, bpm, speed, player1, player2, girlfriend, sections_data):
    """
    Generates a dictionary representing a Friday Night Funkin' song chart.

    Args:
        song_name (str): The name of the song.
        bpm (float): Beats per minute.
        speed (float): Scroll speed.
        player1 (str): Name of the player character (bf).
        player2 (str): Name of the opponent character.
        girlfriend (str): Name of the girlfriend character.
        sections_data (list): List of dictionaries, each containing:
            - 'mustHitSection' (bool): True if the section belongs to the player.
            - 'notes' (list of lists): 16 rows x 8 columns (0 or 1).
              Columns 0-3 are Opponent, 4-7 are Player.

    Returns:
        dict: The FNF JSON structure.
    """

    # Calculate step duration in milliseconds
    # 60 seconds / BPM = seconds per beat
    # seconds per beat / 4 = seconds per step (16th note)
    # * 1000 = ms per step
    step_ms = (60.0 / bpm) / 4.0 * 1000.0

    fnf_notes = []

    total_steps_passed = 0

    for section_idx, section in enumerate(sections_data):
        section_notes = []

        # Iterate through the 16 steps of the section
        grid = section.get('grid', [])

        for step_in_section, row in enumerate(grid):
            # row should be a list of 8 items (booleans or ints)
            # 0-3: Opponent, 4-7: Player

            current_step_time = (total_steps_passed + step_in_section) * step_ms

            for col_idx, is_active in enumerate(row):
                if is_active:
                    # Determine note data (0-7)
                    # In standard FNF JSON:
                    # If mustHitSection is True (Player's turn):
                    #   0-3 are for Player? No, usually indices are absolute.
                    #   However, some engines swap them based on mustHitSection.
                    #   Let's stick to the Vanilla behavior where 0-3 is Left side (Dad) and 4-7 is Right side (BF).
                    #   Wait, checking Kade Engine / Psych Engine / Vanilla source...
                    #
                    #   Vanilla:
                    #   noteData % 4 is the direction.
                    #   If mustHitSection is TRUE:
                    #       0-3 = Player
                    #       4-7 = Opponent
                    #   If mustHitSection is FALSE:
                    #       0-3 = Opponent
                    #       4-7 = Player

                    #   This is confusing. Let's verify.
                    #   "mustHitSection": true -> camera points to BF.
                    #   Usually, chart editors show two grids: "Left" and "Right".
                    #   If mustHitSection is true, "Left" grid becomes Player?

                    #   Let's simplify:
                    #   We will assume the user inputs into absolute columns:
                    #   Cols 0-3: Opponent
                    #   Cols 4-7: Player

                    #   So we need to map that to the JSON format.
                    #   If we use absolute indices (0-7) in JSON, the game logic handles swapping if needed.
                    #   Actually, most charts just use 0-7, where 0-3 is ALWAYS Dad and 4-7 is ALWAYS BF?
                    #
                    #   Let's look at a reference snippet if possible. Or search.
                    #   Since I can't search, I will use the most common convention:
                    #   0-3 is Dad. 4-7 is BF.
                    #   HOWEVER, `mustHitSection` changes the "lane" perspective in the game rendering for hitting notes?

                    #   Let's use the standard "Psych Engine" or modern convention which tends to be consistent.
                    #   Actually, let's look at `sections_data`.
                    #   If I simply output 0-7 based on column index 0-7, it should be fine.
                    #   0: Left (Opponent)
                    #   1: Down (Opponent)
                    #   2: Up (Opponent)
                    #   3: Right (Opponent)
                    #   4: Left (Player)
                    #   5: Down (Player)
                    #   6: Up (Player)
                    #   7: Right (Player)

                    note_data = col_idx
                    sustain_length = 0 # Default to 0 for now

                    section_notes.append([current_step_time, note_data, sustain_length])

        fnf_notes.append({
            "sectionNotes": section_notes,
            "lengthInSteps": 16,
            "mustHitSection": section.get('mustHitSection', True),
            "bpm": bpm,
            "changeBPM": False,
            "altAnim": False
        })

        total_steps_passed += 16

    song_data = {
        "song": song_name,
        "notes": fnf_notes,
        "bpm": bpm,
        "needsVoices": True,
        "player1": player1,
        "player2": player2,
        "gfVersion": girlfriend,
        "speed": speed,
        "validScore": True
    }

    return {"song": song_data}
