"""@eliandruthie - minggu 3-5: Minggu 18 Okt s/d Sabtu 7 Nov 2026 (hari 15-35), 3 post/hari.
Slot: "pagi" 07:00, "pagi2" 12:00, "malam" 20:00 (malam = Reel). Bahasa Inggris, humor NZ.

Lebih banyak variasi: baju ganti-ganti (rain jacket, gumboots, bush shirt, hi-vis, jersey rugby,
celana pendek & kacamata hitam, baju gereja, piyama, apron, Christmas jumper), plus teman-teman
tetap di FRIENDS (dipakai di +-1/3 post, who="friends", nama teman selalu disebut di adegan).
Eli SELALU pakai navy pom-pom beanie; Ruthie SELALU pakai bunga daisy pink di belakang telinga.

Alur cerita mini:
  - Pip (adik Ruthie) menginap: hari 17-20
  - Kiwi Kev (tetangga kiwi, nokturnal) diperkenalkan hari 19, jaga rumah hari 21
  - Road trip Rotorua (Labour Weekend 24-26 Okt): hari 21-23; Grandpa Ram tanam tomat (tradisi Labour Day)
  - BBQ dengan teman-teman: rencana hari 25, persiapan 26-27, pesta Sabtu 31 Okt (hari 28)
  - Natal mulai muncul minggu 4 (3 post) dan minggu 5 (+-1/4): stok Natal di toko, lagu Natal di
    supermarket, Nana Dot merajut Christmas jumper, daftar Natal, Santa parade, pohutukawa bertunas,
    beli pohon cemara asli terlalu awal.
Rohani hanya 1x/minggu: Minggu pagi (hari 15, 22, 29), ayat KJV dikutip persis.
Tanpa merek di adegan; tanpa teks/tulisan di gambar (teks meme ditambahkan otomatis)."""

FRIENDS = {
    "Grandpa Ram": ("Grandpa Ram, the elderly farmer next door: a photorealistic old ram with thick grey-white curly wool, "
                    "small curled horns, bushy white eyebrows, round wire-rimmed glasses, a brown tweed flat cap and a tweed "
                    "waistcoat over a checked shirt, kind wrinkly smile, slightly stooped, standing upright like a person, "
                    "same slightly Pixar-ish knitted-wool photorealistic style as Eli and Ruthie, no text"),
    "Nana Dot": ("Nana Dot, Grandpa Ram's wife: a photorealistic elderly ewe with soft snowy-white curly wool, rosy cheeks, "
                 "gold-rimmed reading glasses on a beaded chain, a pearl necklace and a lilac hand-knitted cardigan, sweet "
                 "twinkly smile, often holding knitting needles or a tea tray, standing upright like a person, same slightly "
                 "Pixar-ish knitted-wool photorealistic style as Eli and Ruthie, no text"),
    "Kiwi Kev": ("Kiwi Kev, the cheeky neighbour: a photorealistic brown kiwi bird with a round shaggy-feathered body about half "
                 "Eli's height, a long thin slightly curved beak, bright beady eyes with a mischievous glint, usually wearing a "
                 "black singlet and tiny black gumboots, standing upright like a person, nocturnal and always a bit sleepy in "
                 "daytime, same slightly Pixar-ish photorealistic style as Eli and Ruthie, realistic feather detail, no text"),
    "Pip": ("Pip, Ruthie's bubbly little sister: a smaller, younger photorealistic lamb with light honey-blonde curly wool, a "
            "fluffy fringe, big sparkly brown eyes with long eyelashes, usually wearing a bright pink raincoat and yellow "
            "gumboots, always beaming and full of energy, standing upright like a person, same slightly Pixar-ish "
            "knitted-wool photorealistic style as Eli and Ruthie, no text"),
}

