/// scr_edu_laranja_controller()
/// Controlador principal de eventos do Edu Laranja

// Variáveis globais de estado da história
if (!variable_global_exists("edu_state")) global.edu_state = 0;
if (!variable_global_exists("edu_seen_count")) global.edu_seen_count = 0;
if (!variable_global_exists("edu_room_last_seen")) global.edu_room_last_seen = "";

/// Chame no Step de um controller object
function edu_laranja_update(_player_x, _player_y, _room_name) {
    // Aparição tipo observador: surge em área específica e some
    if (global.edu_state == 0) {
        if (_room_name == "RUINS_HALL_03" && _player_x > 220 && _player_x < 360) {
            instance_create_layer(_player_x + 120, _player_y - 30, "Instances", obj_edu_laranja);
            global.edu_seen_count += 1;
            global.edu_room_last_seen = _room_name;
            global.edu_state = 1;
        }
    }

    // Segunda aparição com fantasma e gatilho de diálogo
    if (global.edu_state == 1) {
        if (_room_name == "RUINS_CROSSROAD" && _player_y < 160) {
            var edu = instance_create_layer(320, 120, "Instances", obj_edu_laranja);
            var ghost = instance_create_layer(360, 110, "Instances", obj_edu_ghost);
            edu.target_ghost = ghost;

            scr_dialogue_start("edu_intro_submundo");
            global.edu_state = 2;
        }
    }

    // Cutscene principal
    if (global.edu_state == 2 && !scr_dialogue_is_running()) {
        scr_cutscene_start("edu_cutscene_submundo");
        global.edu_state = 3;
    }
}
