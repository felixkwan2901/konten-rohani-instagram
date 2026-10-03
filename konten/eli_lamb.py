"""@eliandruthie (dulu @sahabat.eli) -> Eli the Lamb: domba kecil fotorealistik (gambar AI) yang hidup sehari-hari di New Zealand.
Bahasa Inggris. Humor relatable NZ (PAK'nSAVE, cuaca, macet Auckland, dairy, pie, jandals...).
Rohani hanya 1x seminggu: hari Minggu pagi. Pasangan: Ruthie (domba coklat karamel), untuk konten suami-istri. 3 post/hari (07:00, 12:00, 20:00 NZ), malam = Reels (zoom pelan + musik).

Gambar dibuat di Gemini/ChatGPT dari foto referensi Eli, lalu disimpan sebagai
output/eli_lamb/raw/<id>.jpg (atau .png), misalnya output/eli_lamb/raw/1-pagi.jpg.
Teks meme, handle & musik ditambahkan otomatis oleh eli_lamb.py (jangan minta AI menulis teks di gambar).
Merek (PAK'nSAVE, The Warehouse, Bunnings) hanya disebut di teks; di prompt pakai deskripsi umum tanpa logo."""

CHARACTER = ("Photorealistic fluffy white baby lamb named Eli, standing or sitting upright like a person, big gentle dark eyes, "
             "soft cream curly wool, small pink nose, slightly chubby, wholesome and funny expression, realistic fur detail, "
             "natural lighting, shot on a 50mm lens, Instagram photo, no text, no logos")

PARTNER = ("Ruthie, Eli's wife: a photorealistic fluffy caramel-brown lamb, standing or sitting upright like a person, "
           "long eyelashes, big warm brown eyes, soft light-brown curly wool, a small pastel flower tucked behind one ear, "
           "sassy but sweet expression, same realistic style and size as Eli, no text, no logos")
COUPLE = ("Two photorealistic lambs as a married couple: Eli (fluffy WHITE lamb, big gentle dark eyes) and his wife Ruthie "
          "(fluffy CARAMEL-BROWN lamb with long eyelashes and a small pastel flower behind one ear), upright like people, "
          "realistic fur, natural lighting, 50mm lens, Instagram photo, no text, no logos")

TAGS = "#newzealand #nzlife #kiwi #kiwilife #aotearoa #funnyanimals #lamb #relatable #elithelamb"
FAITH_TAGS = "#newzealand #kiwi #sundayvibes #faith #psalm23 #goodshepherd #lamb #elithelamb"

