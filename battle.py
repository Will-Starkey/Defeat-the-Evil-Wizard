import random
import time

# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health
        # defensive flags
        self.evade_active = False  # completely avoid next attack
        self.shield_active = False  # block next attack

    def attack(self, opponent):
        # randomized damage within a small range
        min_dmg = max(1, self.attack_power - 5)
        max_dmg = self.attack_power + 5
        damage = random.randint(min_dmg, max_dmg)
        opponent._take_damage(damage)
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")

    def _take_damage(self, damage):
        # applies evade or shield if active
        if self.evade_active:
            print(f"{self.name} evades the attack and takes no damage!")
            self.evade_active = False
            return
        if self.shield_active:
            print(f"{self.name}'s Divine Shield blocks the attack!")
            self.shield_active = False
            return
        self.health -= damage

    def heal(self, amount=25):
        if self.health <= 0:
            print(f"{self.name} cannot be healed because they are defeated.")
            return
        before = self.health
        self.health = min(self.max_health, self.health + amount)
        healed = self.health - before
        print(f"{self.name} heals for {healed} health (now {self.health}/{self.max_health}).")

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")
        flags = []
        if self.evade_active:
            flags.append('Evade (next)')
        if self.shield_active:
            flags.append('Shield (next)')
        if flags:
            print("Active buffs:", ", ".join(flags))


# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)

    def heavy_strike(self, opponent):
        # Heavy strike: higher potential damage
        base = self.attack_power + 10
        min_dmg = max(1, base - 5)
        max_dmg = base + 10
        damage = random.randint(min_dmg, max_dmg)
        opponent._take_damage(damage)
        print(f"{self.name} uses Heavy Strike on {opponent.name} for {damage} damage!")

    def rally(self):
        # Small heal for self
        self.heal(20)
        print(f"{self.name} rallies and gains resolve.")


# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

    def fireball(self, opponent):
        # Fireball: chance for critical
        damage = random.randint(self.attack_power - 5, self.attack_power + 10)
        crit = random.random() < 0.2
        if crit:
            damage = int(damage * 1.5)
            print("A critical fireball!", end=' ')
        opponent._take_damage(damage)
        print(f"{self.name} casts Fireball at {opponent.name} for {damage} damage!")

    def mana_shield(self):
        # Mage's shield acts like a weaker divine shield
        self.shield_active = True
        print(f"{self.name} raises a Mana Shield and will block the next attack.")


# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)
        self.minions = []
        self.summoned = False

    def regenerate(self):
        if self.health <= 0:
            return
        before = self.health
        self.health = min(self.max_health, self.health + 5)
        regen_amt = self.health - before
        if regen_amt > 0:
            print(f"{self.name} regenerates {regen_amt} health! Current health: {self.health}/{self.max_health}")

    def attack(self, opponent):
        # Wizard deals variable magical damage
        min_dmg = max(1, self.attack_power - 3)
        max_dmg = self.attack_power + 8
        damage = random.randint(min_dmg, max_dmg)
        opponent._take_damage(damage)
        print(f"{self.name} hurls dark magic at {opponent.name} for {damage} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")

    def summon_minions(self):
        if self.summoned:
            return
        print(f"{self.name} screams and summons 3 minions to defend itself!")
        self.minions = [Minion(f"Minion #{i+1}") for i in range(3)]
        self.summoned = True


# Create Archer class
class Archer(Character):
    def __init__(self, name):
        # Archer is a nimble ranged attacker
        super().__init__(name, health=110, attack_power=30)

    def quick_shot(self, opponent):
        # Quick Shot: two smaller attacks
        print(f"{self.name} uses Quick Shot!")
        for i in range(2):
            min_dmg = max(1, int(self.attack_power * 0.6))
            max_dmg = int(self.attack_power * 0.9)
            damage = random.randint(min_dmg, max_dmg)
            opponent._take_damage(damage)
            print(f"  Arrow {i+1} hits for {damage} damage.")
            time.sleep(0.15)
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")

    def evade(self):
        # Evade: avoid the next incoming attack
        self.evade_active = True
        print(f"{self.name} focuses and will evade the next attack.")


# Create Dwarf class (renamed from Paladin)
class Dwarf(Character):
    def __init__(self, name):
        # Dwarf: high health, moderate attack
        super().__init__(name, health=160, attack_power=20)

    def war_axe(self, opponent):
        # War Axe: powerful fixed-damage attack (45 damage)
        damage = 45
        opponent._take_damage(damage)
        print(f"{self.name} swings a mighty War Axe at {opponent.name} for {damage} damage!")

    def divine_shield(self):
        # Shield: blocks the next attack
        self.shield_active = True
        print(f"{self.name} raises a Divine Shield and will block the next attack.")


# Create Knight class
class Knight(Character):
    def __init__(self, name):
        # Knight: sturdy front-line fighter
        super().__init__(name, health=150, attack_power=22)

    def long_sword(self, opponent):
        # Long Sword: powerful fixed-damage attack (38 damage)
        damage = 38
        opponent._take_damage(damage)
        print(f"{self.name} strikes with Long Sword at {opponent.name} for {damage} damage!")

    def shield_stance(self):
        # Shield Stance: prepare to block next attack
        self.shield_active = True
        print(f"{self.name} takes a Shield Stance and will block the next attack.")


# Minion class
class Minion(Character):
    def __init__(self, name):
        super().__init__(name, health=10, attack_power=5)

    def attack(self, opponent):
        # Minions deal a fixed 5 damage
        damage = self.attack_power
        opponent._take_damage(damage)
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")


