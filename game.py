import random
import time

class Hero:
    def __init__(self):
        self.level = 1
        self.max_hp = 10
        self.hp = self.max_hp
        self.attack = 5 + self.level
        self.defense = 5 + self.level
        self.name = ''
        self.xp = 0

    def name_self(self):
        self.name = raw_input("What do you call yourself, anyway? ")
        if self.name == "":
            self.name_self()

    def heal_self(self):
        amount = self.xp * .2
        self.hp += amount
        print "You attempt to heal yourself..."
        time.sleep(1)
        print "You healed yourself for %d HP, but used half your XP. Feels good, man." % amount
        self.xp *= .5
        self.hp_limit()

    def hp_limit(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def death(self):
        print "Sorry, %s, you is dead now." % (self.name)
        time.sleep(1)
        print "Well, aren't you lucky, there is an afterlife after all."

    def xp_up(self, xp):
        self.xp += xp
        print "You gain: %s XP" % xp

    def look_self(self):
        print ("You are %s, not from around here.") % self.name
        print ("You are level %s with %s attack and %s defense.") % (self.level, self.attack, self.defense)
        print ("You need %s XP to level up.") % (self.level**2 * 10)

class Monster:
    def __init__(self, name):
        self.name = name
        self.hp = random.randint(2,10)
        self.attack = random.randint(2,5)
        self.defense = random.randint(2,5)
        self.xp = random.randint(2,8)

class Room:
    def __init__(self, key):
        self.room_data = {
            "home":{"description":"You're at home. This is where you live, unfortunately.",
                    "exits":["forest"]},
            "forest":{"description":"You're in a dark forest. It's fairly gloomy.",
                    "exits":["home", "lake"]},
            "lake":{"description":"You see a lake circled by rocks. It's too cold to swim.",
                    "exits":["forest","mountain"]},
            "mountain":{"description":"You can see for miles around. Don't fall off.",
                    "exits":["lake"]},
            }
        self.description = self.room_data[key]["description"]
        self.exits = self.room_data[key]["exits"]
        self.name = str(key)
        self.monster_list = {}

class Game:
    def __init__(self):
        self.command_list = ["look","name","fight","heal",'report','move','?']
        self.hero = Hero()
        self.current_room = Room("home")


    def list_commands(self):
        print 'Commands are', ', '.join(self.command_list[:-1]), 'and', self.command_list[-1] + '.'

    def handle_input(self):
        com = raw_input(self.prompt()).lower().split()
        if len(com) < 1:
            print ("Huh?")
        elif com[0] == "fight":
            if len(com) > 1:
                if com[1] in self.current_room.monster_list:
                    self.combat(self.hero, self.current_room.monster_list[com[1]])
            else:
                print "Fight what?"
        elif com[0] == "report":
            self.hero.look_self()
        elif com[0] == "look":
            if len(com) > 1:
                if com[1] in self.current_room.monster_list:
                    self.look_monster(self.current_room.monster_list[com[1]])
                else:
                    print "You don't see that monster."
            else:
                self.look()
        elif com[0] == "move":
            if len(com) > 1:
                self.move(com[1])
            else:
                print "Move where?", "You can exit to: %s" % ', '.join(self.current_room.exits)
        elif com[0] == "name":
            self.hero.name_self()
        elif com[0] == "info":
            self.info()
        elif com[0] == "heal":
            self.hero.heal_self()
        elif com[0] == "?":
            self.list_commands()
        else:
            print ("lol wut")

    def combat(self, attacker, defender):
        attack = int(random.random() * attacker.attack)
        defense = int(random.random() *defender.defense)
        print "Attack: %s vs Defense: %s" % (str(attack), str(defense))
        if attack > defense:
            print "You hit the %s for %s HP." % (defender.name.capitalize(), str(attack))
            defender.hp -= attack
        elif attack == defense:
            print "The attack missed. You feel kind of disappointed."
        else:
            print ("The %s hit you for %s HP and it hurt real bad.") % (defender.name.capitalize(), str(attack))
            self.hero.hp -= attack
        if defender.hp <= 0:
            print "You killed the %s. How sad for the %s's family." % (defender.name.capitalize(), defender.name.capitalize())
            self.hero.xp_up(defender.xp)
            del self.current_room.monster_list[defender.name]

    def level_up(self):
        if self.hero.xp > self.hero.level**2 * 10:
            self.hero.level += 1
            print "You've reached level " + str(self.hero.level)
            self.hero.max_hp += self.hero.level
            self.hero.hp = self.hero.max_hp

    def populate(self):
        for i in range(self.hero.level):
            new_monster = random.choice(["ogre", "orc", "goblin"])
            self.current_room.monster_list[new_monster] = Monster(new_monster)

    def look(self):
        print self.current_room.description
        print "You can exit to: %s" % ', '.join(self.current_room.exits)
        monster_list= []
        for name in self.current_room.monster_list:
            monster_list.append(self.current_room.monster_list[name].name.capitalize())
        if monster_list:
            print "You see: %s" % ', '.join(monster_list)

    def look_monster(self, monster):
        print ("The %s has %s HP, %s attack, %s defense, and is worth %s XP."
            % (monster.name.capitalize(), monster.hp, monster.attack, monster.defense, monster.xp))

    def move(self, exit):
        if exit in self.current_room.exits:
             self.current_room = Room(exit)
             self.populate()
             self.look()
        elif exit == self.current_room.name:
            print ("You're already here.")
        else:
            print ("You can't get there from here.")

    def update(self):
        self.level_up()
        if self.hero.hp <= 0:
            self.hero.death()
            time.sleep(2)
            game = Game()

    def prompt(self):
        return '\n' + self.hero.name + " HP:" + str(int(self.hero.hp)) + " XP:" + str(self.hero.xp) + " >"

    def output(self):
        pass

game = Game()

game.populate()
print ("Welcome, adventurer.")
game.list_commands()
game.hero.name_self()
game.hero.look_self()
game.look()

while True:
    game.handle_input()
    game.update()
    game.output()