# (hari, slot, teks meme, adegan untuk prompt gambar, caption)
_DATA = [
    # Minggu 4 Okt
    (1, "pagi", "Sheep don't stress about tomorrow's grass.\nThe Shepherd's got it covered.",
     "Eli sitting peacefully on a green New Zealand hillside at sunrise, other sheep grazing behind, soft golden light, calm and peaceful",
     "Sunday reminder 🐑🤍\n\n“The LORD is my shepherd; I shall not want.” — Psalm 23:1 (KJV)\n\nWhatever this week brings, you're looked after.", True),
    (1, "pagi2", "Went to PAK'nSAVE for milk.\nCame out with 4kg of chicken, a pillow and a garden hose.",
     "Eli pushing an overflowing shopping trolley out of a big discount supermarket with yellow signage, trolley full of chicken, a pillow and a garden hose, car park, overcast NZ day",
     "Every. Single. Time. 🛒😅\n\nWhat's the most random thing you've walked out with?", False),
    (1, "malam", "Sunday night me realising\ntomorrow is Monday again.",
     "Eli lying on a couch under a blanket at night staring at the ceiling with a worried face, cosy living room, lamp light",
     "The Sunday scaries are real 😩\n\nTag someone who feels this.", False),
    # Senin 5 Okt
    (2, "pagi", "Auckland traffic:\nleave at 7:00, arrive at 7:00…\nnext week.",
     "Eli behind the wheel of a small hatchback stuck in a long motorway traffic jam in the morning, looking bored, city skyline in the distance",
     "Southern Motorway, is that you? 🚗🐌\n\nHow long was your commute today?", False),
    (2, "pagi2", "Lunch budget: $5.\nThe pie at the dairy: $5.50.",
     "Eli at the counter of a small New Zealand corner dairy shop, looking shocked at the price of a mince and cheese pie in a warmer cabinet",
     "When did pies get so expensive?? 🥧😭\n\nMince & cheese or steak & cheese? Comment below 👇", False),
    (2, "malam", "Me turning the heater on for 5 minutes.\nThe power bill:",
     "Eli wrapped in three blankets holding a power bill with a horrified face, small heater glowing beside, cold NZ house at night",
     "Kiwi winter things ❄️⚡\n\nWho else wears a hoodie inside instead? 🙋", False),
    # Selasa 6 Okt
    (3, "pagi", "NZ weather:\n4 seasons before morning tea.",
     "Eli standing on a windy street wearing sunglasses, a beanie, a raincoat and holding an umbrella turned inside out by the wind, sun and rain at the same time",
     "Sunscreen AND a raincoat. Every day. ☀️🌧️🌬️\n\nWhat's the weather doing where you are?", False),
    (3, "pagi2", "NZ: about 5 million people.\nAlso NZ: about 24 million sheep.\nWe run this place.",
     "Eli standing confidently at the front of a huge flock of sheep on a country road, like a boss, rolling green hills behind",
     "Just saying 😎🐑\n\nFollow for more sheep facts (and sheep opinions).", False),
    (3, "malam", "Me watching the rugby:\n“I'm not stressed.”",
     "Eli on a couch in front of a TV showing a rugby match, clutching a cushion, wide eyes, very stressed, snacks everywhere",
     "Calm. Totally calm. 🏉😬\n\nWho's watching this weekend?", False),
    # Rabu 7 Okt
    (4, "pagi", "I don't need coffee.\nI need a flat white.\nThat's different.",
     "Eli at a cosy café counter holding a flat white with latte art, looking serious and sleepy, morning light",
     "Very different. ☕🐑\n\nWhat's your café order?", False),
    (4, "pagi2", "Went to the hardware store for one screw.\nLeft with a sausage in bread and 3 plants.",
     "Eli outside a big hardware store at a sausage sizzle stand, holding a sausage in white bread with tomato sauce and carrying three potted plants",
     "The sausage sizzle gets me every time 🌭🪴\n\nOnions on top or under?", False),
    (4, "malam", "Wednesday: halfway there.\nThe laundry: not even close.",
     "Eli sitting next to a giant mountain of unfolded laundry on a bed, looking defeated, evening light",
     "Halfway through the week, zero percent through the washing 🧺\n\nTag your laundry buddy.", False),
    # Kamis 8 Okt
    (5, "pagi", "Kiwis at 8°C: jandals and shorts.\nTourists: full winter gear.",
     "Eli in shorts and jandals on a frosty morning next to a tourist wrapped in a thick puffer jacket, scarf and gloves, NZ street",
     "Jandals are a lifestyle, not a season 🩴\n\nWho else wears them all year?", False),
    (5, "pagi2", "Me: I'll just grab one thing.\nThe Warehouse:",
     "Eli in a big red discount department store aisle carrying an armful of random items, cushions, snacks, a lamp, looking surprised",
     "One thing. That was the plan. 🛍️\n\nWhat's always in your basket?", False),
    (5, "malam", "Pavlova is from New Zealand.\nI will not be taking questions.",
     "Eli proudly holding a big pavlova with kiwifruit and strawberries on top, sitting at a table, determined face, warm kitchen light",
     "Say what you want, Australia 😤🍓\n\nPav at Christmas: yes or YES?", False),
    # Jumat 9 Okt
    (6, "pagi", "Road trip across NZ:\n10% driving\n90% road cones.",
     "Eli driving on a scenic New Zealand road completely surrounded by hundreds of orange road cones, mountains in the background",
     "The cones are part of the landscape now 🚧😂\n\nWhere's your favourite road trip?", False),
    (6, "pagi2", "Friday fish & chips at the beach.\nThe seagulls: “We're a family now.”",
     "Eli sitting on a beach holding fish and chips wrapped in paper, surrounded by several seagulls staring at the chips, sunny NZ beach",
     "Never make eye contact with them 🐟🍟\n\nWho else guards their chips like treasure?", False),
    (6, "malam", "Friday night plans:\ncouch, blanket, chips,\nasleep by 9:30.",
     "Eli asleep on a couch with a blanket and a bag of chips, TV still on, cosy living room, night",
     "Living my best life 😴\n\nWhat are your Friday night plans?", False),
    # Sabtu 10 Okt
    (7, "pagi", "Saturday farmers market:\n$9 for one fancy tomato.\nWorth it.",
     "Eli at a sunny outdoor farmers market stall holding one big heirloom tomato with pride, baskets of vegetables around",
     "Treat yourself 🍅✨\n\nWhat's your must-buy at the market?", False),
    (7, "pagi2", "Tramping in NZ:\nviews 10/10\nsandflies 0/10.",
     "Eli on a scenic hiking track by a lake with mountains, wearing a tiny backpack, swatting at little bugs, beautiful view",
     "Worth it. Mostly. 🏔️🦟\n\nWhat's your favourite walk?", False),
    (7, "malam", "Picking my Sunday outfit tonight\nlike it's the first day of school.",
     "Eli standing in front of a wardrobe holding up two little outfits, choosing carefully, bedroom at night, excited face",
     "See you at church tomorrow? 😄👔\n\nWhat time is your Sunday service?", False),
]

