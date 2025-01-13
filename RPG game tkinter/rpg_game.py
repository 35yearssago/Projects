import tkinter as tk
from tkinter import messagebox
import random
import datetime


class Player:
    def __init__(self, main_stat, secondary_stat):
        self.stats = {
            "Strength": 10,
            "Dexterity": 10,
            "Intelligence": 10,
            "Charisma": 10
        }
        self.stats[main_stat] += 2
        self.stats[secondary_stat] += 1
        self.title_xp = 0
        self.stat_xp = {
            "Strength": 0,
            "Dexterity": 0,
            "Intelligence": 0,
            "Charisma": 0
        }
        self.penalties = []
        self.current_main_quest = None
        self.main_quest_start = None
        self.daily_quests = []
        self.side_quests = []
        self.hidden_quest = None
        self.system_penalty = False
        self.initialize_system_quests()

    def initialize_system_quests(self):
        self.system_quests = {
            "Fall asleep by 2 AM": False,
            "Wake up before 10 AM": False
        }

    def check_system_quests(self, current_time):
        if current_time.hour >= 2:
            hours_after_2am = current_time.hour - 2
            self.apply_penalty(hours_after_2am)

        if current_time.hour >= 10:
            hours_after_10am = current_time.hour - 10
            self.apply_penalty(hours_after_10am)

    def apply_penalty(self, hours):
        self.title_xp -= hours
        self.system_penalty = True
        penalty_options = ["No entertainment", "No Smoking", "No Music"]
        penalty = random.choice(penalty_options)
        self.penalties.append(penalty)
        print(f"Penalty applied: {penalty} for 24 hours")

    def start_main_quest(self, quest, days):
        if self.current_main_quest:
            print("Finish current Main Quest before starting a new one.")
            return

        self.current_main_quest = quest
        self.main_quest_start = datetime.datetime.now()
        self.main_quest_duration = days
        print(f"Started Main Quest: {quest} for {days} days")

    def complete_main_quest(self):
        if not self.current_main_quest:
            print("No active Main Quest to complete.")
            return

        days_taken = (datetime.datetime.now() - self.main_quest_start).days
        if days_taken > self.main_quest_duration:
            self.title_xp -= days_taken
            print(f"Failed Main Quest: {self.current_main_quest}. Lost {days_taken} XP.")

        else:
            xp_reward = min(self.main_quest_duration * 2, 30)
            self.title_xp += xp_reward
            self.stat_xp[self.current_main_quest] += xp_reward
            print(f"Completed Main Quest: {self.current_main_quest}. Gained {xp_reward} XP.")

        self.current_main_quest = None
        self.main_quest_start = None

    def add_daily_quest(self, quest, stat):
        if len(self.daily_quests) >= 5:
            print("Cannot add more than 5 Daily Quests.")
            return
        self.daily_quests.append((quest, stat))

    def complete_daily_quest(self, quest):
        for q in self.daily_quests:
            if q[0] == quest:
                self.title_xp += 1
                self.stat_xp[q[1]] += 1
                self.daily_quests.remove(q)
                print(f"Completed Daily Quest: {quest}. Gained 1 XP.")
                return
        print("Daily Quest not found.")

    def add_side_quest(self, quest, stat):
        if len(self.side_quests) >= 2:
            print("Cannot add more than 2 Side Quests.")
            return
        self.side_quests.append((quest, stat))

    def complete_side_quest(self, quest):
        for q in self.side_quests:
            if q[0] == quest:
                self.title_xp += 2
                self.stat_xp[q[1]] += 2
                self.side_quests.remove(q)
                print(f"Completed Side Quest: {quest}. Gained 2 XP.")
                return
        print("Side Quest not found.")

    def add_hidden_quest(self, quest):
        if self.hidden_quest:
            print("Cannot have more than one Hidden Quest at a time.")
            return
        self.hidden_quest = quest

    def complete_hidden_quest(self):
        if not self.hidden_quest:
            print("No active Hidden Quest to complete.")
            return
        self.title_xp += 15
        print(f"Completed Hidden Quest: {self.hidden_quest}. Gained 15 XP.")
        self.hidden_quest = None

    def show_stats(self):
        stats = "\nPlayer Stats:\n"
        for stat, value in self.stats.items():
            stat_points = self.stat_xp[stat] // 20
            stats += f"{stat}: {value + stat_points} (XP: {self.stat_xp[stat]})\n"
        stats += f"Title XP: {self.title_xp}"
        return stats

    def get_title(self):
        if self.title_xp >= 5000:
            return "Incomprehensible Omnipotent Being"
        elif self.title_xp >= 2500:
            return "Ascended"
        elif self.title_xp >= 1500:
            return "Overlord"
        elif self.title_xp >= 1000:
            return "Holder of the Reality Cheat Codes"
        elif self.title_xp >= 750:
            return "CEO of Leveling"
        elif self.title_xp >= 500:
            return "Something normal"
        elif self.title_xp >= 350:
            return "Platinum"
        elif self.title_xp >= 200:
            return "Gold"
        elif self.title_xp >= 100:
            return "Silver"
        else:
            return "Bronze"

    def show_title(self):
        return f"Current Title: {self.get_title()}"


class QuestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quest System")

        self.player = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20)

        self.create_character_frame()

    def create_character_frame(self):
        self.character_frame = tk.Frame(self.main_frame)
        self.character_frame.pack()

        tk.Label(self.character_frame, text="Choose Main Stat:").grid(row=0, column=0)
        self.main_stat = tk.StringVar(value="Intelligence")
        tk.OptionMenu(self.character_frame, self.main_stat, "Strength", "Dexterity", "Intelligence", "Charisma").grid(
            row=0, column=1)

        tk.Label(self.character_frame, text="Choose Secondary Stat:").grid(row=1, column=0)
        self.secondary_stat = tk.StringVar(value="Charisma")
        tk.OptionMenu(self.character_frame, self.secondary_stat, "Strength", "Dexterity", "Intelligence",
                      "Charisma").grid(row=1, column=1)

        tk.Button(self.character_frame, text="Create Character", command=self.create_character).grid(row=2,
                                                                                                     columnspan=2,
                                                                                                     pady=10)

    def create_character(self):
        main_stat = self.main_stat.get()
        secondary_stat = self.secondary_stat.get()

        if main_stat == secondary_stat:
            messagebox.showerror("Error", "Main and Secondary stats must be different!")
            return

        self.player = Player(main_stat, secondary_stat)

        self.character_frame.pack_forget()
        self.create_quest_frame()

    def create_quest_frame(self):
        self.quest_frame = tk.Frame(self.main_frame)
        self.quest_frame.pack()

        self.quest_title = tk.Label(self.quest_frame, text=self.player.show_title(), font=("Arial", 16))
        self.quest_title.grid(row=0, columnspan=2)

        self.stats_label = tk.Label(self.quest_frame, text=self.player.show_stats(), justify="left")
        self.stats_label.grid(row=1, columnspan=2, pady=10)

        self.main_quest_frame = tk.Frame(self.quest_frame)
        self.main_quest_frame.grid(row=2, columnspan=2)

        tk.Label(self.main_quest_frame, text="Main Quest:").grid(row=0, column=0)
        self.main_quest_entry = tk.Entry(self.main_quest_frame)
        self.main_quest_entry.grid(row=0, column=1)
        tk.Label(self.main_quest_frame, text="Days:").grid(row=1, column=0)
        self.main_quest_days = tk.Entry(self.main_quest_frame)
        self.main_quest_days.grid(row=1, column=1)
        tk.Button(self.main_quest_frame, text="Start Main Quest", command=self.start_main_quest).grid(row=2,
                                                                                                      columnspan=2)

        self.daily_quest_frame = tk.Frame(self.quest_frame)
        self.daily_quest_frame.grid(row=3, columnspan=2, pady=10)

        tk.Label(self.daily_quest_frame, text="Daily Quest:").grid(row=0, column=0)
        self.daily_quest_entry = tk.Entry(self.daily_quest_frame)
        self.daily_quest_entry.grid(row=0, column=1)
        tk.Label(self.daily_quest_frame, text="Stat:").grid(row=1, column=0)
        self.daily_quest_stat = tk.StringVar(value="Intelligence")
        tk.OptionMenu(self.daily_quest_frame, self.daily_quest_stat, "Strength", "Dexterity", "Intelligence",
                      "Charisma").grid(row=1, column=1)
        tk.Button(self.daily_quest_frame, text="Add Daily Quest", command=self.add_daily_quest).grid(row=2,
                                                                                                     columnspan=2)
        tk.Button(self.daily_quest_frame, text="Complete Daily Quest", command=self.complete_daily_quest).grid(row=3,
                                                                                                               columnspan=2)

        self.side_quest_frame = tk.Frame(self.quest_frame)
        self.side_quest_frame.grid(row=4, columnspan=2, pady=10)

        tk.Label(self.side_quest_frame, text="Side Quest:").grid(row=0, column=0)
        self.side_quest_entry = tk.Entry(self.side_quest_frame)
        self.side_quest_entry.grid(row=0, column=1)
        tk.Label(self.side_quest_frame, text="Stat:").grid(row=1, column=0)
        self.side_quest_stat = tk.StringVar(value="Intelligence")
        tk.OptionMenu(self.side_quest_frame, self.side_quest_stat, "Strength", "Dexterity", "Intelligence",
                      "Charisma").grid(row=1, column=1)
        tk.Button(self.side_quest_frame, text="Add Side Quest", command=self.add_side_quest).grid(row=2, columnspan=2)
        tk.Button(self.side_quest_frame, text="Complete Side Quest", command=self.complete_side_quest).grid(row=3,
                                                                                                            columnspan=2)

        self.hidden_quest_frame = tk.Frame(self.quest_frame)
        self.hidden_quest_frame.grid(row=5, columnspan=2, pady=10)

        tk.Label(self.hidden_quest_frame, text="Hidden Quest:").grid(row=0, column=0)
        self.hidden_quest_entry = tk.Entry(self.hidden_quest_frame)
        self.hidden_quest_entry.grid(row=0, column=1)
        tk.Button(self.hidden_quest_frame, text="Add Hidden Quest", command=self.add_hidden_quest).grid(row=1,
                                                                                                        columnspan=2)
        tk.Button(self.hidden_quest_frame, text="Complete Hidden Quest", command=self.complete_hidden_quest).grid(row=2,
                                                                                                                  columnspan=2)

        tk.Button(self.quest_frame, text="Show Stats", command=self.update_stats).grid(row=6, columnspan=2, pady=10)

    def start_main_quest(self):
        quest = self.main_quest_entry.get()
        days = int(self.main_quest_days.get())
        self.player.start_main_quest(quest, days)
        self.update_stats()

    def add_daily_quest(self):
        quest = self.daily_quest_entry.get()
        stat = self.daily_quest_stat.get()
        self.player.add_daily_quest(quest, stat)
        self.update_stats()

    def complete_daily_quest(self):
        quest = self.daily_quest_entry.get()
        self.player.complete_daily_quest(quest)
        self.update_stats()

    def add_side_quest(self):
        quest = self.side_quest_entry.get()
        stat = self.side_quest_stat.get()
        self.player.add_side_quest(quest, stat)
        self.update_stats()

    def complete_side_quest(self):
        quest = self.side_quest_entry.get()
        self.player.complete_side_quest(quest)
        self.update_stats()

    def add_hidden_quest(self):
        quest = self.hidden_quest_entry.get()
        self.player.add_hidden_quest(quest)
        self.update_stats()

    def complete_hidden_quest(self):
        self.player.complete_hidden_quest()
        self.update_stats()

    def update_stats(self):
        self.stats_label.config(text=self.player.show_stats())
        self.quest_title.config(text=self.player.show_title())


root = tk.Tk()
app = QuestApp(root)
root.mainloop()
