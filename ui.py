import pygame
import item # Import the item module

class TabView:
    def __init__(self, rect, tabs, character=None):
        self.tabs = tabs
        self.character = character
        self.font = pygame.font.Font(None, 32)
        self.active_tab = 0
        self.update_rect(rect)

        self.dragging_item = False
        self.dragged_item_id = None
        self.dragged_item_offset_x = 0
        self.dragged_item_offset_y = 0
        self.item_rects = {} # Stores {item_id: pygame.Rect} for click detection
        self.equipped_slot_rects = {} # Stores {slot_name: pygame.Rect} for drop detection
        self.carried_rect = None # Stores the rect for the carried items area

    def update_rect(self, rect):
        self.rect = rect
        self.tab_rects = []
        tab_width = self.rect.width // len(self.tabs)
        for i, tab in enumerate(self.tabs):
            self.tab_rects.append(pygame.Rect(self.rect.x + i * tab_width, self.rect.y, tab_width, 40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.tabs[self.active_tab] == "Inventory" and self.character:
                for item_id, rect in self.item_rects.items():
                    if rect.collidepoint(event.pos):
                        self.dragging_item = True
                        self.dragged_item_id = item_id
                        self.dragged_item_offset_x = rect.x - event.pos[0]
                        self.dragged_item_offset_y = rect.y - event.pos[1]
                        # Remove item from its current location temporarily for visual drag
                        if item_id in self.character.inventory["carried"]:
                            self.character.remove_from_carried(item_id)
                        else: # Check equipped slots
                            for slot, eq_item_id in self.character.inventory["equipped"].items():
                                if eq_item_id == item_id:
                                    self.character.unequip_item(slot) # This will move it to carried
                                    self.character.remove_from_carried(item_id) # Then remove from carried
                                    break
                        break
            for i, tab_rect in enumerate(self.tab_rects):
                if tab_rect.collidepoint(event.pos):
                    self.active_tab = i
                    break
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_item:
                dropped = False
                # Try to equip
                item_obj = item.get_item_by_id(self.dragged_item_id)
                if item_obj and item_obj.slot:
                    for slot_name, slot_rect in self.equipped_slot_rects.items():
                        if slot_rect.collidepoint(event.pos):
                            if self.character.equip_item(self.dragged_item_id):
                                dropped = True
                                break
                
                # If not equipped, try to add to carried
                if not dropped and self.carried_rect and self.carried_rect.collidepoint(event.pos):
                    self.character.add_to_carried(self.dragged_item_id)
                    dropped = True
                
                # If not dropped anywhere valid, return to carried
                if not dropped:
                    self.character.add_to_carried(self.dragged_item_id)

                self.dragging_item = False
                self.dragged_item_id = None
        
        if event.type == pygame.MOUSEMOTION and self.dragging_item:
            pass # Position is handled in draw for now, but will be used for actual drag

    def draw(self, surface):
        # Draw the tab buttons
        for i, tab in enumerate(self.tabs):
            tab_rect = self.tab_rects[i]
            if i == self.active_tab:
                pygame.draw.rect(surface, (200, 200, 200), tab_rect)
            else:
                pygame.draw.rect(surface, (150, 150, 150), tab_rect)
            pygame.draw.rect(surface, (0, 0, 0), tab_rect, 2)
            text_surf = self.font.render(tab, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=tab_rect.center)
            surface.blit(text_surf, text_rect)

        # Draw the content of the active tab
        content_rect = pygame.Rect(self.rect.x, self.rect.y + 40, self.rect.width, self.rect.height - 40)
        pygame.draw.rect(surface, (220, 220, 220), content_rect)
        pygame.draw.rect(surface, (0, 0, 0), content_rect, 2)

        if self.tabs[self.active_tab] == "Character" and self.character:
            self.draw_character_info(surface, content_rect)
        elif self.tabs[self.active_tab] == "Inventory" and self.character:
            self.draw_inventory_info(surface, content_rect)
        else:
            active_tab_text = self.tabs[self.active_tab]
            text_surf = self.font.render(active_tab_text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=content_rect.center)
            surface.blit(text_surf, text_rect)

        # Draw dragged item on top
        if self.dragging_item and self.dragged_item_id:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item_obj = item.get_item_by_id(self.dragged_item_id)
            if item_obj:
                item_name_text = self.font.render(item_obj.name, True, (0,0,0))
                surface.blit(item_name_text, (mouse_x + self.dragged_item_offset_x, mouse_y + self.dragged_item_offset_y))


    def draw_character_info(self, surface, rect):
        y_offset = rect.y + 20
        
        name_text = self.font.render(f"Name: {self.character.name}", True, (0,0,0))
        surface.blit(name_text, (rect.x + 20, y_offset))
        y_offset += 40

        race_text = self.font.render(f"Race: {self.character.race}", True, (0,0,0))
        surface.blit(race_text, (rect.x + 20, y_offset))
        y_offset += 40

        strength_text = self.font.render(f"Strength: {self.character.strength}", True, (0,0,0))
        surface.blit(strength_text, (rect.x + 20, y_offset))
        y_offset += 40

        dexterity_text = self.font.render(f"Dexterity: {self.character.dexterity}", True, (0,0,0))
        surface.blit(dexterity_text, (rect.x + 20, y_offset))
        y_offset += 40

        constitution_text = self.font.render(f"Constitution: {self.character.constitution}", True, (0,0,0))
        surface.blit(constitution_text, (rect.x + 20, y_offset))
        y_offset += 40

        intelligence_text = self.font.render(f"Intelligence: {self.character.intelligence}", True, (0,0,0))
        surface.blit(intelligence_text, (rect.x + 20, y_offset))
        y_offset += 40

        wisdom_text = self.font.render(f"Wisdom: {self.character.wisdom}", True, (0,0,0))
        surface.blit(wisdom_text, (rect.x + 20, y_offset))
        y_offset += 40

        charisma_text = self.font.render(f"Charisma: {self.character.charisma}", True, (0,0,0))
        surface.blit(charisma_text, (rect.x + 20, y_offset))

    def draw_inventory_info(self, surface, rect):
        self.item_rects = {} # Clear item rects for current frame
        self.equipped_slot_rects = {} # Clear equipped slot rects for current frame

        # Equipped items
        equipped_y_offset = rect.y + 20
        equipped_text = self.font.render("Equipped:", True, (0,0,0))
        surface.blit(equipped_text, (rect.x + 20, equipped_y_offset))
        equipped_y_offset += 40

        for slot, item_id in self.character.inventory["equipped"].items():
            item_display_text = f"{slot.replace('_', ' ').title()}: "
            item_name_text_surf = self.font.render(item_display_text, True, (0,0,0))
            item_rect = item_name_text_surf.get_rect(topleft=(rect.x + 40, equipped_y_offset))
            
            if item_id:
                item_obj = item.get_item_by_id(item_id)
                if item_obj:
                    item_display_text += item_obj.name
                    item_name_text_surf = self.font.render(item_display_text, True, (0,0,0))
                    item_rect = item_name_text_surf.get_rect(topleft=(rect.x + 40, equipped_y_offset))
                    surface.blit(item_name_text_surf, item_rect)
                    self.item_rects[item_id] = item_rect # Store rect for actual item
            else:
                item_display_text += "Empty"
                item_name_text_surf = self.font.render(item_display_text, True, (0,0,0))
                item_rect = item_name_text_surf.get_rect(topleft=(rect.x + 40, equipped_y_offset))
                surface.blit(item_name_text_surf, item_rect)
            
            self.equipped_slot_rects[slot] = item_rect # Store rect for the slot itself
            equipped_y_offset += 30

        # Carried items
        carried_y_offset = equipped_y_offset + 20
        carried_text = self.font.render("Carried:", True, (0,0,0))
        surface.blit(carried_text, (rect.x + 20, carried_y_offset))
        carried_y_offset += 40

        # Define the carried items area for dropping
        self.carried_rect = pygame.Rect(rect.x + 20, carried_y_offset, rect.width - 40, rect.height - (carried_y_offset - rect.y))
        pygame.draw.rect(surface, (200, 200, 200), self.carried_rect, 1) # Draw a border for clarity

        if self.character.inventory["carried"]:
            for item_id in self.character.inventory["carried"]:
                item_obj = item.get_item_by_id(item_id)
                if item_obj:
                    item_display_text = f"- {item_obj.name}"
                    item_name_text_surf = self.font.render(item_display_text, True, (0,0,0))
                    item_rect = item_name_text_surf.get_rect(topleft=(rect.x + 40, carried_y_offset))
                    surface.blit(item_name_text_surf, item_rect)
                    self.item_rects[item_id] = item_rect # Store rect for carried items
                    carried_y_offset += 30
        else:
            no_items_text = self.font.render("No items carried.", True, (0,0,0))
            surface.blit(no_items_text, (rect.x + 40, carried_y_offset))


class ChatWindow:
    def __init__(self, rect):
        self.font = pygame.font.Font(None, 24)
        self.history = []
        self.input_text = ""
        self.update_rect(rect)

    def update_rect(self, rect):
        self.rect = rect
        self.history_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height - 40)
        self.input_rect = pygame.Rect(rect.x, rect.y + rect.height - 40, rect.width, 40)

    def add_message(self, message):
        words = message.split(' ')
        lines = []
        current_line = ""
        for word in words:
            if self.font.size(current_line + " " + word)[0] < self.history_rect.width - 20:
                current_line += " " + word
            else:
                lines.append(current_line.strip())
                current_line = " " + word
        lines.append(current_line.strip())
        
        for line in lines:
            self.history.append(line)
            if len(self.history) * 20 > self.history_rect.height:
                self.history.pop(0)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text:
                    user_input = self.input_text
                    self.add_message("> " + user_input)
                    self.input_text = ""
                    return user_input
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode
        return None

    def draw(self, surface):
        # Draw chat history area
        pygame.draw.rect(surface, (220, 220, 220), self.history_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.history_rect, 2)
        for i, message in enumerate(self.history):
            text_surf = self.font.render(message, True, (0, 0, 0))
            surface.blit(text_surf, (self.history_rect.x + 10, self.history_rect.y + 10 + i * 20))

        # Draw input box
        pygame.draw.rect(surface, (255, 255, 255), self.input_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.input_rect, 2)
        input_surf = self.font.render("> " + self.input_text, True, (0, 0, 0))
        surface.blit(input_surf, (self.input_rect.x + 10, self.input_rect.y + 10))

class PartyWindow:
    def __init__(self, rect):
        self.font = pygame.font.Font(None, 32)
        self.update_rect(rect)

    def update_rect(self, rect):
        self.rect = rect

    def draw(self, surface):
        pygame.draw.rect(surface, (220, 220, 220), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        title_text = self.font.render("Party, NPCs, & Enemies", True, (0,0,0))
        title_rect = title_text.get_rect(center=(self.rect.centerx, self.rect.y + 20))
        surface.blit(title_text, title_rect)