# versi pasangan (Eli & Ruthie) untuk beberapa post: (hari, slot) -> (teks, adegan, caption)
COUPLE_POSTS = {
    (1, 'pagi2'): ("Me: we're only getting milk.\nHer: grabs the biggest trolley.",
        'Ruthie happily pushing a giant shopping trolley into a big discount supermarket with yellow signage while Eli walks behind holding one bottle of milk, looking worried, car park',
        "Every PAK'nSAVE trip ever 🛒😅\n\nTag the one who always grabs the trolley."),
    (2, 'malam'): ("Her: it's freezing.\nMe: put on a jumper.\nHer: turns the heater to 28.",
        'Ruthie wrapped in a blanket turning up a heater with a satisfied smile, Eli beside her in a jumper holding the power bill with a horrified face, cosy NZ lounge at night',
        'Every Kiwi winter argument ❄️⚡\n\nTeam jumper or team heater?'),
    (3, 'malam'): ("Her: it's just a game.\nMe during the rugby:",
        'Eli on the couch clutching a cushion, screaming at a TV showing a rugby match, Ruthie next to him calmly sipping tea and rolling her eyes, snacks everywhere',
        "It's NOT just a game 🏉😤\n\nTag your rugby-watching partner."),
    (4, 'malam'): ("Him: I'll fold it later.\nThe laundry, 3 weeks later:",
        'Ruthie with hands on hips staring at Eli, who is buried under a giant mountain of unfolded laundry on the bed with only his face showing, evening light',
        "“Later” is a very flexible word 🧺😂\n\nWho's the folder in your house?"),
    (5, 'pagi2'): ("Her: I'm just grabbing one thing.\nThe trolley 40 minutes later:",
        'Ruthie happily pushing an overflowing trolley full of cushions, candles, snacks and a lamp in a big red discount store aisle, Eli following with a tired face',
        "One thing. That was the plan. 🛍️\n\nWhat's always in your basket?"),
    (6, 'pagi2'): ("Her: I'm not hungry.\nAlso her: eats half my chips.",
        "Eli and Ruthie sitting on a beach bench, Ruthie sneakily eating chips from Eli's fish and chips paper while he looks at her in disbelief, seagulls watching, sunny NZ beach",
        'Every. Single. Time. 🍟😂\n\nTag the chip thief in your life.'),
    (6, 'malam'): ('Date night before marriage: dinner out.\nDate night now: couch, blanket,\nasleep by 9:30.',
        'Eli and Ruthie asleep together on a couch under one blanket, a bag of chips and the TV still on, cosy living room at night',
        'Honestly? Best date ever 😴💕\n\nWhat does date night look like for you?'),
    (7, 'pagi'): ("Her: we don't need anything.\nAlso her: $64 of fancy cheese.",
        'Ruthie at a sunny outdoor farmers market stall holding several blocks of fancy cheese and a jar of honey, Eli holding the wallet with a shocked face',
        "Farmers market math 🧀💸\n\nWhat's your must-buy at the market?"),
    (7, 'malam'): ('Her: which outfit, this one or this one?\nMe: the first one.\nHer: wears the third one.',
        'Ruthie in front of a wardrobe holding up two little dresses with three more on the bed, Eli sitting on the bed looking confused, bedroom at night',
        'Getting ready for church tomorrow 😄👗\n\nSee you Sunday? What time is your service?'),
}

