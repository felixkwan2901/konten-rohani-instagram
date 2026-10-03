"""@eliandruthie - minggu 6-7: Minggu 8 Nov s/d Sabtu 21 Nov 2026 (hari 36-49), 3 post/hari.
Slot: "pagi" 07:00, "pagi2" 12:00, "malam" 20:00 (malam = Reel). Bahasa Inggris, humor NZ.

Dua teman baru (FRIENDS_NEW), dipakai sering; teman lama (Grandpa Ram, Nana Dot, Kiwi Kev, Pip) sesekali.
  - Big Tama: domba jantan Romney raksasa (2x tinggi Eli), tukang bangunan, gentle giant, takut wētā,
    pelukannya meremukkan, harus menunduk di pintu, semua barang kelihatan mini di tangannya.
  - Mei: burung pīwakawaka (fantail) mungil seukuran cangkir teh, barista kafe di pojok jalan,
    selalu merekam semuanya untuk media sosial, suka bertengger di kepala/bahu Big Tama.
Teman +-40% post (who="friends", nama teman selalu disebut persis di adegan).
Eli SELALU pakai navy pom-pom beanie; Ruthie SELALU pakai bunga daisy pink di belakang telinga.

Alur cerita mini:
  - Kenalan dengan Mei di kafe baru (hari 36) dan Big Tama si tukang dek (hari 37)
  - Bangun dek baru: jabat tangan (37), wētā & Kiwi Kev jadi pahlawan (38), teh dalam mangkuk adonan (39),
    pelukan take 14 (39), dek dipernis (40), tes keamanan: Big Tama lompat (41)
  - Kemah di DOC campsite + pantai pertama Big Tama: hari 42-43
  - Video wētā Big Tama viral di akun Mei (47)
  - Float Santa parade (lanjutan hari 30, Pip jadi elf): Pip merekrut Big Tama (44), glitter (45), parade (49)
Acara: Diwali (36, tetangga berbagi lampu & manisan), World Kindness Day (41), pohon Natal komunitas (48),
Santa parade (49), musim ujian akhir, belanja Natal mulai, pōhutukawa mekar, jangkrik/cicada, PYO stroberi,
sunscreen/UV, panas pertama musim panas. Natal +-1/3 minggu 7 (pav, Secret Santa, jumper Nana Dot, float).
Rohani hanya 1x/minggu: Minggu pagi (hari 36, 43), ayat KJV dikutip persis.
Tanpa merek di adegan; tanpa teks/tulisan di gambar (teks meme ditambahkan otomatis)."""

FRIENDS_NEW = {
    "Big Tama": ("Big Tama, the gentle-giant builder: a photorealistic enormous Romney ram, twice Eli's height and nearly "
                 "three times as wide, with massive broad shoulders, a barrel chest and huge hooves, thick dense cream-coloured "
                 "curly wool with a fluffy woolly topknot, no horns, a broad kind face with soft brown eyes and a shy gentle "
                 "smile, usually wearing an orange hi-vis vest over a grey T-shirt or a plain black rugby jersey, has to duck "
                 "under doorways, everything he holds looks tiny in his hooves, standing upright like a person, same slightly "
                 "Pixar-ish knitted-wool photorealistic style as Eli and Ruthie, no text"),
    "Mei": ("Mei, the café barista who films everything: a photorealistic tiny New Zealand fantail (pīwakawaka) no bigger "
            "than a teacup, a round fluffy body with a soft grey-brown head and back, a bold white eyebrow stripe, a white "
            "throat above a thin black chest band, a warm golden-buff belly, bright black beady eyes, and a long black tail "
            "with white edges almost always fanned out wide like an open fan, wearing a tiny mint-green barista apron, "
            "always bouncing, flitting or hovering mid-air, often filming on a tiny phone held in one wing, loves perching "
            "on shoulders and heads, same slightly Pixar-ish photorealistic style as Eli and Ruthie, realistic feather "
            "detail, no text"),
}

