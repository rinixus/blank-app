import streamlit as st
import fnf_utils
import pandas as pd

st.set_page_config(page_title="FNF Chart Maker", layout="wide")

st.title("Friday Night Funkin' Chart Maker")
st.write("Create your own FNF song charts and export them to JSON.")

st.header("Song Metadata")

col1, col2, col3 = st.columns(3)
with col1:
    song_name = st.text_input("Song Name", "Test Song")
    bpm = st.number_input("BPM", value=120.0, step=1.0)
with col2:
    player1 = st.text_input("Player 1 (Boyfriend)", "bf")
    speed = st.number_input("Scroll Speed", value=1.0, step=0.1)
with col3:
    player2 = st.text_input("Player 2 (Opponent)", "dad")
    girlfriend = st.text_input("Girlfriend", "gf")

st.header("Chart Editor")

if 'sections' not in st.session_state:
    # Initialize with one empty section
    # Grid: 16 rows, 8 columns (Boolean)
    st.session_state.sections = [{
        "mustHitSection": True,
        "grid": [[False]*8 for _ in range(16)]
    }]

def add_section():
    st.session_state.sections.append({
        "mustHitSection": True,
        "grid": [[False]*8 for _ in range(16)]
    })

def remove_section():
    if len(st.session_state.sections) > 1:
        st.session_state.sections.pop()

c1, c2 = st.columns(2)
with c1:
    st.button("Add Section", on_click=add_section)
with c2:
    st.button("Remove Last Section", on_click=remove_section)

# Display editors for each section
# Note: Streamlit data_editor can edit session state directly if key is provided,
# but dealing with nested lists is tricky. We'll iterate and update.

# Columns for the editor
columns = ["Op_L", "Op_D", "Op_U", "Op_R", "P_L", "P_D", "P_U", "P_R"]

for i, section in enumerate(st.session_state.sections):
    st.subheader(f"Section {i+1}")

    # Toggle for mustHitSection
    section['mustHitSection'] = st.checkbox(f"Must Hit Section (Player Focus) ##{i}", value=section['mustHitSection'], key=f"mhs_{i}")

    # Data Editor
    # Convert list of lists to DataFrame for better display
    df = pd.DataFrame(section['grid'], columns=columns)

    # We want indices to be Steps (0-15)
    df.index.name = "Step"

    edited_df = st.data_editor(
        df,
        key=f"editor_{i}",
        use_container_width=True,
        column_config={
            "Op_L": st.column_config.CheckboxColumn("← (Dad)", help="Opponent Left"),
            "Op_D": st.column_config.CheckboxColumn("↓ (Dad)", help="Opponent Down"),
            "Op_U": st.column_config.CheckboxColumn("↑ (Dad)", help="Opponent Up"),
            "Op_R": st.column_config.CheckboxColumn("→ (Dad)", help="Opponent Right"),
            "P_L": st.column_config.CheckboxColumn("← (BF)", help="Player Left"),
            "P_D": st.column_config.CheckboxColumn("↓ (BF)", help="Player Down"),
            "P_U": st.column_config.CheckboxColumn("↑ (BF)", help="Player Up"),
            "P_R": st.column_config.CheckboxColumn("→ (BF)", help="Player Right"),
        }
    )

    # Update state from edited dataframe
    # We need to convert back to list of lists (booleans)
    # The data_editor returns a new dataframe with changes
    # We must ensure we capture this change in the loop

    # Wait, st.data_editor returns the edited data immediately.
    # We need to sync it back to st.session_state.sections[i]['grid']
    # But doing it inside the loop on rerun is standard Streamlit pattern.

    # Convert dataframe values to list of lists
    # Note: data_editor preserves the index, but we just need values
    # cast to bool just in case
    section['grid'] = edited_df.values.tolist()

import json

st.header("Export")

# Generate JSON
if st.button("Prepare JSON"):
    # Collect data
    # Note: st.session_state.sections is updated in place by the data editor logic above on rerun.
    # So we just pass it to the utils.

    # We might need to ensure types are correct.
    # data_editor with boolean columns returns booleans, so it fits fnf_utils expectation.

    try:
        fnf_data = fnf_utils.generate_fnf_json(
            song_name,
            bpm,
            speed,
            player1,
            player2,
            girlfriend,
            st.session_state.sections
        )

        json_str = json.dumps(fnf_data, indent=4)

        st.download_button(
            label="Download Chart JSON",
            data=json_str,
            file_name=f"{song_name.lower().replace(' ', '-')}.json",
            mime="application/json"
        )

        st.success("JSON generated! Click download above.")
        st.json(fnf_data, expanded=False)

    except Exception as e:
        st.error(f"Error generating JSON: {e}")