# ---------- minggu 2: Minggu 11 - Sabtu 17 Okt (hari 8-14) ----------
# (hari, slot, pasangan?, teks meme, adegan, caption, rohani?)
_DATA2 = [
    (8, "pagi", True, "When life feels like too much,\nremember who carries the lambs.",
     "Eli and Ruthie sitting peacefully together in a green spring paddock full of daisies, soft morning light, calm and content",
     "Sunday reminder 🐑🤍\n\n“He shall gather the lambs with his arm, and carry them in his bosom.” — Isaiah 40:11 (KJV)\n\nYou don't have to carry this week alone.", True),
    (8, "pagi2", False, "Daylight saving:\nlost one hour of sleep.\nStill looking for it.",
     "Eli in bed under a duvet squinting at a ringing alarm clock, messy wool, sunlight through curtains, very sleepy",
     "Is it just me or does it take a whole week to recover? 😴⏰\n\nWho else is still tired?", False),
    (8, "malam", True, "Us after Sunday lunch:\n“Let's be productive this afternoon.”\nAlso us:",
     "Eli and Ruthie fast asleep on a couch at 2pm with empty plates on the coffee table, sunny living room",
     "Sunday naps are a spiritual discipline, right? 😅\n\nTag your nap partner.", False),
    (9, "pagi", False, "Kiwis at the supermarket:\nno shoes, no problem.",
     "Eli walking barefoot down a supermarket aisle holding a shopping basket, relaxed and confident, other shoppers blurred",
     "Bare feet at the supermarket is a Kiwi right 🦶🛒\n\nBe honest: have you done it?", False),
    (9, "pagi2", True, "Her: let's eat healthy this week.\nAlso her at 9pm:",
     "Ruthie in a cosy kitchen at night eating hokey pokey ice cream straight from a big tub with a spoon, Eli standing behind her holding a salad, surprised",
     "Healthy starts tomorrow. Every day. 🍨😂\n\nHokey pokey or cookies & cream?", False),
    (9, "malam", False, "Spring in NZ: baby lambs everywhere.\nMe: finally, my people.",
     "Eli leaning on a wooden farm fence proudly watching a paddock full of tiny newborn lambs in spring, golden evening light, green hills",
     "Lambing season is the best season 🐑🌸\n\nFollow for more lamb life.", False),
    (10, "pagi", False, "NZ roundabouts:\neveryone waiting for everyone.",
     "Eli in a small car at a suburban roundabout, politely waving another car through while all the other cars are also stopped and waving, sunny morning",
     "After you. No, after YOU. 🚗🔄\n\nKiwi politeness at its finest.", False),
    (10, "pagi2", True, "Her: I got a trim.\nMe, who can't see any difference:\n“Wow, it looks amazing!”",
     "Ruthie at a hair salon admiring her freshly trimmed caramel wool in the mirror, Eli standing next to her giving an enthusiastic thumbs up with a nervous smile",
     "Husband survival tip #1 💇‍♀️😅\n\nTag someone who needs this advice.", False),
    (10, "malam", False, "Tuesday dinner: mince, again.\nThe mince: “see you tomorrow.”",
     "Eli standing at a stove stirring a big pan of mince with a tired face, simple home kitchen at night",
     "Mince and cheese, mince on toast, mince pasta… 🍝😂\n\nWhat's your go-to weeknight dinner?", False),
    (11, "pagi", False, "When someone says “yeah nah”\nand you know exactly what they mean.",
     "Eli chatting with an older sheep friend over a wooden fence in the countryside, Eli nodding knowingly, morning light",
     "Kiwi is a language of its own 🇳🇿😄\n\nComment your favourite Kiwi phrase 👇", False),
    (11, "pagi2", True, "Our love language:\nsending each other videos\nwhile sitting on the same couch.",
     "Eli and Ruthie sitting side by side on a couch, both laughing at their phones, cosy living room",
     "Romance is not dead 📱💕\n\nTag the person you send videos to.", False),
    (11, "malam", False, "Me at the op shop: “I don't need anything.”\nAlso me:",
     "Eli in a second-hand op shop happily holding up a quirky lamp shaped like a duck, shelves of vintage items behind",
     "Op shop finds hit different 🦆💡\n\nWhat's your best op shop find?", False),
    (12, "pagi", True, "Me: I'll cook tonight.\nThe smoke alarm:",
     "Eli in a smoky kitchen holding a burnt pan with an innocent face while Ruthie waves a tea towel at the ceiling smoke alarm, evening",
     "It's called flavour 🔥😂\n\nWho's the cook in your house?", False),
    (12, "pagi2", False, "Kiwi BBQ rule:\n“She'll be right.”\nThe sausages:",
     "Eli at a backyard barbecue calmly holding tongs while sausages on the grill are very burnt and smoking, sunny backyard",
     "She'll be right… probably 🌭🔥\n\nTomato sauce or mustard?", False),
    (12, "malam", True, "Choosing what to watch: 45 minutes.\nWatching it: 10 minutes\nbefore we fall asleep.",
     "Eli and Ruthie on a couch under a blanket at night, Eli holding a TV remote scrolling endlessly, Ruthie already half asleep on his shoulder",
     "Every. Single. Night. 📺😴\n\nWhat are you watching right now?", False),
    (13, "pagi", False, "Friday morning me:\nMonday me could never.",
     "Eli happily dancing in the kitchen in the morning holding a coffee mug, sunlight streaming in, joyful expression",
     "Friday energy is unmatched 🕺☕\n\nWhat are your weekend plans?", False),
    (13, "pagi2", True, "Packing for the weekend away:\nher: 3 suitcases.\nme: one jandal.",
     "Ruthie standing next to a car boot packed with three big suitcases, Eli next to her proudly holding a single jandal, driveway, sunny day",
     "I'll find the other one there 🩴🧳\n\nOverpacker or underpacker?", False),
    (13, "malam", False, "Friday takeaways:\n“I'll just have a small.”\nAlso me:",
     "Eli at a table surrounded by lots of takeaway boxes, burgers, chips and noodles, looking very happy, Friday night",
     "Small is a state of mind 🍔🍟\n\nWhat's your Friday night takeaway?", False),
    (14, "pagi", False, "Everyone: mowing the lawn on Saturday.\nMe, a sheep:",
     "Eli happily munching the long grass of a suburban backyard lawn while a lawn mower sits unused next to him, sunny Saturday morning",
     "Work smarter, not harder 🐑🌱\n\nWho's mowing the lawn today?", False),
    (14, "pagi2", True, "Her: “It's only a 2-hour walk.”\nThe track: 6 hours, all uphill.",
     "Ruthie cheerfully hiking up a steep scenic New Zealand track with a small backpack while Eli behind her is exhausted and sweaty, mountains and lake in the distance",
     "The views were worth it. My legs disagree. 🏔️😮‍💨\n\nWhat's your favourite NZ walk?", False),
    (14, "malam", True, "Setting 3 alarms for church tomorrow\nbecause we know ourselves.",
     "Eli and Ruthie sitting in bed at night both setting alarms on their phones, a bedside lamp on, church clothes hanging ready on the wardrobe",
     "See you at church tomorrow! ⛪😄\n\nMorning service or evening service?", False),
]