# (hari, slot, who, teks meme, adegan untuk prompt gambar, caption, rohani?)
# who = "eli" | "ruthie" | "couple" | "friends"  (friends = minimal satu karakter FRIENDS/FRIENDS_NEW, namanya disebut di adegan)
DATA6 = [
    # ---------- Minggu 8 Nov (hari 36) - Diwali ----------
    (36, "pagi", "couple", "The best friends love you\non the good days\nand the hard ones.",
     "Eli in a crisp white short-sleeved shirt, navy chinos and his navy pom-pom beanie walking arm in arm with Ruthie in a "
     "cornflower-blue Sunday dress with a white Peter Pan collar, pink daisy behind her ear, across a small wooden footbridge "
     "over a clear bubbling stream in lush native bush, Ruthie carrying a little basket with a cloth-wrapped loaf of homemade "
     "bread to share with a friend, giant tree ferns arching overhead, soft beams of golden morning sunlight through the "
     "canopy, gentle peaceful smiles",
     "Sunday reminder 🐑🤍\n\n“A friend loveth at all times, and a brother is born for adversity.” — Proverbs 17:17 (KJV)\n\n"
     "Thank God for the friends who stay. And be that friend for someone this week.", True),
    (36, "pagi2", "friends", "New café on our street.\nThe barista filmed my flat white\nfrom 9 angles. It's cold now.",
     "Bright little corner café with a gleaming espresso machine, pastel tiles and pot plants: Mei hovering mid-air above the "
     "wooden counter with her tail fanned wide, filming a flat white with a perfect latte-art heart on her tiny phone from a "
     "dramatic low angle, Eli in a pale-blue linen shirt and his navy pom-pom beanie reaching for the cup with a desperate, "
     "caffeine-deprived face, Ruthie in a mint-green tea dress with her pink daisy behind her ear laughing behind her hoof, "
     "sunny late-morning light through the big front window",
     "Everyone, meet Mei 🐦☕ Tiny fantail, huge energy. She runs the new café on the corner and films EVERYTHING.\n\n"
     "Would you let your coffee go cold for the perfect video?", False),
    (36, "malam", "couple", "Our neighbours' house for Diwali:\nglowing like a festival.\nOurs: one porch light and a moth.",
     "Night on a quiet suburban street: the house next door glowing beautifully with rows of little clay diya oil lamps along "
     "its steps, windowsills and path, strings of warm golden fairy lights and a bright flower-petal rangoli on the front path, "
     "a kind neighbour ewe in an elegant emerald-and-gold saree crossing the lawn towards them with a tray of Indian sweets "
     "(ladoos, barfi and jalebi) and a few lit diyas; Eli in a smart navy shirt and his navy pom-pom beanie and Ruthie in a "
     "coral dress with her pink daisy behind her ear standing on their own plain porch under a single bare bulb with one moth "
     "fluttering around it, both faces lit up with delight, warm magical glow",
     "Happy Diwali to everyone celebrating 🪔✨ Our lovely neighbours brought sweets AND lent us some diyas, so now our porch "
     "glows too.\n\nAre you celebrating tonight? What's your favourite Diwali sweet?", False),

    # ---------- Senin 9 Nov (hari 37) - kenalan dengan Big Tama, mulai bangun dek ----------
    (37, "pagi", "friends", "The builder knocked.\nI opened the door…\nand kept looking up.",
     "Eli in a grey hoodie, track pants and his navy pom-pom beanie standing in his front doorway holding a mug of tea, craning "
     "his neck all the way back with his mouth open, as Big Tama fills the entire doorframe and bends down low to peek in with "
     "a shy little wave, wearing an orange hi-vis vest over a grey T-shirt and a heavy tool belt, a tape measure looking like a "
     "tiny coin in his enormous hoof, a stack of fresh timber on the driveway behind him, bright early-morning sunlight",
     "Everyone, meet Big Tama 🐏💪 Builder, gentle giant, twice my height, and he's building our new deck this week.\n\n"
     "Who's the tallest person you know?", False),
    (37, "pagi2", "ruthie", "Summer wardrobe swap:\npacked away 9 cardigans.\nFound 6 more.",
     "Ruthie in a breezy white cotton sundress, pink daisy behind her ear, sitting cross-legged on the bedroom floor surrounded "
     "by towering stacks of folded cardigans in every pastel colour, half-filled storage bags and an open wardrobe still "
     "bursting with knitwear, holding up yet another lilac cardigan with a guilty 'oh no' face, bright midday sunlight through "
     "sheer curtains",
     "In my defence, they're all slightly different 🧶😅\n\nWhat do you own way too many of?", False),
    (37, "malam", "couple", "Shook hands with the new builder.\nI'll be doing everything\nleft-hoofed this week.",
     "Eli in pyjama shorts, a faded T-shirt and his navy pom-pom beanie slumped on the couch at night with his right hoof "
     "soaking in a big bowl of ice water and a pained but brave face, Ruthie in cosy pyjamas with her pink daisy behind her ear "
     "sitting beside him pressing a bag of frozen peas onto his hoof and trying very hard not to laugh, warm lamp light in a "
     "cosy lounge",
     "Big Tama is very friendly. VERY friendly 🤝🧊\n\nWhat's the strongest handshake you've ever survived?", False),

    # ---------- Selasa 10 Nov (hari 38) ----------
    (38, "pagi", "eli", "Car's been parked in the sun.\nThe seatbelt buckle:\n400 degrees.",
     "Eli in a short-sleeved summer shirt, shorts, sunglasses and his navy pom-pom beanie in the driver's seat of a small car, "
     "flinching dramatically and blowing on his hoof after touching the hot seatbelt buckle, a tea towel draped over the "
     "steering wheel, heat shimmering through the windscreen, bright glaring sun",
     "Kiwi summer has entered the chat ☀️🔥\n\nWhat's your trick for a hot car?", False),
    (38, "pagi2", "friends", "Big Tama: lifts a 60kg beam alone.\nAlso Big Tama: finds a wētā.\nHero of the day: Kev.",
     "Back yard with the old deck half torn up: Big Tama in his orange hi-vis vest balancing on top of an upturned wheelbarrow, "
     "clutching his chest with huge terrified eyes, while tiny Kiwi Kev, woken from his daytime nap and still in his black "
     "singlet, tiny black gumboots and a fluffy dressing gown, calmly holds up a glass jar with a big spiky brown wētā inside, "
     "sleepy half-closed eyes and a smug little smile, Eli in work gloves, an old grey T-shirt and his navy pom-pom beanie "
     "covering his mouth to hide a laugh, scattered old deck boards, bright midday sun",
     "The wētā was released safely in the garden. Tama is still recovering 🦗😂\n\n"
     "What tiny creature are YOU secretly scared of?", False),
    (38, "malam", "couple", "Summer nights:\none fan, two sheep,\nzero compromise.",
     "Hot summer night in a dim bedroom: Eli in a white singlet, boxer shorts and his navy pom-pom beanie and Ruthie in a light "
     "cotton nightie with her pink daisy behind her ear lying on top of the sheets, both reaching across the bed to turn a "
     "little oscillating desk fan towards themselves and glaring at each other playfully, wool fluffing in the breeze, window "
     "wide open, moonlight and a warm bedside lamp",
     "The fan belongs to whoever is awake 😤🌀\n\nFan, aircon or open window?", False),

    # ---------- Rabu 11 Nov (hari 39) ----------
    (39, "pagi", "friends", "Made the builder a cup of tea.\nIn his hoof it's an espresso.\nRound two: the mixing bowl.",
     "Sunny back yard with fresh pale timber deck joists: Big Tama in a plain black rugby jersey sitting on a stack of new "
     "timber, delicately pinching a tiny floral china teacup between two fingers with his pinky raised and a sheepishly "
     "grateful face, while Ruthie in a red gingham apron with her pink daisy behind her ear walks towards him carrying a huge "
     "steaming mixing bowl of tea in both hooves with a determined smile, a packet of biscuits tucked under her arm, bright "
     "morning light",
     "Builder's tea, Big Tama-sized ☕🐏\n\nHow do you take your tea?", False),
    (39, "pagi2", "eli", "24°C today.\n“Aren't you hot in that beanie?”\nNana Dot knitted it. It stays.",
     "Eli in a bright orange singlet, board shorts, jandals and sunglasses, still proudly wearing his navy pom-pom beanie, "
     "sitting on a park bench under a blazing summer sun with beads of sweat on his brow, holding a melting ice block, a "
     "determined and dignified face, sun-bleached grass and a sparkling harbour behind, bright midday glare",
     "Some things are bigger than the weather 🧶💙\n\nWhat's the one piece of clothing you'd never give up?", False),
    (39, "malam", "friends", "Mei: “One more hug,\nthe light wasn't right.”\nTake 14:",
     "Golden-hour back yard beside the half-built deck: Big Tama in his orange hi-vis vest wrapping Eli in an enormous bear hug "
     "and lifting him clean off the ground, Eli in an olive polo shirt, shorts and his navy pom-pom beanie squished and "
     "wide-eyed with his wool puffed out in all directions, while Mei hovers in front of them with her tail fanned, filming on "
     "her tiny phone and directing with one wing, Ruthie in a sundress with her pink daisy behind her ear holding a little "
     "ring light and giggling, warm orange evening glow",
     "Big Tama's hugs: 10/10 warmth, 11/10 pressure 🤗😵 Mei says the video will be worth it.\n\n"
     "Tag the best hugger you know.", False),

    # ---------- Kamis 12 Nov (hari 40) ----------
    (40, "pagi", "ruthie", "Decorating our real tree in 25°C.\nEvery bauble I hang:\n40 needles on the floor.",
     "Ruthie in a sleeveless floral playsuit with her pink daisy behind her ear standing beside a real pine Christmas tree in a "
     "sunny lounge, gently hanging a shiny red bauble while a shower of pine needles falls onto a carpet already covered in "
     "needles, a desk fan blowing on her face, a box of baubles at her feet, her expression a mix of joy and denial, bright "
     "warm morning light",
     "We bought it way too early and we'd do it again 🎄🥵\n\nWhen does your tree go up?", False),
    (40, "pagi2", "eli", "Mall car park in November:\nfollowing a stranger to their car\nlike a nature documentary.",
     "Eli in a white polo shirt, sunglasses and his navy pom-pom beanie driving a small hatchback at walking pace through a "
     "packed shopping-centre car park, leaning forward over the steering wheel with intense focused eyes, creeping slowly "
     "behind an unaware shopper carrying bags towards their parked car, rows of full parking spaces shimmering in the heat, "
     "bright midday sun",
     "Christmas shopping season has begun 🚗🛍️ Patience is a virtue. So is a car park.\n\n"
     "Do you circle, or park miles away and walk?", False),
    (40, "malam", "couple", "Staining the new deck.\nThe deck: patchy.\nMe: now the same colour as my wife.",
     "Golden evening on a brand-new timber deck half-coated in warm caramel-brown stain: Eli in paint-splattered white overalls "
     "and his navy pom-pom beanie holding a dripping brush, his white wool now splotched all over in the exact caramel-brown "
     "shade of Ruthie's wool, looking down at himself in shock, Ruthie in a pale-yellow sundress with her pink daisy behind "
     "her ear doubled over laughing and holding her hoof next to his arm to compare colours, an unlabelled tin of stain at "
     "their feet, long golden evening light",
     "Big Tama built it. I stained it. Only one of us did a tidy job 😂🪵\n\nWho's the messy DIYer in your house?", False),

    # ---------- Jumat 13 Nov (hari 41) - World Kindness Day ----------
    (41, "pagi", "friends", "World Kindness Day:\nI paid for the next person's coffee.\nIt was Big Tama. For his whole crew.",
     "Mei's sunny corner café at 7am: Eli in a crisp light-blue work shirt, navy tie and his navy pom-pom beanie at the counter "
     "staring wide-eyed into his open wallet, while Big Tama in his orange hi-vis vest stands behind him beaming with "
     "gratitude, carefully holding two cardboard trays stacked with nine takeaway coffees that look tiny in his hooves, Mei "
     "perched on top of the espresso machine with her tail fanned, giggling, soft golden morning light",
     "Still the best $54 I've ever spent 💛☕ Happy World Kindness Day!\n\n"
     "What's the kindest thing a stranger has done for you?", False),
    (41, "pagi2", "ruthie", "26°C and I'm a sheep\nin a full wool coat.\nI live on the kitchen tiles now.",
     "Ruthie in a white tank top and denim shorts, pink daisy behind her ear, lying flat on her back on cool white kitchen floor "
     "tiles with her arms and legs spread out like a starfish, an ice pack on her forehead, a little fan on the floor blowing "
     "her caramel wool, a glass of iced water beside her, bright hot midday sunlight through the window",
     "Wool: great in winter, questionable in November 🥵🐑\n\nWhere's the coolest spot in your house?", False),
    (41, "malam", "friends", "The deck is finished.\nFinal safety test:\nBig Tama jumps on it.",
     "Long golden summer evening on a brand-new stained timber deck: Big Tama in a plain black rugby jersey caught mid-air in a "
     "huge joyful jump with his arms up, Eli in a mustard-yellow T-shirt, shorts and his navy pom-pom beanie and Ruthie in a "
     "floral sundress with her pink daisy behind her ear clutching each other on the lawn with eyes squeezed shut, Grandpa Ram "
     "in his flat cap and tweed waistcoat peering over the fence with a cup of tea and one bushy eyebrow raised, Mei hovering "
     "nearby filming in slow motion, festoon lights overhead, warm golden light",
     "It held. Not a single wobble 🪵💪 Thank you, Tama!\n\nWhat would you get a Big Tama to build for you?", False),

    # ---------- Sabtu 14 Nov (hari 42) - kemah DOC campsite, pantai pertama Big Tama ----------
    (42, "pagi", "friends", "Camping weekend.\nFitting Big Tama into the hatchback:\n45 minutes.",
     "Early-morning driveway: a small hatchback with its doors open, Big Tama in a black hoodie folded into the back seat with "
     "his knees up to his chin and his head bent sideways against the roof, a chilly bin and sleeping bags piled on his lap, "
     "Mei perched on his knee happily filming, Eli in a khaki fishing vest over a T-shirt, shorts and his navy pom-pom beanie "
     "pushing on the back door with his shoulder trying to shut it, Ruthie in a denim jacket and sunhat with her pink daisy "
     "behind her ear holding a camping lantern and a pillow, soft pink sunrise light",
     "Off to a DOC campsite for the weekend ⛺🚗 Tama says he's “totally comfortable.”\n\n"
     "Who always gets squished in the back seat?", False),
    (42, "pagi2", "friends", "Big Tama's first beach day.\nSunscreen needed:\none whole bottle. Per arm.",
     "Golden-sand New Zealand beach with turquoise water and blooming red pōhutukawa on the headland: Big Tama in giant floral "
     "board shorts standing patiently with his arms out and a thick white stripe of sunscreen on his nose, while Ruthie in a "
     "pink striped swimsuit and sunhat with her pink daisy behind her ear stands on top of a chilly bin squeezing a big bottle "
     "of sunscreen onto his enormous shoulder, Eli in board shorts, a rash vest and his navy pom-pom beanie holding two more "
     "bottles at the ready, Mei sitting on top of Big Tama's head under a tiny beach umbrella, bright midday sun",
     "Tama grew up on a high-country farm and had NEVER been to the beach 🏖️🐏 The NZ sun doesn't play, so we went in hard.\n\n"
     "Do you remember your first time at the beach?", False),
    (42, "malam", "couple", "Camping air mattress:\n9pm: luxury hotel.\n3am: a sheet of plastic on a rock.",
     "Inside a small tent at night lit by a warm hanging lantern: Eli in a camping hoodie and his navy pom-pom beanie and Ruthie "
     "in a fleece jumper with her pink daisy behind her ear lying wide awake side by side on a completely deflated air "
     "mattress sunk flat onto the ground, both staring up at the tent roof with blank exhausted faces, sleeping bags tangled, "
     "a small pump lying uselessly beside them, soft lantern glow",
     "Camping: where romance meets a slow leak ⛺😩\n\nAir mattress, stretcher or just the ground?", False),

    # ---------- Minggu 15 Nov (hari 43) ----------
    (43, "pagi", "couple", "Sandy wool. Salty air.\nGood friends.\nThank You for all of it.",
     "Eli in a navy hooded fleece and his navy pom-pom beanie and Ruthie wrapped in a cream knitted blanket with her pink daisy "
     "behind her ear walking slowly hand in hand along the edge of a quiet golden beach at sunrise, their little hoofprints "
     "trailing behind them in the wet sand, gentle waves rolling in, a few tents tucked among the grassy dunes behind, soft "
     "pink and gold sky reflecting on the water, peaceful grateful smiles",
     "Sunday reminder 🐑🤍\n\n“In every thing give thanks: for this is the will of God in Christ Jesus concerning you.” "
     "— 1 Thessalonians 5:18 (KJV)\n\nBig blessings, small blessings, sandy blessings: thank Him for them all today.", True),
    (43, "pagi2", "friends", "Camping hack:\nbring a fantail.\nSandflies: 0.",
     "Shady DOC campsite beside a clear river in native bush: Eli in a T-shirt, shorts and his navy pom-pom beanie lounging "
     "blissfully in a camp chair with his eyes closed and a mug of coffee, while Mei zips and swoops all around his head with "
     "her tail fanned wide, snapping up tiny sandflies mid-air like a little superhero, Big Tama in the background in a black "
     "singlet cooking sausages on a small camping gas cooker, tents and tree ferns behind, dappled midday sunlight",
     "Fantails really do follow you around to catch the bugs you stir up 🐦✨ Mei takes it personally.\n\n"
     "What's your best sandfly defence?", False),
    (43, "malam", "couple", "Home from camping.\nWe brought back souvenirs:\n3kg of sand. In the wool.",
     "Evening in a small laundry: Eli in an old T-shirt and his navy pom-pom beanie and Ruthie in a beach cover-up with her pink "
     "daisy behind her ear vigorously shaking out their curly wool, sand pouring out of it and forming little dunes around "
     "their hooves on the floor, a broom propped hopelessly in the corner, sandy towels piled in the washing machine, warm "
     "evening light",
     "We'll be finding sand until Easter 🏖️😂\n\nBeach or camping: where do you bring home the most sand?", False),

    # ---------- Senin 16 Nov (hari 44) - alur float Santa parade dimulai ----------
    (44, "pagi", "eli", "Mid-November at work:\nevery email now ends with\n“let's pick this up in the new year.”",
     "Eli in a short-sleeved white business shirt, a loosened navy tie and his navy pom-pom beanie leaning way back in his "
     "office chair with his hooves up on the desk, sunglasses pushed up on his beanie, sipping an iced coffee through a straw, "
     "a little desk fan ruffling his wool and a small potted succulent beside his laptop (seen from behind), sunny open-plan "
     "office, bright morning light",
     "Brains are officially in summer mode 😎📧\n\nIs your workplace winding down yet?", False),
    (44, "pagi2", "friends", "Pip needed a float for the Santa parade.\nShe asked Big Tama nicely.\nHe never stood a chance.",
     "Sunny front lawn: Pip in a pink T-shirt, denim shorts and her yellow gumboots holding up a big crayon drawing of a "
     "sparkly gold sleigh and gazing up with huge pleading puppy-dog eyes, Big Tama in his orange hi-vis vest kneeling down to "
     "her level with one hoof over his heart, completely melted, Eli in a T-shirt and his navy pom-pom beanie in the "
     "background shaking his head knowingly, bright midday light",
     "First she got me in an elf suit, now she's got Tama 🎅🛷 Pip is unstoppable.\n\n"
     "Who in your life can talk you into anything?", False),
    (44, "malam", "ruthie", "Online order: “arrives in 3–5 days.”\nMe: checks the tracking\nevery 11 minutes.",
     "Ruthie in pastel striped summer pyjamas with her pink daisy behind her ear lying on her tummy on the bed at night, chin "
     "propped on one hoof, face lit by the glow of her phone, eyes narrowed in impatient concentration, an empty teacup and a "
     "half-eaten bag of lollies on the bedside table, soft lamp light",
     "It's been “in transit” for two days. WHERE is it going? 📦😤\n\nAre you a tracking-checker too?", False),

    # ---------- Selasa 17 Nov (hari 45) ----------
    (45, "pagi", "couple", "Pōhutukawa season:\nstunning trees.\nI am now a pink sheep.",
     "Eli in a white T-shirt, shorts and his navy pom-pom beanie standing under a huge blooming crimson pōhutukawa tree by the "
     "sea, his white wool and his beanie completely dusted with thousands of fallen red stamens so he looks fluffy and pink, "
     "arms out and looking down at himself in bewilderment, Ruthie in a white linen dress with her pink daisy behind her ear "
     "laughing and taking a photo of him on her phone, the footpath carpeted in red fluff, sparkling blue harbour behind, "
     "bright morning sun",
     "NZ's Christmas tree is in full bloom 🌺 and apparently so am I.\n\nIs your local pōhutukawa flowering yet?", False),
    (45, "pagi2", "eli", "Exam season.\nI finished uni years ago.\nI still dream I forgot one.",
     "Dreamlike scene: Eli in striped pyjamas and his navy pom-pom beanie sitting alone at a single wooden exam desk in the "
     "middle of a vast empty exam hall, rows of empty desks fading into a soft haze around him, staring in pure panic at a "
     "blank sheet of paper with a pencil trembling in his hoof, strange pale dreamy light",
     "Good luck to everyone sitting end-of-year exams right now 📚🍀 You've got this.\n\n"
     "Do you still get the exam dream?", False),
    (45, "malam", "friends", "Building the parade float.\nDay 1: we bought glitter.\nDay 2: we are the glitter.",
     "Big garage workshop at night under bright work lights: a half-built sleigh float on a flat trailer, Big Tama in a black "
     "singlet holding a giant paintbrush, Pip in denim overalls and yellow gumboots with a tub of glue, Eli in an old T-shirt "
     "and his navy pom-pom beanie, all three completely covered head to hoof in sparkly gold glitter, Big Tama's thick cream "
     "wool shimmering like a disco ball, Mei shaking glitter off her fanned tail, paint tins and cardboard stars everywhere, "
     "warm sparkly light",
     "Glitter is forever ✨😂 Parade is this Saturday!\n\nTeam Glitter or Team Never Again?", False),

    # ---------- Rabu 18 Nov (hari 46) ----------
    (46, "pagi", "eli", "First cicadas of summer.\nDay 1: “Ahh, the sound of summer.”\nDay 3:",
     "Eli in a sky-blue singlet, shorts, sunglasses and his navy pom-pom beanie lying in a rope hammock between two trees in a "
     "sunny back yard, pressing both hooves over his ears with an anguished, exhausted face, a cold drink tipping out of the "
     "hammock, a few cicadas clinging to the tree bark right beside his head, hazy hot morning sunlight",
     "Summer's soundtrack has arrived 🦗🔊\n\nLove the cicadas or need earplugs?", False),
    (46, "pagi2", "ruthie", "Christmas pav practice #3:\ncracked, sunk and leaning.\nIt's called “rustic.”",
     "Ruthie in a cherry-print apron with her pink daisy behind her ear in a sunny kitchen proudly presenting a cracked, sunken, "
     "leaning pavlova on a cake stand, piled high with whipped cream, strawberries, kiwifruit and passionfruit to hide the "
     "cracks, a smear of cream on her nose, eggshells and mixing bowls everywhere and two more collapsed pavlovas behind her, "
     "bright midday light",
     "Christmas Day is the final exam 🍓😤 Five more weeks of practice.\n\nWhat's your secret to a perfect pav?", False),
    (46, "malam", "friends", "Nana Dot is knitting Big Tama\na Christmas jumper.\nShe's on ball of wool 27.",
     "Cosy cottage lounge in the evening: Big Tama in a grey T-shirt sitting very still on a sturdy wooden stool with a shy, "
     "delighted smile and his arms held out, Nana Dot in her lilac cardigan, pearls and reading glasses standing on tiptoe on "
     "a kitchen chair stretching a tape measure across his enormous shoulders, Grandpa Ram in his flat cap on a small "
     "stepladder on the other side holding the end of the tape and peering over his round glasses, mountains of red and green "
     "wool balls covering the floor and the couch, warm lamplight",
     "Nana Dot doesn't do things by halves 🧶🎄\n\nWhat's the best handmade gift you've ever been given?", False),

    # ---------- Kamis 19 Nov (hari 47) ----------
    (47, "pagi", "friends", "Mei posted Big Tama vs the wētā.\n2.4 million views.\nTama is “not talking about it.”",
     "Mei's cosy corner café in the morning: Mei hovering excitedly over the counter with her tail fanned, proudly holding up "
     "her tiny phone, Eli in a striped T-shirt and his navy pom-pom beanie and Ruthie in a lemon-yellow sundress with her pink "
     "daisy behind her ear leaning in and laughing, while Big Tama in a black rugby jersey sits squeezed onto a tiny café chair "
     "in the corner, trying to hide his huge face behind a tiny coffee cup, soft morning light",
     "Our gentle giant is officially internet famous 📱🦗😂\n\n"
     "What's the most embarrassing video of you that exists?", False),
    (47, "pagi2", "eli", "Work Secret Santa.\nI drew the boss.\n$20 limit. No pressure.",
     "Eli in a short-sleeved business shirt, a navy tie and his navy pom-pom beanie standing in an open-plan office holding a "
     "tiny folded slip of paper and staring at it in pure horror, a red Santa hat full of folded paper slips on the desk beside "
     "him, a strand of silver tinsel along the desk partition, colleagues blurred in the background, bright midday office light",
     "What do you even buy the boss for $20?? 🎁😰 Ideas welcome.\n\n"
     "What's the best Secret Santa gift you've ever received?", False),
    (47, "malam", "couple", "Heard the ice cream van.\nWe're grown adults with a mortgage.\nWe sprinted.",
     "Warm summer dusk on a suburban street: Eli in a singlet, shorts and his navy pom-pom beanie and Ruthie in a floral sundress "
     "with her pink daisy behind her ear sprinting barefoot down the footpath side by side, waving coins, wool flying, faces "
     "full of childlike joy, a pastel-pink ice cream van with no logos parked further along the street with a small queue of "
     "children, golden-orange evening sky",
     "That jingle hits different at any age 🍦🏃\n\nWhat's your ice cream van order?", False),

    # ---------- Jumat 20 Nov (hari 48) ----------
    (48, "pagi", "ruthie", "Weekend forecast: 27°C.\nBought a paddling pool “for the nieces.”\nThere are no nieces.",
     "Ruthie in a pink polka-dot swimsuit, oversized sunglasses and a floppy sunhat with her pink daisy tucked behind one ear "
     "lounging blissfully in a small inflatable paddling pool on the back lawn, holding a cold lemonade with a tiny paper "
     "umbrella, the new stained timber deck behind her, a sprinkler sparkling in the background, bright sunny morning",
     "Self-care is a two-metre paddling pool 🏊‍♀️☀️\n\nWhat's your favourite way to cool down?", False),
    (48, "pagi2", "couple", "Her: “Let's keep December quiet.”\nThe calendar, already:",
     "Sunny kitchen: Eli in a T-shirt and his navy pom-pom beanie staring in disbelief at the fridge door, which is completely "
     "covered in blank cream party invitation cards, a wall calendar beside it with every single square plastered with "
     "colourful sticky notes, Ruthie in a sage-green blouse with her pink daisy behind her ear pinning up yet another card "
     "with a sheepish smile, bright midday light",
     "Silly season has officially begun 📅😅\n\nHow many end-of-year events are on your calendar?", False),
    (48, "malam", "friends", "Community Christmas tree night.\nMe: “Who's got the ladder?”\nBig Tama:",
     "Local park at dusk on a warm summer evening: Big Tama in a red-and-white striped T-shirt casually reaching up to place a "
     "glowing gold star on top of a tall Christmas tree covered in warm twinkling fairy lights, an unused ladder lying on the "
     "grass beside him, Mei hovering above the treetop filming with her tail fanned, Eli in shorts, a T-shirt and his navy "
     "pom-pom beanie and Ruthie in a red sundress with her pink daisy behind her ear cheering in a small happy crowd of sheep, "
     "deep blue twilight sky",
     "The tree is lit and the season has officially started 🎄✨\n\nHas your town lit its Christmas tree yet?", False),

    # ---------- Sabtu 21 Nov (hari 49) - Santa parade ----------
    (49, "pagi", "couple", "PYO strawberries:\n“a fun, relaxing family morning.”\nMy back, 40 minutes in:",
     "Sunny pick-your-own strawberry farm with long rows of plants: Eli in a T-shirt, shorts and a wide straw sunhat perched on "
     "top of his navy pom-pom beanie, bent over with one hoof pressed to his lower back and a pained grimace, holding a nearly "
     "empty bucket, while Ruthie in a gingham sundress with her pink daisy behind her ear skips ahead with a bucket "
     "overflowing with ripe red strawberries, bright morning sunshine",
     "Worth it for the strawberries. My back disagrees 🍓😩\n\nHave you been strawberry picking this season?", False),
    (49, "pagi2", "friends", "Santa parade day.\nMe: elf. Pip: head elf.\nBig Tama: pulled the float himself.",
     "Sunny main street lined with a cheering crowd: Big Tama in a black rugby jersey and a red Santa hat pulling a glittering "
     "gold sleigh float by a thick rope over his shoulder, Mei riding on top of his head and filming, Pip in a green elf "
     "costume standing on the float throwing lollies with total joy, Eli in a matching green elf costume with a jingle-bell "
     "collar but still wearing his navy pom-pom beanie instead of the elf hat, waving with a forced smile, Ruthie in a red "
     "sundress with her pink daisy behind her ear, Grandpa Ram and Nana Dot cheering from deck chairs on the kerb, bright "
     "midday summer sun",
     "Promised Pip, didn't I? 🎅🧝 A week of glitter, and Tama made it look easy.\n\n"
     "What's the best part of your local Santa parade?", False),
    (49, "malam", "friends", "Backyard cricket with Big Tama.\nHe hit it once.\nWe're still looking for the ball.",
     "Long golden summer evening in the back yard beside the new deck: Big Tama in a white T-shirt holding a cricket bat that "
     "looks like a toy in his enormous hooves, shading his eyes and gazing proudly up at the sky, Eli in shorts, a T-shirt, "
     "wicketkeeping gloves and his navy pom-pom beanie with his jaw dropped watching the ball vanish over the rooftops, Kiwi "
     "Kev, just woken up, in his black singlet and tiny gumboots wearing a head torch and ready to search, Mei darting off "
     "into the sky after the ball, a wheelie bin as the wicket, warm golden-hour light",
     "Six AND out. Kev's still out there with his head torch 🏏😂\n\nWhat are the backyard cricket rules at your place?", False),
]
