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

# post yang kotak teksnya di bawah (wajah karakter ada di atas gambar)
TEKS_BAWAH = {"2-malam"}

POSTS = []
for hari, slot, teks, adegan, caption, faith in _DATA:
    pasangan = (hari, slot) in COUPLE_POSTS
    if pasangan:
        teks, adegan, caption = COUPLE_POSTS[(hari, slot)]
    POSTS.append({"id": f"{hari}-{slot}", "hari": hari, "slot": slot, "teks": teks, "reel": slot == "malam", "pasangan": pasangan,
                  "prompt": f"{COUPLE if pasangan else CHARACTER}. Scene: {adegan}.",
                  "caption": caption + "\n\nFollow @{handle} for more 🐑\n.\n.\n" + (FAITH_TAGS if faith else TAGS)})
