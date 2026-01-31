# Maskaria: Guardianes Nasa - Metroidvania ligero: máscaras de animales, Nasa Yuwe

import pygame
import sys
import os

from config import (
    TITLE, SCREEN_W, SCREEN_H, FPS, TILE_SIZE, INITIAL_LIVES,
    START_ROOM_ID, ZONES, CAMERA_SMOOTH, CAMERA_DEADZONE_LEFT, CAMERA_DEADZONE_RIGHT,
    ZONE_SPLASH_DURATION,
)
from player import Player
from levels_data import get_room, get_start_room_id, LEVEL_ORDER, FINAL_ROOM_ID
from world import build_world_from_grid, MaskPickup
from ui import (
    draw_hud, draw_title_screen, draw_game_over,
    draw_main_menu, draw_pause_menu, draw_credits, draw_options,
    draw_level_select,
    draw_zone_splash, draw_parallax_bg,
    draw_story_screen, draw_victory_screen, draw_speech_bubble_character,
    draw_glossary_screen, draw_world_labels,
    STORY_SCREENS, LEVEL_NARRATIVES, LEVEL_INTRO_MESSAGES, MASK_PICKUP_MESSAGES,
)
from masks import get_mask_name, get_mask_color, get_all_mask_ids, can_swim, MASK_SECRETS, MASK_SWIM, MASK_FINAL
from audio import (
    init_audio, play_mask_pickup, play_jump, play_door_open, play_music, play_stomp,
    play_coin, play_hurt, play_level_complete, play_word_sound,
    stop_ambient, play_ambient_story, play_ambient_game,
)
from effects import ScreenShake, ParticleManager
from savegame import load as load_save, save_state, add_coins, set_lives, get_lives, get_coins, get_glossary_unlocked, add_glossary_word, add_word_collected
from glossary import get_words_for_zone
try:
    from tts import speak as tts_speak, stop as tts_stop
except Exception:
    def tts_speak(_):
        pass
    def tts_stop():
        pass

STATE_TITLE = "title"
STATE_STORY = "story"
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
STATE_OPTIONS = "options"
STATE_CREDITS = "credits"
STATE_LEVEL_SELECT = "level_select"


def _try_hurt_player(lives, player, start_x, start_y, shake, particles):
    """Devuelve lives (reducidas si no tenía escudo). Si tenía escudo, lo consume y no pierde vida."""
    if player.can_shield():
        player.use_shield()
        shake.trigger(12, 4)
        particles.emit_hurt(player.rect.centerx, player.rect.top)
        return lives
    lives -= 1
    set_lives(lives)
    play_hurt()
    player.rect.x = start_x
    player.rect.y = start_y
    player.vel_x = player.vel_y = 0
    player.invincible_frames = 90
    shake.trigger(20, 8)
    particles.emit_hurt(player.rect.centerx, player.rect.top)
    return lives


