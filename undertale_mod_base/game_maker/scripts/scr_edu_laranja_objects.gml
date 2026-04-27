/// Objetos exemplo para GameMaker

// obj_edu_laranja - Create Event
image_speed = 0;
alpha_target = 1;
vanish_timer = room_speed; // 1 segundo
floating_phase = irandom(360);
target_ghost = noone;

// obj_edu_laranja - Step Event
floating_phase += 4;
y += lengthdir_y(0.35, floating_phase);

if (vanish_timer > 0) {
    vanish_timer -= 1;
} else {
    alpha_target = 0;
}

image_alpha = lerp(image_alpha, alpha_target, 0.12);

if (image_alpha < 0.05) {
    instance_destroy();
}

// obj_edu_ghost - Create Event
image_speed = 0.15;
image_alpha = 0.9;
hover_phase = irandom(360);

// obj_edu_ghost - Step Event
hover_phase += 6;
y += lengthdir_y(0.5, hover_phase);
