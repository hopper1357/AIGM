import pygame
import config
import ui
import database
import llm
from character import Character

def update_ui_layout(screen, tab_view, chat_window, party_window, divider1_x, divider2_x):
    screen_width, screen_height = screen.get_size()
    
    left_panel_rect = pygame.Rect(0, 0, divider1_x, screen_height)
    middle_panel_rect = pygame.Rect(divider1_x, 0, divider2_x - divider1_x, screen_height)
    right_panel_rect = pygame.Rect(divider2_x, 0, screen_width - divider2_x, screen_height)

    tab_view.update_rect(left_panel_rect)
    chat_window.update_rect(middle_panel_rect)
    party_window.update_rect(right_panel_rect)


def main():
    pygame.init()
    database.initialize_database()

    # Try to load character, otherwise create a new one
    player_character = database.load_character(1) # Using fixed ID 1 for now
    if player_character is None:
        # Add sample items to the database (only if creating a new character)
        dagger_id = database.add_item({
            'name': 'Dagger', 'class': 'weapon', 'subclass': 'dagger', 'rarity': 'common',
            'description': 'A sharp, small dagger.', 'damage': '1d4', 'damage_type': 'piercing',
            'slot': 'main_hand', 'weight': 1.0, 'value': 5
        })
        leather_armor_id = database.add_item({
            'name': 'Leather Armor', 'class': 'armor', 'subclass': 'light armor', 'rarity': 'common',
            'description': 'Light and flexible leather armor.', 'armor_class': 11,
            'slot': 'chest', 'weight': 10.0, 'value': 10
        })
        healing_potion_id = database.add_item({
            'name': 'Potion of Healing', 'class': 'potion', 'subclass': 'healing potion', 'rarity': 'common',
            'description': 'Heals 2d4+2 hit points.', 'effect': 'heal 2d4+2 HP', 'uses': 1,
            'duration': 'instant', 'weight': 0.5, 'value': 25
        })
        ring_of_protection_id = database.add_item({
            'name': 'Ring of Protection', 'class': 'ring', 'subclass': 'ring of protection', 'rarity': 'rare',
            'description': 'A ring that offers magical protection.', 'magical': 1, 'enchantment': 'protection +1',
            'slot': 'ring', 'weight': 0.1, 'value': 500
        })

        player_character = Character(
            name="Player 1", 
            race="Human", 
            strength=10, 
            dexterity=10, 
            constitution=10, 
            intelligence=10, 
            wisdom=10, 
            charisma=10
        )
        player_character.inventory["equipped"]["main_hand"] = dagger_id
        player_character.inventory["equipped"]["chest"] = leather_armor_id
        player_character.inventory["carried"].append(healing_potion_id)
        player_character.inventory["carried"].append(ring_of_protection_id)
        database.save_character(player_character) # Save new character

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("AIGM")
    fullscreen = False

    divider1_x = int(config.SCREEN_WIDTH * 0.25)
    divider2_x = int(config.SCREEN_WIDTH * 0.75)
    
    dragging_divider1 = False
    dragging_divider2 = False

    # Create the UI elements
    tabs = ["Character", "Inventory", "Quests", "Menu"]
    tab_view = ui.TabView(pygame.Rect(0,0,0,0), tabs, player_character)
    chat_window = ui.ChatWindow(pygame.Rect(0,0,0,0))
    party_window = ui.PartyWindow(pygame.Rect(0,0,0,0))
    
    update_ui_layout(screen, tab_view, chat_window, party_window, divider1_x, divider2_x)

    # Create the AI Dungeon Master
    dungeon_master = llm.LLM_DM()
    story_prompt = "This is the beginning of your adventure. You are in a dark tavern. What do you do?"
    chat_window.add_message(story_prompt)


    # Colors
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                database.save_character(player_character) # Save character on exit
            if event.type == pygame.VIDEORESIZE:
                divider1_x = int(screen.get_width() * 0.25)
                divider2_x = int(screen.get_width() * 0.75)
                update_ui_layout(screen, tab_view, chat_window, party_window, divider1_x, divider2_x)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
                    
                    divider1_x = int(screen.get_width() * 0.25)
                    divider2_x = int(screen.get_width() * 0.75)
                    update_ui_layout(screen, tab_view, chat_window, party_window, divider1_x, divider2_x)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if abs(event.pos[0] - divider1_x) < 5:
                    dragging_divider1 = True
                if abs(event.pos[0] - divider2_x) < 5:
                    dragging_divider2 = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                dragging_divider1 = False
                dragging_divider2 = False
                # Pass mouse up event to tab_view for drag and drop handling
                tab_view.handle_event(event) # Pass player_character here

            if event.type == pygame.MOUSEMOTION:
                if dragging_divider1:
                    divider1_x = event.pos[0]
                    update_ui_layout(screen, tab_view, chat_window, party_window, divider1_x, divider2_x)
                if dragging_divider2:
                    divider2_x = event.pos[0]
                    update_ui_layout(screen, tab_view, chat_window, party_window, divider1_x, divider2_x)


            tab_view.handle_event(event) # Pass all events to tab_view
            user_input = chat_window.handle_event(event)
            if user_input:
                response = dungeon_master.get_story_prompt(user_input)
                chat_window.add_message(response)

        screen.fill(BLACK)

        # Draw the UI elements
        tab_view.draw(screen)
        chat_window.draw(screen)
        party_window.draw(screen)

        # Draw the dividers
        pygame.draw.line(screen, GRAY, (divider1_x, 0), (divider1_x, screen.get_height()), 5)
        pygame.draw.line(screen, GRAY, (divider2_x, 0), (divider2_x, screen.get_height()), 5)


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
