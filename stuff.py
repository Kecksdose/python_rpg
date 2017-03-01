import copy
implemented_attributes = {'strenght', 'agility', 'intelligence'}
implemented_slots = {'weapon', 'legs', 'arms', 'chest', None}

class Hero:
    """Basic hero class for characters."""

    def __init__(self, name='',
                 hero_class='',
                 level=1,
                 attributes=implemented_attributes,
                 hitpoints=10,
                 inventory=[],
                 equipped={},
                 xp_points=0,
                 gold=0,
                 base_damage=[1,1]):
        """Returns base hero class."""
        self.name = name
        self.hero_class = hero_class
        self.level = level
        self.base_attributes = {attributes: 1 for attributes in implemented_attributes}
        self.current_attributes = self.base_attributes
        self.hitpoints = hitpoints
        self.current_hitpoints = hitpoints
        self.xp_points = xp_points

        self.inventory = inventory
        self.equipped = {slot: None for slot in implemented_slots
                         if slot}
        self.gold = gold

        self.base_damage = base_damage
        self.current_damage = base_damage
        self.is_alive = True

    def describe(self,
                 show_attributes=False,
                 show_inventory=False,
                 show_equipped=False):
        """Describe hero object."""
        print(f'Name: {self.name}')
        print(f'Class: {self.hero_class}')
        print(f'Level: {self.level} ({self.xp_points} xp)')
        if show_attributes:
            print('Attributes:')
            for att, val in self.current_attributes.items():
                print(f'\t{att}: {val}')
        print(f'Damage: {self.current_damage}')
        print()
        if show_inventory:
            if len(self.inventory) > 0:
                print('Items:')
                for item_number, item in enumerate(self.inventory, start=1):
                    print(f'\tPosition {item_number}: {item.name}')
            else:
                print('\tNo items found...')
        if show_equipped:
            if any(self.equipped.values()):
                print('Items equipped:')
                for slot, item in self.equipped.items():
                    if item:
                        print(f'\tSlot {slot}: {item.name}')
            else:
                print('No items equipped...')

    def receive_item(self, item):
        """Puts Item into inventory."""
        self.inventory.append(item)
        print(f'{item.name} recieved.')

    def equip_item(self, item_number):
        """Equips/consumes item."""
        if len(self.inventory) == 0:
            print('No items in inventory.')
            return
        elif item_number > len(self.inventory) or item_number < 1:
            print('Item not found.')
            return

        # Until now, the item must exist.
        if self.inventory[item_number - 1].is_consumable == True:
            # TODO: Apply functionality
            item_name = self.inventory.pop(item_number - 1).name
            print(f'{item_name} consumed. It was tasty.')
            return

        # Try to equip item
        item_slot = self.inventory[item_number - 1].slot
        old_item = self.equipped[item_slot]
        self.equipped[item_slot] = self.inventory.pop(item_number - 1)
        if old_item:
            self.inventory.append(old_item)
        print(f'{self.equipped[item_slot].name} equipped.')
        self._update_attributes()

    def unequip_item(self, slot):
        """Unequips item and puts it back to inventory."""
        if not slot in self.equipped.keys():
            print('No such slot available. Chose from the following:')
            print(list(self.equipped.keys()))
            return
        if self.equipped[slot]:
            self.inventory.append(self.equipped[slot])
            print(f'Put {self.equipped[slot].name} back to inventory.')
            self.equipped[slot] = None
            self._update_attributes()
        else:
            print(f'No item found at slot {slot}.')


    def _update_attributes(self):
        """Updates all attributes (e.g. after equipping an item)."""
        self.current_attributes = copy.deepcopy(self.base_attributes)
        self.current_damage = copy.deepcopy(self.base_damage)
        for item in self.equipped.values():
            if item:
                # Update attributes
                for attr, val in item.attribute_boni.items():
                    if attr not in self.base_attributes.keys():
                        # This case should never happen.
                        print(f'ERROR: Attribute {attr} not found. Will skip it.')
                    else:
                        self.current_attributes[attr] += val
                # Update damage
                if item.damage_bonus:
                    self.current_damage[0] += item.damage_bonus[0]
                    self.current_damage[1] += item.damage_bonus[1]


class Item():
    """Basic item class."""

    def __init__(self,
                 name,
                 slot,
                 attribute_boni,
                 damage_bonus,
                 is_consumable,
                 description=''
                 ):
        self.name = name
        self.slot = slot
        self.attribute_boni = attribute_boni
        self.damage_bonus = damage_bonus
        self.is_consumable = is_consumable
        self.description = description

    def describe(self):
        """Describe item object."""
        print(f'Name: {self.name}')
        print(f'Slot: {self.slot}')
        if len(self.attribute_boni) > 0:
            print('Attribute boni:')
            for att, val in self.attribute_boni.items():
                print(f'\t{att}: {val:+}')
        if self.damage_bonus:
            print(f'Damage: {self.damage_bonus[0]} - {self.damage_bonus[1]}')
        if self.description:
            print(f'Description: {self.description}')