# (hari, slot, who, teks meme, adegan untuk prompt gambar, caption, rohani?)
# who = "eli" | "ruthie" | "couple" | "friends"  (friends = minimal satu karakter FRIENDS, namanya disebut di adegan)
DATA3 = [
    # ---------- Minggu 18 Okt (hari 15) ----------
    (15, "pagi", "couple", "Not yesterday. Not tomorrow.\nToday is the gift.",
     "Eli in his Sunday best (navy blazer, crisp white shirt, little red bow tie and his navy pom-pom beanie) walking hand in hand "
     "with Ruthie (pale-yellow floral sundress, white cardigan, pink daisy behind her ear) down a quiet country lane lined with "
     "white spring blossom trees towards a small white wooden country church, both smiling softly, petals drifting in the air, "
     "warm golden morning sunlight",
     "Sunday reminder 🐑🤍\n\n“This is the day which the LORD hath made; we will rejoice and be glad in it.” — Psalm 118:24 (KJV)\n\n"
     "Whatever today holds, there is joy to be found in it.", True),
    (15, "pagi2", "friends", "Church morning tea:\nNana Dot's ginger crunch\ngone in 4 minutes.",
     "Bright church hall after the service, a long trestle table with a lace cloth, plates of homemade slices, a big tea urn and "
     "floral cups and saucers; Nana Dot in her lilac cardigan and pearls proudly holding out a plate of golden ginger crunch, "
     "Eli in his navy blazer, bow tie and navy pom-pom beanie sneakily stacking three pieces on his saucer with a guilty grin, "
     "Grandpa Ram behind him holding a cup of tea and chuckling, soft late-morning window light",
     "Church family + homemade slice = the best kind of Sunday 🍰💕 (Say hi to Nana Dot & Grandpa Ram!)\n\n"
     "Ginger crunch or Louise slice?", False),
    (15, "malam", "ruthie", "Sunday meal prep:\n5 lunches, perfectly portioned.\n9pm: there are 2.",
     "Ruthie in a fluffy pink dressing gown and bunny slippers, pink daisy behind her ear, standing in a cosy kitchen at night "
     "staring at a neat row of five glass lunch containers on the bench, three of them empty with forks inside and lids off, "
     "one eyebrow raised in deep suspicion, warm pendant light",
     "I have one suspect and he wears a beanie 🕵️‍♀️🍱\n\nDo you meal prep, or wing it every day?", False),

    # ---------- Senin 19 Okt (hari 16) ----------
    (16, "pagi", "eli", "The bus app: “arriving in 2 min.”\n25 minutes later:\nstill “arriving in 2 min.”",
     "Eli in a bright yellow rain jacket, black gumboots and his navy pom-pom beanie standing alone at a suburban bus shelter in "
     "light drizzle, holding his phone and staring down the empty road with a flat, unimpressed face, wet footpath reflecting "
     "soft grey morning light",
     "Any minute now… 🚌🙃\n\nWhat's your record wait for the bus?", False),
    (16, "pagi2", "friends", "Grandpa Ram: “Tomatoes go in at Labour Day.\nNot before. Not after.\nThat's the law.”",
     "Grandpa Ram in his flat cap, round glasses and tweed waistcoat leaning on the wooden fence between the two backyards, holding "
     "a tray of small tomato seedlings and wagging one hoof very seriously, Eli on the other side in a green gardening apron, "
     "gardening gloves and his navy pom-pom beanie nodding obediently with a trowel in hand, sunny spring vegetable garden, "
     "bright midday light",
     "Is this a real rule or a Grandpa rule? 🍅👴\n\nWhen do your tomatoes go in?", False),
    (16, "malam", "couple", "Spring cleaning:\nher: declutters the whole house.\nme: emotional over a 2009 phone charger.",
     "Ruthie in a striped apron with a headscarf tied over her curls and her pink daisy, carrying a full cardboard box of clutter "
     "and giving Eli a look; Eli in flannel pyjamas and his navy pom-pom beanie sitting on the lounge floor surrounded by tangled "
     "old cables and gadgets, holding up an ancient mobile phone with a nostalgic, teary smile, warm evening lamplight",
     "It might still work! 🔌🥹\n\nWhat's hiding in your junk drawer?", False),

    # ---------- Selasa 20 Okt (hari 17) ----------
    (17, "pagi", "ruthie", "Spring in NZ is so pretty.\nAchoo.\nSo pretty. Achoo.",
     "Ruthie in a lilac knitted cardigan, pink daisy behind her ear, standing under a big pink blossom tree caught mid-sneeze with "
     "her eyes squeezed shut and a tissue in her hoof, petals swirling around her, watery eyes, suburban park, bright soft "
     "morning light",
     "Hay fever season is no joke 🌸🤧\n\nWho else is sneezing non-stop?", False),
    (17, "pagi2", "friends", "Ruthie: my sister's coming to stay!\nMe: for how long?\nRuthie: *changes the subject*",
     "Pip in her bright pink raincoat and yellow gumboots bursting through the front door with her arms wide open, beaming, Ruthie "
     "squealing with joy as she hugs her, Eli standing behind them in his navy Fair Isle jumper and navy pom-pom beanie holding "
     "Pip's bulging suitcase and a rolled-up sleeping bag with a nervous smile, bright hallway, midday light",
     "Everyone, meet Pip 💕 Ruthie's little sister, staying for “a couple of nights.”\n\nDo you have a sibling like Pip?", False),
    (17, "malam", "friends", "Sisters: “Let's have an early night.”\nAlso sisters at 1am:",
     "Ruthie and Pip in matching pink pyjamas lying on the lounge floor on a pile of cushions under glowing fairy lights, giggling "
     "uncontrollably with a big bowl of popcorn between them; Eli in the doorway in striped pyjamas and his navy pom-pom beanie "
     "with a sleep mask pushed up, squinting sleepily, dark cosy room lit only by fairy lights",
     "I now know everything that ever happened at their high school 😴😂\n\nTag your sister or your night-owl bestie.", False),

    # ---------- Rabu 21 Okt (hari 18) ----------
    (18, "pagi", "friends", "Pip: “Do you have oat milk?\nAvocado? Sourdough?”\nMe: we have Weet-Bix.",
     "Pip in a pink hoodie sitting at the kitchen table counting on her hooves with a hopeful smile, Eli standing at the bench in "
     "a grey T-shirt and his navy pom-pom beanie holding a plain unbranded cereal box and a bottle of milk with a deadpan face, "
     "sunny little kitchen, morning light",
     "Guest breakfast menu: cereal… or cereal 🥣😂\n\nHow many Weet-Bix do you go?", False),
    (18, "pagi2", "ruthie", "Lunch break hobby:\nlooking at houses I can't afford\nand choosing curtains for them.",
     "Ruthie in a camel trench coat with her pink daisy, sitting on a park bench at lunchtime with a takeaway salad untouched "
     "beside her, scrolling on her phone with a dreamy, hopeful face, city park with trees and a fountain, bright midday light",
     "Just browsing 🏡😅\n\nDream house: beach, bush or city?", False),
    (18, "malam", "couple", "Her feet in bed:\n-4°C.\nMy legs: why.",
     "Eli and Ruthie in bed in matching tartan flannel pyjamas under a thick duvet, Ruthie smugly pressing her cold feet against "
     "Eli with a cheeky grin, Eli wide-eyed and frozen in shock with his navy pom-pom beanie slightly askew, bedside lamp "
     "glowing, cosy bedroom at night",
     "How are they ALWAYS cold?? 🥶🦶\n\nTag the one with ice-block feet.", False),

    # ---------- Kamis 22 Okt (hari 19) ----------
    (19, "pagi", "eli", "10am smoko:\nthe most important meeting\nof the day.",
     "Eli in an orange hi-vis vest over a flannel shirt, work boots and his navy pom-pom beanie sitting on a stack of timber at a "
     "building site, holding a steaming thermos cup and a giant sandwich with a blissful face, a tin lunchbox beside him, "
     "scaffolding behind, bright morning sun",
     "Smoko is sacred ☕🥪\n\nWhat's in your smoko box?", False),
    (19, "pagi2", "ruthie", "Humidity: 85%.\nMy wool:",
     "Ruthie in a pastel blue blouse holding a hand mirror and staring in horror at her caramel curls, which have frizzed into an "
     "enormous puffy cloud around her face, her pink daisy almost lost in the fluff, muggy grey sky through the window behind "
     "her, soft midday light",
     "Good wool days are a myth 😩☁️\n\nCurly crew: how do you survive the humidity?", False),
    (19, "malam", "friends", "Our neighbour Kev is a kiwi.\n11pm: “Can I borrow a cup of sugar?\nAnd your ladder? And your trailer?”",
     "Eli in pyjamas and his navy pom-pom beanie opening the front door at night with sleepy half-closed eyes, porch light glowing, "
     "and on the doorstep Kiwi Kev in his black singlet and tiny black gumboots wearing a head torch, holding out an empty mug "
     "with a big cheeky grin, moths fluttering around the light, dark garden behind",
     "Meet Kiwi Kev 🥝🐦 Great neighbour. Totally nocturnal.\n\nWhat's the latest someone's knocked on your door?", False),

    # ---------- Jumat 23 Okt (hari 20) ----------
    (20, "pagi", "eli", "Spring alarm clock:\none very loud tūī.\n5:12am. Every day.",
     "Eli in a navy checked dressing gown, slippers and his navy pom-pom beanie standing on the front porch at dawn holding a mug "
     "of tea, bed-head wool, squinting up at a tūī (glossy dark bird with a white throat tuft) singing loudly from a "
     "yellow-flowering kōwhai tree, soft pink dawn light",
     "Beautiful song. Terrible timing 🐦🎶\n\nWhat bird wakes you up?", False),
    (20, "pagi2", "couple", "Planning the long weekend:\nher: itinerary, bookings, colour-coded.\nme: “we'll stop for snacks.”",
     "Ruthie in round reading glasses and a cardigan at the dining table surrounded by a laptop, highlighters and a planner "
     "bristling with colourful sticky tabs, concentrating hard, while Eli in a hoodie and his navy pom-pom beanie sits beside her "
     "happily hugging a big bag of road-trip lollies, sunny dining room, midday light",
     "Labour Weekend road trip loading… 🚗🗺️\n\nAre you the planner or the passenger?", False),
    (20, "malam", "friends", "Pip went home.\nThe house is so quiet.\n(I miss her too. Don't tell Ruthie.)",
     "Eli in his navy Fair Isle jumper and navy pom-pom beanie and Ruthie in a soft cardigan standing in their driveway at dusk "
     "waving goodbye, Pip in her pink raincoat waving back from the open window of a small car as it pulls away, Eli secretly "
     "wiping a tear with one hoof, warm orange sunset light",
     "Come back soon, Pip 🥹💕\n\nWho's the sibling or friend you miss the most?", False),

    # ---------- Sabtu 24 Okt (hari 21) - Labour Weekend, road trip ke Rotorua ----------
    (21, "pagi", "friends", "Who's minding the house this weekend?\nKev.\nHe'll be awake… at some point.",
     "Early morning in the driveway: Eli in a navy puffer vest, shorts and his navy pom-pom beanie loading a bag into the boot of "
     "a small hatchback, Ruthie in a denim jacket and straw sunhat carrying two pillows, and Kiwi Kev in an oversized fluffy "
     "dressing gown standing on their front step yawning hugely, holding the spare key, eyes half shut, soft early sunlight",
     "House-sitter: secured. Awake: debatable 🥝🔑\n\nWho looks after your place when you're away?", False),
    (21, "pagi2", "couple", "Road trip snacks:\nbought for a 3-hour drive.\nGone before the end of our street.",
     "Inside a small car on a country highway: Ruthie in the passenger seat in big sunglasses with empty chip packets and lolly "
     "bags on her lap, mid-chew with a guilty smile, Eli driving in sunglasses and his navy pom-pom beanie glancing at her in "
     "disbelief, rolling green farmland and cows through the windows, bright midday sun",
     "Rotorua, here we come 🚗🍬\n\nWhat's your must-have road trip snack?", False),
    (21, "malam", "couple", "Arrived in Rotorua.\nHer: “Did you…?”\nMe: “It's the town, I promise!”",
     "Eli in a light rain jacket and his navy pom-pom beanie and Ruthie in her denim jacket standing beside bubbling grey "
     "geothermal mud pools with plumes of steam rising, Ruthie pinching her nose and giving Eli a suspicious side-eye, Eli holding "
     "both hooves up innocently, dusky evening sky glowing orange through the steam",
     "Rotorua: you smell it before you see it 😂♨️\n\nBeen there? Love it or can't handle the smell?", False),

    # ---------- Minggu 25 Okt (hari 22) - di Rotorua ----------
    (22, "pagi", "couple", "Sometimes the most faithful thing\nyou can do is… be still.",
     "Eli in his navy Fair Isle jumper and navy pom-pom beanie and Ruthie wrapped in a cream hand-knitted blanket, pink daisy "
     "behind her ear, sitting close together at the end of an old wooden jetty on a glassy calm lake at dawn, soft wisps of "
     "steam and mist drifting over the water, distant hills, pink and gold sunrise reflecting on the lake, peaceful and quiet",
     "Sunday reminder 🐑🤍\n\n“Be still, and know that I am God…” — Psalm 46:10 (KJV)\n\n"
     "Wherever you are this long weekend, take a quiet moment with Him.", True),
    (22, "pagi2", "eli", "Me: I'll take it slow on the luge.\nAlso me:",
     "Eli speeding down a winding luge track in a small three-wheeled cart, a safety helmet perched on top of his navy pom-pom "
     "beanie, wool flying back in the wind, mouth wide open in pure joy, hooves gripping the handlebar, pine forest and a "
     "sparkling lake far below, bright sunny day, slight motion blur",
     "One more ride. Okay, five more 🛷😆\n\nHave you done the luge?", False),
    (22, "malam", "couple", "Hot pools:\n10 minutes in: relaxed.\n40 minutes in: I am soup.",
     "Eli and Ruthie soaking up to their shoulders in a steaming outdoor geothermal hot pool at night, Eli still wearing his navy "
     "pom-pom beanie, Ruthie's pink daisy behind her ear, both flushed, droopy-eyed and blissfully melted, damp fluffy wool, warm "
     "lanterns glowing through thick steam, starry sky",
     "Lamb soup, anyone? ♨️😵‍💫\n\nHot pools: how long can you last?", False),

    # ---------- Senin 26 Okt (hari 23) - Labour Day ----------
    (23, "pagi", "ruthie", "“Just one quick photo in the Redwoods.”\nPhoto count: 312.",
     "Ruthie in a sage-green hiking jacket and white sneakers, pink daisy behind her ear, striking a dramatic pose with one hoof "
     "on a giant redwood trunk among towering redwood trees and lush green tree ferns, beams of misty morning sunlight streaming "
     "through the forest, glamorous confident expression",
     "Instagram husband duties 📸🌲 (Eli took all 312.)\n\nWho's the photographer in your relationship?", False),
    (23, "pagi2", "friends", "Labour Day, 6am.\nWe're in Rotorua.\nGrandpa Ram planted our tomatoes anyway.",
     "Grandpa Ram in a red-and-black checked woollen bush shirt, flat cap and round glasses kneeling in Eli and Ruthie's backyard "
     "vegetable garden, carefully pressing soil around a row of freshly planted tomato seedlings with little wooden stakes, a "
     "watering can beside him, quiet proud smile, fresh early sunlight and dew sparkling on the grass",
     "Best neighbour in Aotearoa 🍅👴💚 Rules are rules.\n\nAre your tomatoes in yet?", False),
    (23, "malam", "couple", "Home from the long weekend.\nThe suitcase will now live\nin the hallway for 2 weeks.",
     "Eli in a grey hoodie and his navy pom-pom beanie and Ruthie in an oversized sweatshirt collapsed side by side on the couch at "
     "night with their eyes closed, an open suitcase spilling clothes across the hallway floor in front of them, car keys and a "
     "bag of souvenir fudge on the coffee table, warm lamp light",
     "Unpacking? Never heard of it 😴🧳\n\nHow long does your suitcase sit before you unpack?", False),

    # ---------- Selasa 27 Okt (hari 24) ----------
    (24, "pagi", "eli", "4-day week after a long weekend\nsomehow feels like 9 days.",
     "Eli in a crisp light-blue business shirt, navy tie and his navy pom-pom beanie slumped at an office desk with his cheek "
     "resting on a pile of papers, a mug of tea going cold beside the keyboard, half-closed eyes, bright morning office light "
     "through the window",
     "How is it only Tuesday? 😩💼\n\nStill in long weekend mode?", False),
    (24, "pagi2", "ruthie", "Shops in October:\n“Christmas is HERE!”\nMe: too early… *buys tinsel*",
     "Ruthie in a white linen shirt, denim shorts and sunglasses pushed up on her head, pink daisy behind her ear, standing in a "
     "bright department store aisle overflowing with tinsel, shiny baubles and artificial Christmas trees, holding a sparkly red "
     "bauble with a shocked-but-secretly-thrilled face, a basket of tinsel on her arm, bright store lighting",
     "Too early? Or never too early? 🎄😂\n\nWhen do you start your Christmas shopping?", False),
    (24, "malam", "friends", "Kev's secret whitebait spot.\nHe made me swear not to tell.\nIt's the river. Everyone's there.",
     "Misty riverbank at dusk: Kiwi Kev in his black singlet, shorts and tiny gumboots proudly holding a long-handled whitebait net "
     "over the water, Eli beside him in a red-and-black checked woollen bush shirt, black gumboots and his navy pom-pom beanie "
     "holding a bucket and glancing at the many other nets lined up along the bank into the distance, golden-grey evening light "
     "reflecting on the water",
     "Whitebait fritter or bust 🐟🍳\n\nFritter in white bread with lemon: yes or yes?", False),

    # ---------- Rabu 28 Okt (hari 25) - mulai alur BBQ ----------
    (25, "pagi", "couple", "Her: let's have a few friends over Saturday.\nMe: how many is “a few”?\nHer: fourteen.",
     "Ruthie in a pink knitted cardigan perched on the kitchen bench happily chatting on her phone and counting on her other hoof, "
     "eyes sparkling with excitement, Eli in a grey hoodie and his navy pom-pom beanie standing beside her holding a single "
     "packet of sausages, eyes wide with alarm, bright morning kitchen",
     "BBQ season is officially open 🔥🌭\n\nHow many is “a few” in your house?", False),
    (25, "pagi2", "eli", "Eating lunch in the sun\nfor the first time since April.",
     "Eli in a short-sleeved navy polo shirt, sunglasses and his navy pom-pom beanie sitting on a wooden bench in a green city park "
     "with his face tilted up to the sun, eyes closed in bliss, holding a half-eaten sandwich, blossom trees and blue sky, bright "
     "warm midday light",
     "Vitamin D, we meet again ☀️😌\n\nWhere's your favourite lunch spot?", False),
    (25, "malam", "friends", "Nana Dot is knitting us\nmatching Christmas jumpers.\nIt's October.",
     "Cosy cottage lounge at night: Nana Dot in her lilac cardigan, pearls and reading glasses on a beaded chain sitting in a floral "
     "armchair knitting a bright red-and-green Christmas jumper with a reindeer pattern, a basket of wool at her feet, Eli in his "
     "navy Fair Isle jumper and navy pom-pom beanie and Ruthie on the couch holding teacups and exchanging an amused glance, warm "
     "lamplight",
     "Nana Dot's needles never stop 🧶💕 (She knitted my beanie too!)\n\nDid your nana knit for you?", False),

    # ---------- Kamis 29 Okt (hari 26) ----------
    (26, "pagi", "ruthie", "Guests coming Saturday.\nMe: deep-cleans places\nnobody will ever see.",
     "Ruthie in a yellow apron, pink rubber gloves and a headscarf, pink daisy behind her ear, balancing on a stepladder scrubbing "
     "the top of the fridge with fierce determination, a spray bottle in her other hoof, sparkling clean kitchen, bright morning "
     "sunlight",
     "They WILL look on top of the fridge. Probably 😤🧽\n\nWhat do you only clean when guests are coming?", False),
    (26, "pagi2", "friends", "Teaching Pip to drive.\nPip: “Which one's the brake again?”\nMe:",
     "Pip in her pink raincoat behind the steering wheel of a small car, grinning with total confidence, Eli in the passenger seat "
     "in his navy pom-pom beanie gripping the door handle and the dashboard with wide terrified eyes, his wool standing on end, "
     "quiet tree-lined suburban street through the windscreen, bright midday light",
     "Pip's going for her licence 🚗😬 Please keep me in your thoughts.\n\nWho taught you to drive?", False),
    (26, "malam", "couple", "8pm and still light outside.\nMy brain: it's 4pm,\nlet's start a DIY project.",
     "Eli in shorts, a T-shirt and his navy pom-pom beanie on the back deck at golden hour hammering together a slightly wonky "
     "wooden planter box, sawdust everywhere, very pleased with himself, Ruthie in a floral sundress with her pink daisy sitting "
     "in a deck chair sipping lemonade and laughing, long warm golden evening light",
     "Long summer evenings are coming ☀️🔨\n\nWhat do you do with the extra daylight?", False),

    # ---------- Jumat 30 Okt (hari 27) ----------
    (27, "pagi", "eli", "October 30.\nThe supermarket's playing Christmas carols.\nI'm buying sunscreen.",
     "Eli in shorts, a T-shirt, jandals and sunglasses pushed up onto his navy pom-pom beanie standing in a supermarket aisle "
     "holding a bottle of sunscreen and a tub of ice cream, looking up towards the ceiling with a puzzled face, shiny tinsel "
     "garlands strung above the aisle, bright store lighting",
     "Jingle bells in 24 degrees 🎶☀️\n\nCarols in October: yay or nay?", False),
    (27, "pagi2", "couple", "Her: we have 3 bags of ice.\nMe: the chilly bin has NEEDS.",
     "Eli in board shorts, a singlet and his navy pom-pom beanie straining to drag a huge chilly bin overflowing with bags of ice "
     "across the back deck, Ruthie in a straw sunhat with her pink daisy, arms crossed, watching with an amused smirk, bright "
     "sunny backyard at midday",
     "The chilly bin is never full enough 🧊😂\n\nChilly bin or esky? (Wrong answers only 😉)", False),
    (27, "malam", "friends", "Grandpa Ram inspecting my BBQ\nthe night before the party.\nI feel like I'm being marked.",
     "Grandpa Ram in his tweed waistcoat, flat cap and round glasses pushed down his nose leaning in close to examine a shiny "
     "backyard gas barbecue with a wire brush in hand, one bushy eyebrow raised, Eli in a navy-and-white striped BBQ apron and "
     "his navy pom-pom beanie standing stiffly beside him holding tongs like a nervous student, deck lit by festoon lights at dusk",
     "He gave it a 6/10. I'll take it 🔥👴\n\nWho's the BBQ boss in your family?", False),

    # ---------- Sabtu 31 Okt (hari 28) - hari BBQ ----------
    (28, "pagi", "couple", "Party starts at 4.\nUs at 3:58:",
     "Eli in a bright tropical-print summer shirt and his navy pom-pom beanie wobbling on a ladder while hanging festoon lights "
     "across the deck, Ruthie in a floral sundress with her pink daisy rushing past carrying a giant bowl of salad and a bunch of "
     "balloons, half-blown-up balloons and an open box of paper plates everywhere, both frantic but laughing, bright sunny "
     "afternoon",
     "Every host, every time 😅🎈\n\nAre you an early-ready host or a 3:58 host?", False),
    (28, "pagi2", "friends", "“Bring a plate,” we said.\nKev:",
     "Sunny backyard BBQ: Kiwi Kev in his black singlet and sunglasses proudly holding up a completely empty white dinner plate "
     "with a huge grin, Nana Dot beside him holding a heaped tray of club sandwiches and looking puzzled, Eli in his striped BBQ "
     "apron and navy pom-pom beanie at the grill laughing so hard he is bent over, Grandpa Ram and Pip in the background with "
     "glasses of lemonade, festoon lights strung overhead, bright summer light",
     "In NZ, “bring a plate” means bring FOOD, Kev 😂🍽️\n\nDid you know this Kiwi rule?", False),
    (28, "malam", "friends", "The party ended at 9.\nThe goodbye ended at 10:30.",
     "Driveway at night under festoon lights: Grandpa Ram and Nana Dot halfway into their old car with the doors open, still "
     "chatting and laughing with Eli (tropical shirt and navy pom-pom beanie) and Ruthie, Pip hugging Ruthie from behind, Kiwi "
     "Kev waving a torch, everyone holding containers of leftovers, warm happy faces, deep blue night sky",
     "The Kiwi goodbye is an event in itself 😂🚗\n\nHow long does your goodbye take?", False),

    # ---------- Minggu 1 Nov (hari 29) ----------
    (29, "pagi", "couple", "Before the tinsel and the lists…\nremember the greatest Gift.",
     "Eli in his navy Fair Isle jumper and navy pom-pom beanie and Ruthie in a soft cream dress with her pink daisy sitting "
     "together on a weathered wooden bench beneath a large coastal pōhutukawa tree with its first deep-red buds, Ruthie holding a "
     "small hand-carved wooden star, calm turquoise sea and gentle morning sun behind them, peaceful warm smiles",
     "Sunday reminder 🐑🤍\n\n“For unto us a child is born, unto us a son is given: and the government shall be upon his shoulder: "
     "and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace.” "
     "— Isaiah 9:6 (KJV)\n\nThe shops are counting down to Christmas. Let's count our blessings too.", True),
    (29, "pagi2", "friends", "Nana Dot: “You're looking thin.\nHave some more.”\nMe, on my third plate:",
     "Sunday lunch at Nana Dot's: a lace-covered dining table with roast chicken, crispy roast potatoes, pumpkin and gravy; Eli in "
     "a collared Sunday shirt and his navy pom-pom beanie with a plate piled impossibly high and cheeks full, Nana Dot in a floral "
     "apron happily spooning more potatoes onto it, Grandpa Ram chuckling at the head of the table and Ruthie giggling behind her "
     "hoof, warm sunny dining room",
     "Nana love is measured in roast potatoes 🥔💕\n\nWhat's your nana's signature dish?", False),
    (29, "malam", "ruthie", "November 1st:\nmy Christmas list is done.\nAnd laminated.",
     "Ruthie in cosy candy-striped pyjamas, pink daisy behind her ear, sitting cross-legged on the bed with a very long paper "
     "scroll unrolling off the bed onto the floor, covered in tiny doodles of stars, hearts and gift boxes, a pen in her mouth "
     "and a proud grin, fairy lights glowing over the headboard, warm night light",
     "Organised, not obsessed 🎄📝\n\nHave you started your Christmas list yet?", False),

    # ---------- Senin 2 Nov (hari 30) ----------
    (30, "pagi", "eli", "Working from home:\nbusiness on top,\nweekend on the bottom.",
     "Eli at a home desk on a video call (laptop seen from behind) wearing a crisp white shirt, navy tie and his navy pom-pom "
     "beanie, sitting up straight with a professional smile, while under the desk he wears tartan pyjama pants and fluffy "
     "slippers, a mug of coffee beside the laptop, bright morning light from a window",
     "Nobody needs to know 💼🩴\n\nWhat's your WFH outfit? Be honest 👇", False),
    (30, "pagi2", "couple", "Budget meeting.\nHer: “What's this $43 at a bakery?”\nMe: “…a very good bakery.”",
     "Ruthie in a smart navy blouse with her pink daisy at the dining table pointing at a laptop (seen from the side) with a "
     "calculator beside her and one eyebrow raised, Eli next to her in a knitted vest and his navy pom-pom beanie clutching a "
     "paper bag of pastries, flaky crumbs all over his wool and a guilty innocent smile, sunny midday dining room",
     "Worth every cent 🥐😇\n\nWho's the saver in your relationship?", False),
    (30, "malam", "friends", "Pip signed up to be an elf\nin the Santa parade.\nShe signed me up too.",
     "Pip in her pink raincoat bouncing with excitement in the lounge, holding up two green elf costumes with pointy hats and "
     "jingle bells, Eli on the couch in a grey hoodie and his navy pom-pom beanie frozen in horror, Ruthie beside him laughing "
     "into a cushion, warm evening lamplight",
     "Santa parade season is coming 🎅🧝 Come watch me suffer.\n\nDo you go to your local Santa parade?", False),

    # ---------- Selasa 3 Nov (hari 31) ----------
    (31, "pagi", "ruthie", "First swim of the season:\n“It's not even that cold!”\n(It was that cold.)",
     "Ruthie in a pink-and-white floral swimsuit and a wide straw sunhat, pink daisy behind her ear, standing knee-deep in clear "
     "turquoise sea at a golden-sand New Zealand beach, arms up in the air, mouth open in a frozen gasp, wool bristling, bright "
     "morning sun and gentle waves",
     "NZ sea in November = for the brave only 🥶🌊\n\nHave you been in the water yet?", False),
    (31, "pagi2", "eli", "NZ sun:\n10 minutes outside in November.\nMe:",
     "Eli in a T-shirt, summer shorts and his navy pom-pom beanie staring at himself in a bathroom mirror, his little nose bright "
     "pink with sunburn and a perfect pale outline of sunglasses around his eyes, an unopened bottle of sunscreen sitting on the "
     "bench, shocked face, bright midday light",
     "The NZ sun does not play 🌞🥵 Slip, slop, slap, people!\n\nSPF 30 or SPF 50?", False),
    (31, "malam", "couple", "2am. Thumping on the roof.\nHer: “What IS that?”\nMe: “A possum. Probably. Hopefully.”",
     "Eli and Ruthie sitting bolt upright in bed in their pyjamas at night, both staring up at the ceiling with huge eyes, Eli in "
     "his navy pom-pom beanie holding a torch and a slipper like a weapon, Ruthie clutching the duvet up to her chin, moonlight "
     "through the curtains, dark bedroom",
     "Possums: NZ's least favourite alarm clock 🐾😳\n\nWhat's the weirdest noise you've heard at night?", False),

    # ---------- Rabu 4 Nov (hari 32) ----------
    (32, "pagi", "friends", "Grandpa Ram: “Pōhutukawa flowering early\nmeans a long hot summer.”\nHe's said that every year since 1971.",
     "Grandpa Ram in his flat cap, tweed waistcoat and round glasses pointing his walking stick wisely up at a huge coastal "
     "pōhutukawa tree covered in tiny red buds, Eli in a short-sleeved summer shirt and his navy pom-pom beanie gazing up beside "
     "him, sparkling blue sea and clifftop behind, fresh golden morning light",
     "NZ's Christmas tree is getting ready 🌺🎄\n\nHas your pōhutukawa started flowering?", False),
    (32, "pagi2", "ruthie", "Roadside strawberry stall:\n“Just one punnet.”\nIt didn't make it to the car.",
     "Ruthie in denim overalls and a straw sunhat, pink daisy behind her ear, standing beside a rustic wooden roadside fruit stall "
     "in the countryside holding an empty strawberry punnet, a little strawberry juice on her lips and a sheepish guilty smile, "
     "rows of strawberry plants behind, bright sunny midday",
     "Strawberry season is here 🍓😋\n\nDo they ever make it home in your car?", False),
    (32, "malam", "friends", "Wednesday social touch:\n“It's just a casual game.”\nKev:",
     "Evening sports field: Kiwi Kev in a tiny black rugby jersey launching into a dramatic full-length dive over the try line "
     "with the ball, grass flying, Eli in a black rugby jersey, shorts and his navy pom-pom beanie standing behind him with both "
     "hooves on his head in disbelief, other players blurred in the background, golden evening light and long shadows",
     "Kev takes “social” VERY seriously 🏉🥝\n\nAnyone else play touch on a weeknight?", False),

    # ---------- Kamis 5 Nov (hari 33) - Guy Fawkes ----------
    (33, "pagi", "eli", "Ironing my shirt:\nfront: perfect.\nback: the jumper will cover it.",
     "Eli in a white singlet and his navy pom-pom beanie at an ironing board in the bedroom, carefully ironing only the collar and "
     "front of a blue shirt while the back is still very crumpled, a navy jumper ready on the bed, sly satisfied smirk, morning "
     "sun through the curtains",
     "If nobody sees it, it doesn't count 👔😏\n\nBe honest: do you iron the whole shirt?", False),
    (33, "pagi2", "couple", "Planning summer holidays:\nher: “Somewhere new!”\nme: “Same campground as every year.”",
     "Eli and Ruthie at the kitchen table, Ruthie in a sleeveless summer top with her pink daisy fanning out glossy travel "
     "brochures showing palm trees and turquoise water with a hopeful face, Eli in a T-shirt and his navy pom-pom beanie holding "
     "up an old faded photo of a family tent at a beach campground with a cheeky grin, bright sunny midday kitchen",
     "Kiwi summer = the same campsite since forever ⛺☀️\n\nWhere do you go every summer?", False),
    (33, "malam", "couple", "Guy Fawkes night, a guide for sheep:\nearmuffs on, lights off,\nbig cuddle.",
     "Eli and Ruthie snuggled under a thick hand-knitted blanket on the couch, Eli wearing fluffy earmuffs over his navy pom-pom "
     "beanie and Ruthie in pink earmuffs next to her daisy, both holding mugs of hot chocolate with wide eyes, bright colourful "
     "fireworks bursting outside the dark lounge window, cosy lamp glow",
     "Thinking of all the pets and farm animals tonight 🎆🐑 Please be kind with the fireworks!\n\n"
     "Fireworks fan or hide-under-the-blanket type?", False),

    # ---------- Jumat 6 Nov (hari 34) ----------
    (34, "pagi", "friends", "Nana Dot started her Christmas baking.\nIt's November 6.\nShe's on batch four.",
     "Nana Dot in a floral apron and reading glasses on a beaded chain pulling a golden tray of shortbread from the oven in her "
     "warm cottage kitchen, stacks of biscuit tins on every bench, Ruthie in a gingham apron with flour on her nose and her pink "
     "daisy helping cut star shapes from the dough, both smiling, warm sunlight through lace curtains",
     "Christmas shortbread season has officially begun 🎄🍪\n\nWhat's your must-have Christmas bake?", False),
    (34, "pagi2", "eli", "Fixed the fence myself.\nTools used: number 8 wire\nand confidence.",
     "Eli in a red-and-black checked woollen bush shirt, work gloves, black gumboots and his navy pom-pom beanie standing proudly "
     "with hooves on hips beside a slightly crooked wooden farm fence held together with lots of twisted wire, pliers in his "
     "pocket, green paddock and rolling hills behind, bright midday sun",
     "Kiwi ingenuity at its finest 🔧🐑\n\nWhat's your best number 8 wire fix?", False),
    (34, "malam", "friends", "Family games night:\nPip: “It's just for fun.”\nAlso Pip:",
     "Cosy lounge at night: Pip in pink pyjamas standing on the couch with both hooves raised in triumphant victory, playing cards "
     "flying, Ruthie sitting with arms crossed and a mock-furious face, Eli in pyjamas and his navy pom-pom beanie face-down on "
     "the coffee table beside a board game in total defeat, bowls of chips, warm lamp light",
     "Sibling competitiveness is a real sport 🎲😤\n\nWho's the sore winner in your family?", False),

    # ---------- Sabtu 7 Nov (hari 35) ----------
    (35, "pagi", "ruthie", "Garage sale.\nThem: “Lamp's $2.”\nMe: “Would you take $1.50?”",
     "Ruthie in a striped Breton top, white jeans and sunglasses on her head, pink daisy behind her ear, at a sunny suburban "
     "garage sale among trestle tables of bric-a-brac, holding a vintage lamp in one hoof and a little coin purse in the other, "
     "negotiating with a determined narrowed-eyes face, bright morning sun",
     "Saturday bargain hunting is a sport 🏷️😤\n\nWhat's your best garage sale find?", False),
    (35, "pagi2", "couple", "Bought a real Christmas tree on November 7.\nBy Christmas it'll be\na very expensive stick.",
     "Eli in a singlet, shorts and his navy pom-pom beanie carrying a big fresh pine tree on his back across a sunny driveway, pine "
     "needles already sprinkling off it, Ruthie skipping ahead in the red-and-green reindeer Christmas jumper Nana Dot knitted "
     "(despite the heat), pink daisy behind her ear, holding a box of shiny baubles with pure joy, bright summery midday light",
     "Too early? We regret nothing (yet) 🌲😂\n\nReal tree or fake tree?", False),
    (35, "malam", "friends", "Rugby overseas: kick-off 3am.\nGrandpa Ram: “I'll just stay up.”\nGrandpa Ram at 9:15pm:",
     "Cosy lounge at night lit by the glow of a TV: Grandpa Ram in a black rugby jersey and his flat cap fast asleep in a "
     "recliner with his mouth open, glasses sliding down his nose and a cup of tea on the armrest, Eli in a matching black rugby "
     "jersey and his navy pom-pom beanie gently tucking a tartan blanket over him with a fond smile",
     "Respect the commitment 🏉😴\n\nAre you a 3am rugby alarm person?", False),
]
