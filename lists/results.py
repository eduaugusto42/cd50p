results = ["Mario", "Luigi", "Princess", "Yoshi", "Toad"]

results.append("Koopa Troopa")
results.append(["Bowser", "Donkey Kong Jr."])
results.remove(["Bowser", "Donkey Kong Jr."])
results.extend(["Bowser", "Donkey Kong Jr."])
results.remove("Bowser")
results.insert(0, "Bowser")
results.reverse()

print(results)