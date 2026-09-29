from chooser import Chooser, Item, UserProfile


items = [
    Item("rust", "Rust systems programming", frozenset({"systems", "security", "performance"}), popularity=80),
    Item("python", "Python automation", frozenset({"automation", "data", "productivity"}), popularity=95),
    Item("ethics", "Responsible AI design", frozenset({"security", "ethics", "governance"}), popularity=60),
]

profile = UserProfile(interests=frozenset({"security", "systems"}))
chooser = Chooser(items)

for choice in chooser.recommend(profile, limit=3, diversity=0.30):
    print(f"{choice.item.title}: {choice.score:.3f} — {', '.join(choice.reasons)}")