def _get_bg_for_zone(zone_id):
    for z in ZONES:
        if z["id"] == zone_id:
            return z["bg"]
    return ((60, 70, 100), (80, 80, 120))


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    init_audio()
    try:
        play_music()
    except Exception:
        pass

    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 28)
    shake = ScreenShake()
    particles = ParticleManager()

    data = load_save()
    state = STATE_TITLE
    menu_selected = 0
    pause_selected = 0
    level_select_selected = 0
    level_select_start = None  # (room_id, start_x, start_y) cuando se elige un nivel concreto
    current_room_id = data.get("room_id", get_start_room_id())
    lives = data.get("lives", INITIAL_LIVES)
    coins = data.get("coins", 0)
    collected_masks = set(data.get("collected_masks", []))
    current_mask = data.get("current_mask")
    player = None
    world_data = None
    start_x = data.get("player_x", 64)
    start_y = data.get("player_y", 12 * TILE_SIZE)
    room_name_str = ""
    zone_name = ""
    world_width = SCREEN_W
    camera_x = 0.0
    zone_splash_timer = 0
    zone_splash_name = ""
    last_room_id = None
    last_zone = ""
    tutorial_timer = 0
    bosque_hint_timer = 0
    agua_hint_timer = 0
    santuario_hint_timer = 0
    level_narrative_timer = 0
    level_narrative_text = ""
    npc_message_timer = 0
    npc_message_text = ""
    mask_pickup_message_timer = 0
    mask_pickup_message_es = ""
    mask_pickup_message_nasa = ""
    word_pickup_message_timer = 0
    word_pickup_message_es = ""
    word_pickup_message_nasa = ""
    restart_room = False
    retry_from_game_over = False
    pause_glossary_open = False
    story_screen_index = 0
    story_play_rect = None
    story_pause_rect = None
    story_text_to_speak = ""
    bubble_play_rect = None
    bubble_pause_rect = None
    bubble_text_to_speak = ""
    victory_masks = 0
    victory_coins = 0
    victory_lives = 0
    last_state = None

    while True:
        # Ambient procedural: historia (tipo Silksong relajante) y juego (sutil)
        if state == STATE_STORY and last_state != STATE_STORY:
            try:
                stop_ambient()
                play_ambient_story()
            except Exception:
                pass
        elif state == STATE_PLAYING and last_state != STATE_PLAYING:
            try:
                stop_ambient()
                play_ambient_game()
            except Exception:
                pass
        elif state not in (STATE_STORY, STATE_PLAYING) and last_state in (STATE_STORY, STATE_PLAYING):
            try:
                stop_ambient()
            except Exception:
                pass
        last_state = state

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING
                    elif state in (STATE_GAME_OVER,):
                        if get_lives() <= 0:
                            set_lives(INITIAL_LIVES)
                        state = STATE_MENU
                        data = load_save()
                    elif state in (STATE_OPTIONS, STATE_CREDITS, STATE_LEVEL_SELECT):
                        state = STATE_MENU
                elif state == STATE_TITLE and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    state = STATE_STORY
                    story_screen_index = 0
                elif state == STATE_STORY and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    story_screen_index += 1
                    if story_screen_index >= len(STORY_SCREENS):
                        state = STATE_MENU
                        menu_selected = 0
                elif state == STATE_STORY and event.key == pygame.K_v and story_text_to_speak:
                    tts_speak(story_text_to_speak)
                elif state == STATE_STORY and event.key == pygame.K_b:
                    tts_stop()
                elif state == STATE_VICTORY and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    state = STATE_MENU
                    data = load_save()
                elif state == STATE_MENU:
                    if event.key == pygame.K_UP:
                        menu_selected = (menu_selected - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        menu_selected = (menu_selected + 1) % 4
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if menu_selected == 0:
                            state = STATE_LEVEL_SELECT
                            level_select_selected = 0
                        elif menu_selected == 1:
                            state = STATE_OPTIONS
                        elif menu_selected == 2:
                            state = STATE_CREDITS
                        elif menu_selected == 3:
                            pygame.quit()
                            sys.exit()
                elif state == STATE_LEVEL_SELECT:
                    num_level_options = 1 + len(LEVEL_ORDER)  # Continuar + Nivel 1..10
                    if event.key == pygame.K_UP:
                        level_select_selected = (level_select_selected - 1) % num_level_options
                    elif event.key == pygame.K_DOWN:
                        level_select_selected = (level_select_selected + 1) % num_level_options
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        data = load_save()
                        levels_visited = data.get("levels_visited", [])
                        max_level = 1
                        for r in levels_visited:
                            if r in LEVEL_ORDER:
                                max_level = max(max_level, LEVEL_ORDER.index(r) + 1)
                        unlocked = {0}
                        for n in range(1, 11):
                            if n <= max_level:
                                unlocked.add(n)
                        if level_select_selected not in unlocked:
                            pass
                        elif level_select_selected == 0:
                            state = STATE_PLAYING
                            data = load_save()
                            current_room_id = data.get("room_id", get_start_room_id())
                            start_x = data.get("player_x", 64)
                            start_y = data.get("player_y", 12 * TILE_SIZE)
                            collected_masks = set(data.get("collected_masks", []))
                            current_mask = data.get("current_mask")
                            lives = get_lives()
                            coins = get_coins()
                            player = None
                            world_data = None
                        else:
                            room_id = LEVEL_ORDER[level_select_selected - 1]
                            room = get_room(room_id)
                            if room:
                                world_tmp = build_world_from_grid(room["grid"], room)
                                level_select_start = (room_id, world_tmp["start_x"], world_tmp["start_y"])
                            state = STATE_PLAYING
                            data = load_save()
                            collected_masks = set(data.get("collected_masks", []))
                            current_mask = data.get("current_mask")
                            lives = get_lives()
                            coins = get_coins()
                            player = None
                            world_data = None
                elif state == STATE_PAUSED:
                    if pause_glossary_open:
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                            pause_glossary_open = False
                    else:
                        if event.key == pygame.K_UP:
                            pause_selected = (pause_selected - 1) % 4
                        elif event.key == pygame.K_DOWN:
                            pause_selected = (pause_selected + 1) % 4
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            if pause_selected == 0:
                                state = STATE_PLAYING
                            elif pause_selected == 1:
                                restart_room = True
                                player = None
                                world_data = None
                            elif pause_selected == 2:
                                pause_glossary_open = True
                            elif pause_selected == 3:
                                if player:
                                    save_state(current_room_id, player.rect.x, player.rect.y,
                                               player.collected_masks, player.mask_id, lives, coins)
                                state = STATE_MENU
                                player = None
                                world_data = None
                                current_room_id = None
                elif state == STATE_PLAYING and (level_narrative_timer > 0 or mask_pickup_message_timer > 0 or word_pickup_message_timer > 0):
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e, pygame.K_x, pygame.K_ESCAPE):
                        level_narrative_timer = 0
                        mask_pickup_message_timer = 0
                        word_pickup_message_timer = 0
                elif state == STATE_PLAYING and player is not None and event.key in (
                    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0
                ):
                    idx = 9 if event.key == pygame.K_0 else event.key - pygame.K_1
                    mask_list = get_all_mask_ids()
                    if 0 <= idx < len(mask_list) and mask_list[idx] in player.collected_masks:
                        player.set_mask(mask_list[idx])
                        current_mask = mask_list[idx]
                elif state == STATE_GAME_OVER and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    lives = get_lives()
                    if lives <= 0:
                        set_lives(INITIAL_LIVES)
                        state = STATE_MENU
                    else:
                        retry_from_game_over = True
                        state = STATE_PLAYING
                        player = None
                        world_data = None
                elif state == STATE_PLAYING and player:
                    if event.key in (pygame.K_UP, pygame.K_SPACE):
                        player.request_jump_buffer()
                        if player.jump():
                            play_jump()
                    elif event.key in (pygame.K_q, pygame.K_LSHIFT) and player._dash and player.dash_cooldown <= 0:
                        player.vel_x = 14 * (1 if player.facing_right else -1)
                        player.dash_cooldown = 45
                    elif event.key == pygame.K_e:
                        pass  # interact: check in update loop
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Coordenadas del clic: escalar si la ventana tiene tamaño distinto a la superficie (DPI/resize)
                pos = event.pos
                try:
                    win_w, win_h = pygame.display.get_window_size()
                    surf_w, surf_h = screen.get_size()
                    if win_w != surf_w or win_h != surf_h:
                        pos = (int(pos[0] * surf_w / max(1, win_w)), int(pos[1] * surf_h / max(1, win_h)))
                except Exception:
                    pass
                # Zona de clic más amplia (inflate) para que los botones respondan mejor
                if state == STATE_STORY:
                    if story_play_rect and story_play_rect.copy().inflate(16, 16).collidepoint(pos) and story_text_to_speak:
                        tts_speak(story_text_to_speak)
                    elif story_pause_rect and story_pause_rect.copy().inflate(16, 16).collidepoint(pos):
                        tts_stop()
                elif state == STATE_PLAYING:
                    if bubble_play_rect and bubble_play_rect.copy().inflate(12, 12).collidepoint(pos) and bubble_text_to_speak:
                        tts_speak(bubble_text_to_speak)
                    elif bubble_pause_rect and bubble_pause_rect.copy().inflate(12, 12).collidepoint(pos):
                        tts_stop()

        if state == STATE_TITLE:
            screen.fill((30, 25, 40))
            draw_title_screen(screen, font_large, font_small)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_STORY:
            story_play_rect, story_pause_rect, story_text_to_speak = draw_story_screen(screen, font_large, font_small, story_screen_index)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_VICTORY:
            draw_victory_screen(screen, font_large, font_small, victory_masks, victory_coins, victory_lives)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_MENU:
            screen.fill((30, 25, 50))
            draw_main_menu(screen, font_large, font_small, menu_selected)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_LEVEL_SELECT:
            data = load_save()
            levels_visited = data.get("levels_visited", [])
            max_level = 1
            for r in levels_visited:
                if r in LEVEL_ORDER:
                    max_level = max(max_level, LEVEL_ORDER.index(r) + 1)
            unlocked = {0}
            for n in range(1, 11):
                if n <= max_level:
                    unlocked.add(n)
            level_options = ["Continuar"] + [f"Nivel {n}" for n in range(1, 11)]
            screen.fill((28, 25, 48))
            draw_level_select(screen, font_large, font_small, level_select_selected, level_options, unlocked)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_OPTIONS:
            draw_options(screen, font_large, font_small, "Volumen: Activo. Música en assets/music (OGG/MP3).")
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_CREDITS:
            draw_credits(screen, font_large, font_small)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_PLAYING:
            if player is None or world_data is None:
                use_saved_start = True
                if level_select_start:
                    current_room_id, start_x, start_y = level_select_start[0], level_select_start[1], level_select_start[2]
                    level_select_start = None
                    use_saved_start = False
                data = load_save()
                room = get_room(current_room_id)
                if not room:
                    current_room_id = get_start_room_id()
                    room = get_room(current_room_id)
                if not room:
                    state = STATE_MENU
                    continue
                world_data = build_world_from_grid(room["grid"], room)
                if restart_room:
                    start_x = world_data["start_x"]
                    start_y = world_data["start_y"]
                    restart_room = False
                elif use_saved_start:
                    start_x = data.get("player_x", world_data["start_x"])
                    start_y = data.get("player_y", world_data["start_y"])
                zone_name = room.get("zone", "")
                name_es = room.get("zone_name", room["id"])
                name_nasa = ""
                for z in ZONES:
                    if z.get("id") == zone_name:
                        name_nasa = z.get("name_nasa_yuwe", "")
                        break
                # Nombre de zona en Nasa Yuwe primero, español entre paréntesis
                room_name_str = (name_nasa + " (" + name_es + ")").strip() if name_nasa else name_es
                world_width = len(room["grid"][0]) * TILE_SIZE
                if current_room_id != last_room_id:
                    zone_splash_timer = int(ZONE_SPLASH_DURATION * FPS)
                    zone_splash_name = room_name_str
                    if zone_name != last_zone:
                        try:
                            play_level_complete()
                        except Exception:
                            pass
                    last_zone = zone_name
                    last_room_id = current_room_id
                collected = set(data.get("collected_masks", []))
                level_narrative_timer = 1
                level_narrative_text = LEVEL_NARRATIVES.get(current_room_id, "")
                for w in get_words_for_zone(current_room_id):
                    add_glossary_word(w["id"])
                player = Player(start_x, start_y)
                player.invincible_frames = 90  # ~1.5 s al entrar en sala (evitar muerte al instante)
                collected_masks = set(data.get("collected_masks", []))
                current_mask = data.get("current_mask")
                player.collected_masks = collected_masks.copy()
                if current_mask not in player.collected_masks and player.collected_masks:
                    current_mask = next(iter(player.collected_masks))
                player.mask_id = current_mask
                player.apply_mask_stats()
                lives = get_lives()
                coins = get_coins()
                camera_x = max(0, min(start_x - SCREEN_W // 2 + TILE_SIZE // 2, max(0, world_width - SCREEN_W)))

            message_paused = (level_narrative_timer > 0 or mask_pickup_message_timer > 0 or word_pickup_message_timer > 0)
            platforms = world_data["platforms"]
            hidden_platforms = world_data["hidden_platforms"]
            water = world_data["water"]
            doors = world_data["doors"]
            locked_doors = world_data["locked_doors"]
            mask_pickups = world_data["mask_pickups"]
            word_pickups = world_data["word_pickups"]
            spikes = world_data["spikes"]
            falling = world_data["falling"]
            hazards = world_data["hazards"]
            enemies = world_data["enemies"]
            npcs = world_data["npcs"]
            coins_group = world_data["coins"]
            use_hidden = player.sees_secrets()
            all_platforms = list(platforms) + (list(hidden_platforms) if use_hidden else [])
            water_rects = [w.rect for w in water]
            hint_near_door = False
            if not message_paused:
                for w in water:
                    w.update()

                player.update(platforms, [], water_rects, use_hidden, hidden_platforms if use_hidden else [])
                for m in mask_pickups:
                    m.update()
                for wp in word_pickups:
                    wp.update()
                for fp in falling:
                    fp.update()
                for h in hazards:
                    h.update()
                for e in enemies:
                    e.update(all_platforms)
                for c in coins_group:
                    c.update()
                for n in npcs:
                    n.update()
                shake.update()
                particles.update()

                for fp in falling:
                    on_fp = not fp.falling and player.rect.colliderect(fp.rect) and player.vel_y >= 0 and player.rect.bottom <= fp.rect.top + 10
                    if on_fp:
                        fp.stand_delay -= 1
                        if fp.stand_delay <= 0:
                            fp.trigger()
                            shake.trigger(10, 4)
                    else:
                        fp.stand_delay = 35

                for c in list(coins_group):
                    if player.rect.colliderect(c.rect):
                        particles.emit_coin(c.rect.centerx, c.rect.centery)
                        play_coin()
                        coins, extra = add_coins(10)
                        if extra:
                            set_lives(get_lives() + extra)
                        c.kill()
                coins = get_coins()
                if player.just_landed:
                    particles.emit_landing(player.rect.x, player.rect.y)
                    # Sonido de aterrizaje desactivado (era molesto con las partículas por abajo)

                for e in list(enemies):
                    if not player.rect.colliderect(e.rect):
                        continue
                    if player.vel_y > 0 and player.rect.bottom <= e.rect.top + 14:
                        mask_id = getattr(e, "mask_id", None)
                        cx, cy = e.rect.centerx - TILE_SIZE // 2, e.rect.top
                        e.kill()
                        player.vel_y = -10
                        play_jump()
                        play_stomp()
                        shake.trigger(8, 4)
                        particles.emit_stomp(e.rect.centerx, e.rect.centery, (180, 100, 80) if not mask_id else get_mask_color(mask_id))
                        if mask_id:
                            mask_pickups.add(MaskPickup(cx, cy, mask_id))
                            particles.emit_mask_pickup(e.rect.centerx, e.rect.centery, get_mask_color(mask_id))
                    elif not player.is_invincible_to_traps():
                        lives = _try_hurt_player(lives, player, start_x, start_y, shake, particles)
                        if lives <= 0:
                            state = STATE_GAME_OVER
                            player = None
                            world_data = None
                    break

                for m in list(mask_pickups):
                    if player.rect.colliderect(m.rect):
                        player.collect_mask(m.mask_id)
                        collected_masks.add(m.mask_id)
                        current_mask = m.mask_id
                        save_state(current_room_id, player.rect.x, player.rect.y, player.collected_masks, player.mask_id, lives, coins)
                        particles.emit_mask_pickup(m.rect.x, m.rect.y, get_mask_color(m.mask_id))
                        particles.emit_sparkle(m.rect.centerx, m.rect.centery, get_mask_color(m.mask_id))
                        m.kill()
                        play_mask_pickup()
                        shake.trigger(6, 3)
                        msg = MASK_PICKUP_MESSAGES.get(m.mask_id, {})
                        mask_pickup_message_timer = 1
                        mask_pickup_message_es = msg.get("es", get_mask_name(m.mask_id))
                        mask_pickup_message_nasa = msg.get("nasa", "")

                for wp in list(word_pickups):
                    if player.rect.colliderect(wp.rect):
                        add_word_collected(wp.word_id)
                        play_word_sound(wp.word_id)
                        w = get_word_by_id(wp.word_id)
                        word_pickup_message_timer = 1
                        word_pickup_message_es = "Español: " + (w["es"] if w else "") + "  →  Nasa Yuwe: " + (w["nasa"] if w else "")
                        word_pickup_message_nasa = ""
                        wp.kill()
                        break

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    for door in locked_doors:
                        if player.rect.colliderect(door.rect) and player.can_open_doors():
                            target = door.target_room
                            sx = door.spawn_x
                            sy = door.spawn_y - TILE_SIZE * 2
                            save_state(target, sx, sy, player.collected_masks, player.mask_id, lives, coins)
                            current_room_id = target
                            collected_masks = player.collected_masks.copy()
                            current_mask = player.mask_id
                            player = None
                            world_data = None
                            shake.trigger(5, 2)
                            play_door_open()
                            break
                    for n in npcs:
                        if not n.given and player.rect.colliderect(n.rect) and n.mask_id:
                            n.given = True
                            player.collect_mask(n.mask_id)
                            collected_masks.add(n.mask_id)
                            current_mask = n.mask_id
                            save_state(current_room_id, player.rect.x, player.rect.y, player.collected_masks, player.mask_id, lives, coins)
                            msg = MASK_PICKUP_MESSAGES.get(n.mask_id, {})
                            mask_pickup_message_timer = 1
                            mask_pickup_message_es = msg.get("es", get_mask_name(n.mask_id))
                            mask_pickup_message_nasa = msg.get("nasa", "")
                            npc_message_timer = 0
                            npc_message_text = ""
                            play_mask_pickup()
                            particles.emit_mask_pickup(n.rect.centerx, n.rect.centery, get_mask_color(n.mask_id))
                            particles.emit_sparkle(n.rect.centerx, n.rect.centery, get_mask_color(n.mask_id))
                            shake.trigger(6, 3)
                            break

                hint_near_door = False
                if player is not None:
                    for door in doors:
                        # Zona de activación más amplia para que sea fácil salir (camina hacia la puerta)
                        trigger = door.rect.inflate(32, 24)
                        if player.rect.colliderect(trigger):
                            hint_near_door = True
                        if player.rect.colliderect(trigger):
                            target = door.target_room
                            if target == "victory":
                                save_state(current_room_id, player.rect.x, player.rect.y,
                                           player.collected_masks, player.mask_id, lives, coins, game_completed=True)
                                state = STATE_VICTORY
                                victory_masks = len(player.collected_masks)
                                victory_coins = get_coins()
                                victory_lives = lives
                                player = None
                                world_data = None
                                shake.trigger(8, 4)
                                play_level_complete()
                            else:
                                sx = door.spawn_x
                                sy = door.spawn_y - TILE_SIZE * 2  # rect.y: pies sobre plataforma
                                save_state(target, sx, sy, player.collected_masks, player.mask_id, lives, coins)
                                current_room_id = target
                                collected_masks = player.collected_masks.copy()
                                current_mask = player.mask_id
                                player = None
                                world_data = None
                                shake.trigger(5, 2)
                                play_door_open()
                            break

                if player is None:
                    clock.tick(FPS)
                    continue

                for s in spikes:
                    if player.rect.colliderect(s.rect) and not player.is_invincible_to_traps():
                        lives = _try_hurt_player(lives, player, start_x, start_y, shake, particles)
                        if lives <= 0:
                            state = STATE_GAME_OVER
                            player = None
                            world_data = None
                        break
                if player is None:
                    clock.tick(FPS)
                    continue
                for h in hazards:
                    if player.rect.colliderect(h.rect) and not player.is_invincible_to_traps():
                        lives = _try_hurt_player(lives, player, start_x, start_y, shake, particles)
                        if lives <= 0:
                            state = STATE_GAME_OVER
                            player = None
                            world_data = None
                        break
                if player is None:
                    clock.tick(FPS)
                    continue
                if player.in_water and not (player._swim or can_swim(player.mask_id)) and not player.is_invincible_to_traps():
                    for wr in water_rects:
                        if player.rect.colliderect(wr):
                            lives = _try_hurt_player(lives, player, start_x, start_y, shake, particles)
                            if lives <= 0:
                                state = STATE_GAME_OVER
                                player = None
                                world_data = None
                            break
                if player is None:
                    clock.tick(FPS)
                    continue
                if state == STATE_GAME_OVER:
                    screen.fill((50, 30, 30))
                    draw_game_over(screen, font_large, font_small)
                    inst = font_small.render("ENTER o ESPACIO: Reintentar o Volver al menú", 1, (220, 200, 200))
                    screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, SCREEN_H // 2 + 50))
                    pygame.display.flip()
                    clock.tick(FPS)
                    continue

                if player.rect.y > SCREEN_H + 100:
                    lives = get_lives() - 1
                    set_lives(lives)
                    if lives <= 0:
                        state = STATE_GAME_OVER
                        player = None
                        world_data = None
                    else:
                        player.rect.x = start_x
                        player.rect.y = start_y
                        player.vel_x = player.vel_y = 0
                        player.invincible_frames = 90
                        shake.trigger(15, 6)

                # Cámara con deadzone y suavizado
                player_center_x = player.rect.x + player.rect.w // 2
                left_bound = camera_x + SCREEN_W * CAMERA_DEADZONE_LEFT
                right_bound = camera_x + SCREEN_W * (1 - CAMERA_DEADZONE_RIGHT)
                if player_center_x < left_bound:
                    cam_target = player_center_x - SCREEN_W * CAMERA_DEADZONE_LEFT
                elif player_center_x > right_bound:
                    cam_target = player_center_x - SCREEN_W * (1 - CAMERA_DEADZONE_RIGHT)
                else:
                    cam_target = camera_x
                camera_x = camera_x + (cam_target - camera_x) * CAMERA_SMOOTH
                camera_x = max(0, min(camera_x, max(0, world_width - SCREEN_W)))
                sx, sy = shake.offset()
                draw_cam_x = int(camera_x) + sx

                if zone_splash_timer > 0:
                    zone_splash_timer -= 1

            if message_paused:
                sx, sy = shake.offset()
                draw_cam_x = int(camera_x) + sx

            bg_colors = _get_bg_for_zone(zone_name)
            for y in range(0, SCREEN_H + 4, 4):
                t = y / SCREEN_H
                c = (
                    int(bg_colors[0][0] * (1 - t) + bg_colors[1][0] * t),
                    int(bg_colors[0][1] * (1 - t) + bg_colors[1][1] * t),
                    int(bg_colors[0][2] * (1 - t) + bg_colors[1][2] * t),
                )
                pygame.draw.rect(screen, c, (0, y, SCREEN_W, 4))
            draw_parallax_bg(screen, int(camera_x), world_width, zone_name, SCREEN_H)
            for p in platforms:
                p.draw(screen, draw_cam_x)
            for w in water:
                w.draw(screen, draw_cam_x)
            for p in hidden_platforms:
                p.draw(screen, draw_cam_x, visible=use_hidden)
            for s in spikes:
                s.draw(screen, draw_cam_x)
            for fp in falling:
                fp.draw(screen, draw_cam_x)
            for h in hazards:
                h.draw(screen, draw_cam_x)
            for d in doors:
                d.draw(screen, draw_cam_x)
            for ld in locked_doors:
                ld.draw(screen, draw_cam_x)
            for c in coins_group:
                c.draw(screen, draw_cam_x)
            for m in mask_pickups:
                m.draw(screen, draw_cam_x)
            for wp in word_pickups:
                wp.draw(screen, draw_cam_x)
            draw_world_labels(screen, player.rect, water, doors, draw_cam_x)
            for e in enemies:
                e.draw(screen, draw_cam_x)
            for n in npcs:
                n.draw(screen, draw_cam_x)
            particles.draw(screen, draw_cam_x)
            player.draw(screen, draw_cam_x)
            draw_hud(screen, player, room_name_str, get_lives(), coins)
            mouth_open = (pygame.time.get_ticks() // 200 % 2 == 0)
            bubble_play_rect = None
            bubble_pause_rect = None
            bubble_text_to_speak = ""
            if mask_pickup_message_timer > 0:
                if mask_pickup_message_es or mask_pickup_message_nasa:
                    bubble_play_rect, bubble_pause_rect = draw_speech_bubble_character(screen, mask_pickup_message_es, mask_pickup_message_nasa, font_small, mouth_open, speaker="nasa_elder")
                    bubble_text_to_speak = (mask_pickup_message_es or "") + " " + (mask_pickup_message_nasa or "")
                    hint_close = font_small.render("ESPACIO o E: continuar   |   Clic en Play: escuchar   Pausa: detener", 1, (130, 120, 150))
                    screen.blit(hint_close, (SCREEN_W // 2 - hint_close.get_width() // 2, SCREEN_H - 50))
            elif word_pickup_message_timer > 0:
                if word_pickup_message_es or word_pickup_message_nasa:
                    bubble_play_rect, bubble_pause_rect = draw_speech_bubble_character(screen, word_pickup_message_es, word_pickup_message_nasa, font_small, mouth_open, speaker="nasa_elder")
                    bubble_text_to_speak = (word_pickup_message_es or "") + " " + (word_pickup_message_nasa or "")
                    hint_close = font_small.render("ESPACIO o E: continuar   |   Clic en Play: escuchar   Pausa: detener", 1, (130, 120, 150))
                    screen.blit(hint_close, (SCREEN_W // 2 - hint_close.get_width() // 2, SCREEN_H - 50))
            elif level_narrative_timer > 0:
                intro = LEVEL_INTRO_MESSAGES.get(current_room_id)
                if intro:
                    speaker = "player" if (current_room_id == "pueblo_1" and len(player.collected_masks) == 0) else "nasa_elder"
                    bubble_play_rect, bubble_pause_rect = draw_speech_bubble_character(screen, intro["es"], intro["nasa"], font_small, mouth_open, speaker=speaker)
                    bubble_text_to_speak = (intro["es"] or "") + " " + (intro["nasa"] or "")
                    hint_close = font_small.render("ESPACIO o E: continuar   |   Clic en Play: escuchar   Pausa: detener", 1, (130, 120, 150))
                    screen.blit(hint_close, (SCREEN_W // 2 - hint_close.get_width() // 2, SCREEN_H - 50))
            if zone_splash_timer > 0:
                total = int(ZONE_SPLASH_DURATION * FPS)
                alpha = 255
                if zone_splash_timer > total - 20:
                    alpha = int(255 * (total - zone_splash_timer) / 20)
                elif zone_splash_timer < 25:
                    alpha = int(255 * zone_splash_timer / 25)
                draw_zone_splash(screen, zone_splash_name, alpha, font_large)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_PAUSED:
            if pause_glossary_open:
                draw_glossary_screen(screen, font_large, font_small, get_glossary_unlocked())
            else:
                draw_pause_menu(screen, font_large, font_small, pause_selected)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if state == STATE_GAME_OVER:
            screen.fill((50, 30, 30))
            draw_game_over(screen, font_large, font_small)
            W, H = screen.get_width(), screen.get_height()
            inst = font_small.render("ENTER o ESPACIO: Reintentar (si quedan vidas) o Volver al menú", 1, (220, 200, 200))
            screen.blit(inst, (W // 2 - inst.get_width() // 2, H // 2 + 50))
            pygame.display.flip()
            clock.tick(FPS)
            continue

        clock.tick(FPS)


if __name__ == "__main__":
    main()