def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    print("4. Dwarf")
    print("5. Knight")

    class_choice = input("Enter the number of your class choice: ").strip()
    name = input("Enter your character's name: ").strip() or "Hero"

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Archer(name)
    elif class_choice == '4':
        return Dwarf(name)
    elif class_choice == '5':
        return Knight(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)


def _print_separator():
    print('\n' + '-' * 40 + '\n')


def battle(player, wizard):
    print(f"\nA wild {wizard.name} appears! Prepare for battle, {player.name}!")

    while wizard.health > 0 and player.health > 0:
        _print_separator()
        print("--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = input("Choose an action: ").strip()
        # helper to choose a minion target when minions are present
        def choose_minion_target():
            alive = [m for m in wizard.minions if m.health > 0]
            if not alive:
                return None
            print("Choose a minion to target:")
            for idx, m in enumerate(alive, start=1):
                print(f"{idx}. {m.name} (HP: {m.health}/{m.max_health})")
            while True:
                sel = input("Enter minion number: ").strip()
                if not sel.isdigit():
                    print("Please enter a number.")
                    continue
                seln = int(sel)
                if 1 <= seln <= len(alive):
                    return alive[seln-1]
                print("Invalid selection.")

        if choice == '1':
            # Attack: if minions present, must target a single minion
            if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
                target = choose_minion_target()
                if target:
                    player.attack(target)
            else:
                player.attack(wizard)
        elif choice == '2':
            # Use special abilities; target minions if present when ability requires an opponent
            if isinstance(player, Warrior):
                print("1. Heavy Strike\n2. Rally")
                sub = input("Choose ability: ").strip()
                if sub == '1':
                    target = None
                    if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
                        target = choose_minion_target()
                    else:
                        target = wizard
                    if target:
                        player.heavy_strike(target)
                elif sub == '2':
                    player.rally()
                else:
                    print("Invalid ability choice.")
            elif isinstance(player, Mage):
                print("1. Fireball\n2. Mana Shield")
                sub = input("Choose ability: ").strip()
                if sub == '1':
                    target = None
                    if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
                        target = choose_minion_target()
                    else:
                        target = wizard
                    if target:
                        player.fireball(target)
                elif sub == '2':
                    player.mana_shield()
                else:
                    print("Invalid ability choice.")
            elif isinstance(player, Archer):
                print("1. Quick Shot\n2. Evade")
                sub = input("Choose ability: ").strip()
                if sub == '1':
                    target = None
                    if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
                        target = choose_minion_target()
                    else:
                        target = wizard
                    if target:
                        player.quick_shot(target)
                elif sub == '2':
                    player.evade()
                else:
                    print("Invalid ability choice.")
            elif isinstance(player, Dwarf):
                print("1. War Axe\n2. Divine Shield")
                sub = input("Choose ability: ").strip()
                if sub == '1':
                    target = None
                    if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
                        target = choose_minion_target()
                    else:
                        target = wizard
                    if target:
                        player.war_axe(target)
                elif sub == '2':
                    player.divine_shield()
                else:
                    print("Invalid ability choice.")
            elif isinstance(player, Knight):
                print("1. Long Sword\n2. Shield Stance")
                sub = input("Choose ability: ").strip()
                if sub == '1':
                    target = None
                    if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
                        target = choose_minion_target()
                    else:
                        target = wizard
                    if target:
                        player.long_sword(target)
                elif sub == '2':
                    player.shield_stance()
                else:
                    print("Invalid ability choice.")
            else:
                print("You have no special abilities.")
        elif choice == '3':
            player.heal()
        elif choice == '4':
            player.display_stats()
        else:
            print("Invalid choice. Try again.")

        # After player's action: remove any dead minions
        if getattr(wizard, 'minions', None):
            alive = [m for m in wizard.minions if m.health > 0]
            if len(alive) != len(wizard.minions):
                dead_count = len(wizard.minions) - len(alive)
                wizard.minions = alive
                print(f"{dead_count} minion(s) have been destroyed!")

        # If wizard defeated by player's action
        if wizard.health <= 0:
            break

        # If wizard drops below 25 HP and hasn't summoned, summon minions
        if wizard.health > 0 and wizard.health < 25 and not getattr(wizard, 'summoned', False):
            wizard.summon_minions()

        # Wizard turn: if minions exist then wizard only regenerates and minions attack
        print("\n--- Wizard's Turn ---")
        if getattr(wizard, 'minions', []) and any(m.health > 0 for m in wizard.minions):
            wizard.regenerate()
            # minions attack
            for m in list(wizard.minions):
                if m.health > 0:
                    m.attack(player)
                    if player.health <= 0:
                        break
        else:
            # normal behavior: wizard regenerates and attacks
            wizard.regenerate()
            if wizard.health > 0:
                wizard.attack(player)

        # Show health status
        print(f"\n{player.name}: {player.health}/{player.max_health} HP")
        print(f"{wizard.name}: {wizard.health}/{wizard.max_health} HP")

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    _print_separator()
    if wizard.health <= 0 and player.health > 0:
        print(f"Victory! {player.name} has defeated the wicked {wizard.name}!")
    elif player.health <= 0:
        print(f"Defeat... {wizard.name} has triumphed over {player.name}.")
    else:
        print("The battle ends inconclusively.")


def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)


if __name__ == "__main__":
    main()
