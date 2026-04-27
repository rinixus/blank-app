/// scr_cutscene_start("edu_cutscene_submundo")

function scr_cutscene_start(_id) {
    if (_id == "edu_cutscene_submundo") {
        // Pausa controle do jogador
        global.player_locked = true;

        // Exemplo de sequência
        scr_cutscene_queue_camera(300, 140, 70);
        scr_cutscene_queue_wait(20);
        scr_cutscene_queue_dialogue("edu_cutscene_line_1");
        scr_cutscene_queue_spawn("obj_toriel", 260, 140);
        scr_cutscene_queue_spawn("obj_sans", 340, 140);
        scr_cutscene_queue_dialogue("edu_cutscene_line_2");
        scr_cutscene_queue_dialogue("edu_white_man_hint");
        scr_cutscene_queue_wait(30);
        scr_cutscene_queue_despawn("obj_edu_laranja");
        scr_cutscene_queue_despawn("obj_edu_ghost");
        scr_cutscene_queue_callback(function() {
            global.player_locked = false;
        });
    }
}