# posisi teks manual kalau otomatis masih menutupi wajah
POSISI = {"10-malam": "kanan-bawah", "16-malam": "kiri-bawah"}

# post yang kotak teksnya di bawah (wajah karakter ada di atas gambar)
TEKS_BAWAH = {"2-malam", "3-pagi2", "3-malam", "4-pagi2", "4-malam", "5-pagi", "5-pagi2", "10-pagi2"}

POSTS = []
for hari, slot, teks, adegan, caption, faith in _DATA:
    pasangan = (hari, slot) in COUPLE_POSTS
    if pasangan:
        teks, adegan, caption = COUPLE_POSTS[(hari, slot)]
    POSTS.append({"id": f"{hari}-{slot}", "hari": hari, "slot": slot, "teks": teks, "reel": slot == "malam", "pasangan": pasangan,
                  "prompt": f"{COUPLE if pasangan else CHARACTER}. Scene: {adegan}.",
                  "caption": caption + "\n\nFollow @{handle} for more 🐑\n.\n.\n" + (FAITH_TAGS if faith else TAGS)})
for hari, slot, pasangan, teks, adegan, caption, faith in _DATA2:
    POSTS.append({"id": f"{hari}-{slot}", "hari": hari, "slot": slot, "teks": teks, "reel": slot == "malam", "pasangan": pasangan,
                  "prompt": f"{COUPLE if pasangan else CHARACTER}. Scene: {adegan}.",
                  "caption": caption + "\n\nFollow @{handle} for more 🐑\n.\n.\n" + (FAITH_TAGS if faith else TAGS)})


STYLE = ("Photorealistic characters in the same knitted-wool, Pixar-like style as Eli and Ruthie, realistic lighting, "
         "50mm lens, Instagram photo, no text, no logos")


def base_for(who, adegan):
    """Deskripsi dasar prompt: hanya karakter yang memang ada di adegan."""
    if who != "friends":
        return {"eli": CHARACTER, "ruthie": PARTNER, "couple": COUPLE}.get(who, COUPLE)
    e, r = "Eli" in adegan, "Ruthie" in adegan
    return COUPLE if e and r else CHARACTER if e else PARTNER if r else STYLE


# ---------- minggu 3-5: Minggu 18 Okt - Sabtu 7 Nov (hari 15-35), dari konten/eli_lamb_w3.py ----------
from konten.eli_lamb_w3 import DATA3, FRIENDS  # noqa: E402

# acara khusus (menggantikan slot di DATA3): Halloween, Movember
EVENTS = {
    (28, "pagi"): ("friends", "Pip's Halloween costume this year:\na wolf.\nGrandpa Ram: “Very funny.”",
                   "Pip in a fluffy grey wolf onesie with little ears, holding a pumpkin lolly bucket at Eli and Ruthie's front door, "
                   "Grandpa Ram standing behind her with an unimpressed face, Eli and Ruthie laughing in the doorway, warm evening light, autumn leaves",
                   "A sheep in wolf's clothing 🐺🐑😂\n\nDo you do Halloween where you live, or just hand out lollies?", False),
    (30, "pagi"): ("eli", "Movember, day 2.\nMe trying to grow a moustache:\nit's just more wool.",
                   "Eli in his navy pom-pom beanie looking very seriously into a bathroom mirror at a tiny fluffy wool moustache, morning light",
                   "Doing my part for men's health 🥸💙\n\nWho's doing Movember this year?", False),
}

for hari, slot, who, teks, adegan, caption, faith in DATA3:
    who, teks, adegan, caption, faith = EVENTS.get((hari, slot), (who, teks, adegan, caption, faith))
    base = base_for(who, adegan)
    extra = " ".join(f"{n}: {d}." for n, d in FRIENDS.items() if n in adegan)
    POSTS.append({"id": f"{hari}-{slot}", "hari": hari, "slot": slot, "teks": teks, "reel": slot == "malam",
                  "pasangan": who in ("couple", "friends"), "who": who,
                  "prompt": f"{base}. {extra} Scene: {adegan}.".replace(". .", "."),
                  "caption": caption + "\n\nFollow @{handle} for more 🐑\n.\n.\n" + (FAITH_TAGS if faith else TAGS)})

# ---------- minggu 6-7: Minggu 8 - Sabtu 21 Nov (hari 36-49), dari konten/eli_lamb_w6.py ----------
from konten.eli_lamb_w6 import DATA6, FRIENDS_NEW  # noqa: E402

ALL_FRIENDS = {**FRIENDS, **FRIENDS_NEW}
for hari, slot, who, teks, adegan, caption, faith in DATA6:
    base = base_for(who, adegan)
    extra = " ".join(f"{n}: {d}." for n, d in ALL_FRIENDS.items() if n in adegan)
    POSTS.append({"id": f"{hari}-{slot}", "hari": hari, "slot": slot, "teks": teks, "reel": slot == "malam",
                  "pasangan": who in ("couple", "friends"), "who": who,
                  "prompt": f"{base}. {extra} Scene: {adegan}.".replace(". .", "."),
                  "caption": caption + "\n\nFollow @{handle} for more 🐑\n.\n.\n" + (FAITH_TAGS if faith else TAGS)})


# ---------- slot tambahan (4/hari minggu 1, 5/hari minggu 2, 8/hari mulai minggu 3) ----------
import importlib  # noqa: E402

for _mod, _var in (("eli_extra_a", "DATA_A"), ("eli_extra_b", "DATA_B"), ("eli_extra_c", "DATA_C")):
    try:
        _data = getattr(importlib.import_module(f"konten.{_mod}"), _var)
    except ModuleNotFoundError:
        continue
    for hari, slot, who, teks, adegan, caption, faith in _data:
        base = base_for(who, adegan)
        extra = " ".join(f"{n}: {d}." for n, d in ALL_FRIENDS.items() if n in adegan)
        POSTS.append({"id": f"{hari}-{slot}", "hari": hari, "slot": slot, "teks": teks, "reel": slot in ("malam", "larut"),
                      "pasangan": who in ("couple", "friends"), "who": who,
                      "prompt": f"{base}. {extra} Scene: {adegan}.".replace(". .", "."),
                      "caption": caption + "\n\nFollow @{handle} for more 🐑\n.\n.\n" + (FAITH_TAGS if faith else TAGS)})

SLOT_ORDER = ["pagi", "pagi3", "siang0", "pagi2", "sore", "sore2", "malam", "larut"]
POSTS.sort(key=lambda p: (p["hari"], SLOT_ORDER.index(p["slot"])))
