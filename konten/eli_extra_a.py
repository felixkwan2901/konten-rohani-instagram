"""@eliandruthie - post TAMBAHAN hari 1-21 (Minggu 4 Okt s/d Sabtu 24 Okt 2026), total 56 post.
Slot lama (pagi 07:00, pagi2 12:00, malam 20:00) tetap ada di eli_lamb.py / eli_lamb_w3.py; file ini hanya menambah:
  hari 1-7  : "sore" 15:00                                                        -> 7
  hari 8-14 : "pagi3" 09:00, "sore" 15:00                                         -> 14
  hari 15-21: "pagi3" 09:00, "siang0" 10:30, "sore" 15:00, "sore2" 17:00,
              "larut" 21:30 (larut = Reel, suasana cosy menjelang tidur)          -> 35
Bahasa Inggris, humor NZ yang hangat. Tidak ada post rohani di slot tambahan (faith selalu False);
momen kehidupan gereja boleh, dengan hormat.

Tokoh:
  - Hari 1-14 hanya Eli, Ruthie dan Grandpa Ram (Grandpa Ram dikenalkan hari 1 sore, pohon lemonnya).
  - Mulai hari 15 pakai FRIENDS dari eli_lamb_w3.py, mengikuti alur yang sudah ada:
    Nana Dot baru muncul setelah morning tea gereja hari 15 (12:00), Pip menginap hari 17 (mulai 12:00)
    sampai hari 20 (pulang 20:00), Kiwi Kev baru muncul setelah malam hari 19, road trip Rotorua hari 21
    (Kev jaga rumah).
Benang kecil: seri "Small things I love about her/him" (hari 5, 12, 16, 17), pakis bernama Gregory (5 -> 21),
lemon Grandpa Ram (1 -> 17), 3 alarm gereja (14 malam -> 15 pagi3), pencuri bekal makan siang
(15 sore2 -> 15 malam -> 15 larut -> 16 pagi3).
Eli SELALU pakai navy pom-pom beanie; Ruthie SELALU pakai pink daisy di belakang telinga.
Nama teman ditulis persis di adegan hanya kalau tokohnya memang ada di gambar.
Tanpa merek/logo dan tanpa tulisan/papan di adegan (teks meme ditambahkan otomatis)."""

# (hari, slot, who, teks meme, adegan untuk prompt gambar, caption, rohani?)
# who = "eli" | "ruthie" | "couple" | "friends"; faith selalu False
DATA_A = [
    # ================= MINGGU 1: 1 tambahan/hari, slot "sore" 15:00 =================
    # ---------- Minggu 4 Okt (hari 1) ----------
    (1, "sore", "friends", "Grandpa Ram: “Take a few lemons.”\nA few:",
     "Sunny Sunday afternoon in a semi-rural back yard: Grandpa Ram in his brown tweed flat cap, round wire-rimmed glasses and "
     "tweed waistcoat leaning over the low wooden fence with a kind, proud smile, having just handed over an enormous bulging "
     "sack of bright yellow lemons, a big lemon tree heavy with fruit behind him; Eli in a cream cable-knit jumper and his navy "
     "pom-pom beanie staggering under the weight of the sack with wide eyes, a few lemons tumbling out and rolling across the "
     "green lawn, warm golden afternoon light",
     "Everyone, meet Grandpa Ram 👴🍋 Our neighbour, our honorary grandpa, and owner of the most generous lemon tree in "
     "Aotearoa.\n\nDoes your neighbour have a lemon tree too?", False),

    # ---------- Senin 5 Okt (hari 2) ----------
    (2, "sore", "ruthie", "Hung the washing out in the sunshine.\nThe sky took that personally.",
     "Ruthie in a lilac raincoat over a striped T-shirt, pink daisy behind her ear, racing across a back lawn towards a rotary "
     "clothesline full of flapping towels and sheets with her arms stretched out to grab them, as a dark grey rain cloud dumps "
     "a sudden shower right over the clothesline while the sun still shines on the rest of the yard, a plastic laundry basket "
     "abandoned on the grass, dramatic spring afternoon light",
     "Monday washing day, NZ edition 🌦️🧺\n\nHow many times have you raced the rain to the line this week?", False),

    # ---------- Selasa 6 Okt (hari 3) ----------
    (3, "sore", "eli", "Someone ate my yoghurt\nfrom the work fridge.\nI trust no one now.",
     "Eli in a light-blue work shirt, a navy tie and his navy pom-pom beanie standing in a small office kitchenette holding the "
     "shared fridge door wide open, an empty gap on the shelf where his yoghurt should be, squinting over his shoulder with "
     "narrowed suspicious eyes like a detective, blurred colleagues innocently sipping coffee in the background, a kettle and "
     "mismatched mugs on the bench, flat afternoon office light",
     "The investigation continues 🕵️🥄\n\nHas your lunch ever gone missing at work?", False),

    # ---------- Rabu 7 Okt (hari 4) ----------
    (4, "sore", "couple", "I loaded the dishwasher.\nShe reloaded the dishwasher.\nWe don't talk about it.",
     "Bright home kitchen in the afternoon: Ruthie in a sage-green jumper with her pink daisy behind her ear bent over an open "
     "dishwasher, calmly rearranging every plate and bowl with precision, while Eli in a grey hoodie and his navy pom-pom beanie "
     "stands behind her holding a single mug, his face a mix of offence and quiet acceptance, sunlight through the kitchen window",
     "Apparently there's a system 🍽️😅\n\nWho's the dishwasher boss in your house?", False),

    # ---------- Kamis 8 Okt (hari 5) ----------
    (5, "sore", "couple", "Small things I love about her:\nshe names every plant in the house\nand says good morning to each one.",
     "Cosy sunroom full of potted plants on shelves and windowsills: Ruthie in a soft pink cardigan with her pink daisy behind "
     "her ear gently watering a big leafy fern with a little copper watering can and smiling at it as if chatting to an old "
     "friend, Eli in a navy jumper and his navy pom-pom beanie leaning in the doorway with a mug of tea, watching her with a "
     "soft, adoring smile, warm afternoon sunshine streaming in",
     "Small things I love about her, part 1 🪴💕 (The fern is called Gregory.)\n\n"
     "What's a small thing you love about your person?", False),

    # ---------- Jumat 9 Okt (hari 6) ----------
    (6, "sore", "friends", "Me: 15 minutes trying to\nreverse the trailer.\nGrandpa Ram: one go, one hoof, mid-biscuit.",
     "Gravel driveway on a sunny Friday afternoon: a small trailer full of garden clippings now reversed perfectly straight up "
     "against the shed, Grandpa Ram in his tweed flat cap, round glasses and tweed waistcoat sitting in the driver's seat of an "
     "old hatchback with the window down, one hoof casually on the steering wheel and a half-eaten gingernut biscuit in the "
     "other, Eli in a checked flannel shirt, work gloves and his navy pom-pom beanie standing beside the car with his jaw "
     "dropped, zig-zagging tyre tracks all over the gravel from his failed attempts, warm afternoon light",
     "The tip run took two hours. One hour forty-five of that was me reversing 😅🚗\n\nCan you reverse a trailer?", False),

    # ---------- Sabtu 10 Okt (hari 7) ----------
    (7, "sore", "eli", "First club cricket game of the season.\nWhites: ironed.\nOut: first ball.",
     "Sunny village cricket ground with a white picket fence and a small wooden pavilion: Eli in crisp cricket whites, batting "
     "pads and his navy pom-pom beanie trudging slowly back towards the pavilion with his bat tucked under his arm and a deeply "
     "dejected face, the stumps scattered on the pitch behind him, green outfield, blue spring sky, bright afternoon sun",
     "Cricket season is back, and so is my batting average 🏏😩\n\nPlaying any summer sport this year?", False),

    # ================= MINGGU 2: 2 tambahan/hari, "pagi3" 09:00 dan "sore" 15:00 =================
    # ---------- Minggu 11 Okt (hari 8) ----------
    (8, "pagi3", "couple", "Church starts at 10.\nWe live 4 minutes away.\nWe left at 9:59.",
     "Sunny Sunday morning outside a small white wooden country church: Eli in a pale-blue collared shirt, a navy knitted vest "
     "and his navy pom-pom beanie half-jogging across the gravel car park with a Bible under one arm and his shirt tail "
     "untucked, Ruthie in a floral tea dress and white cardigan with her pink daisy behind her ear hurrying beside him while "
     "fastening an earring, both grinning sheepishly, the church door just swinging shut ahead of them, spring blossom trees "
     "and soft morning light",
     "We'll slide into the back row, nobody will notice 😅⛪\n\nAre you an early-to-church person or a just-in-time person?", False),
    (8, "sore", "ruthie", "Same scone recipe as Mum.\nHers: soft little clouds.\nMine: could break a window.",
     "Ruthie in a red gingham apron over a cream jumper, pink daisy behind her ear, standing in a sunny Sunday-afternoon kitchen "
     "with flour on her cheek, knocking on a pale rock-hard scone with her hoof as if it were a door, a tray of flat lumpy "
     "scones on the bench beside a recipe card lying face down, a butter dish and a jar of jam, warm afternoon light",
     "What is the secret?? I'm begging 🥲\n\nCheese scones or date scones?", False),

    # ---------- Senin 12 Okt (hari 9) ----------
    (9, "pagi3", "eli", "Spring: time to get summer-ready.\nGym, day 1, minute 6:",
     "Bright modern gym with mirrors and rubber floors: Eli in a grey tracksuit, a white sweatband on his wrist and his navy "
     "pom-pom beanie lying flat on his back on a yoga mat like a starfish, completely exhausted and staring at the ceiling, a "
     "tiny pink dumbbell beside him and a full untouched water bottle, other gym-goers blurred in the background, morning light "
     "through big windows",
     "New week, new me. Same knees 😮‍💨🏋️\n\nWhat's your favourite way to keep fit?", False),
    (9, "sore", "friends", "Asked Grandpa Ram if I could borrow a spade.\nGot a 40-minute tour of his shed.\nAnd the spade's life story.",
     "Inside a dusty, cosy old garden shed crammed with neatly hung tools, jars of screws, coils of wire and seed trays, sunlight "
     "streaming through a cobwebby window: Grandpa Ram in his tweed flat cap, round wire-rimmed glasses and tweed waistcoat "
     "holding up an old wooden-handled spade like a treasured heirloom and pointing to it lovingly mid-story, Eli in a navy "
     "puffer vest over a T-shirt and his navy pom-pom beanie standing politely beside him with a patient, slightly glazed smile, "
     "warm late-afternoon light",
     "I know a lot about spades now 👴🔧 (I still don't have the spade.)\n\nWho in your family has the best shed?", False),

    # ---------- Selasa 13 Okt (hari 10) ----------
    (10, "pagi3", "ruthie", "The barista started my order\nbefore I even said hello.\nI've never felt so seen.",
     "Cosy neighbourhood café with a wooden counter, a gleaming espresso machine, a cabinet of muffins and scones and pot plants "
     "on the shelves: Ruthie in a camel wool coat and a cream scarf, pink daisy behind her ear, standing at the counter with her "
     "hooves pressed to her heart and a touched, beaming face as a friendly barista sheep in a black apron slides a ready-made "
     "coffee across the counter to her, plain white cups with no logos, soft golden morning light through the front window",
     "Regular status: unlocked ☕🥹\n\nDoes your barista know your order?", False),
    (10, "sore", "couple", "Me with a sniffle:\n“Tell everyone I was brave.”\nHer: “It's a cold.”",
     "Cosy lounge in the afternoon: Eli lying on the couch wrapped in three blankets, in flannel pyjamas and his navy pom-pom "
     "beanie, a thermometer in his mouth, a mountain of crumpled tissues around him and one hoof draped dramatically across his "
     "forehead like a tragic hero, Ruthie in a cosy oatmeal jumper with her pink daisy behind her ear standing over him holding a "
     "steaming bowl of soup and rolling her eyes with a fond smile, soft grey afternoon light through the window",
     "Spring colds hit different when you're dramatic 🤧😂\n\nWho's the bigger sook when they're sick in your house?", False),

    # ---------- Rabu 14 Okt (hari 11) ----------
    (11, "pagi3", "couple", "Her, “guiding” me into a park:\n“Heaps of room! Heaps!”\nThere was no room.",
     "Busy little main street lined with cafés on a bright morning: Eli in a navy rain jacket and his navy pom-pom beanie behind "
     "the wheel of a small hatchback wedged at an awkward angle between two parked cars, one back wheel up on the kerb and his "
     "eyes wide with panic, while Ruthie in a mustard-yellow coat with her pink daisy behind her ear stands on the footpath "
     "confidently waving him back with both hooves, two amused passers-by watching, morning sunshine",
     "Our marriage survived. The kerb did not 🚗😅\n\nWho's the better parker in your relationship?", False),
    (11, "sore", "ruthie", "Planted my spring lettuces.\nThe snails: “Thank you\nfor the lovely dinner.”",
     "Small backyard vegetable garden in spring: Ruthie in denim gardening overalls, floral gardening gloves and a straw sunhat, "
     "pink daisy behind her ear, crouched beside a raised garden bed staring in dismay at a row of baby lettuce seedlings "
     "nibbled into lace, a fat garden snail sitting contentedly on one leaf, a trowel and a watering can beside her, soft "
     "afternoon sunlight",
     "Round one to the snails 🐌🥬\n\nWhat's your trick for keeping snails off the veggies?", False),

    # ---------- Kamis 15 Okt (hari 12) ----------
    (12, "pagi3", "eli", "WOF day.\nMy car is 19 years old.\nWe're both nervous.",
     "Small mechanic's workshop waiting area: Eli in an olive-green bomber jacket and his navy pom-pom beanie perched on a "
     "plastic chair, nervously clutching a paper cup of instant coffee and jiggling one leg, staring through a big window at his "
     "old silver hatchback raised up on a hoist with a mechanic in overalls inspecting underneath, a dusty pot plant and a "
     "water cooler beside him, bright morning light",
     "Come on, old girl. You've got this 🚗🤞\n\nHow old is your car?", False),
    (12, "sore", "couple", "Small things I love about him:\nhe makes my tea exactly right\nwithout ever having to ask.",
     "Sunny window seat piled with cushions in a cosy living room: Ruthie in a soft blue knitted jumper with her pink daisy "
     "behind her ear curled up with a book, looking up with a soft, warm smile as Eli in a grey cardigan and his navy pom-pom "
     "beanie carefully carries a floral cup of tea on a saucer with two biscuits balanced on the side, concentrating hard so "
     "he won't spill, golden afternoon light",
     "Small things I love about him, part 1 (from Ruthie) 🫖💕 Milk in, one sugar, two biscuits. Every time.\n\n"
     "What's a small thing your person always gets right?", False),

    # ---------- Jumat 16 Okt (hari 13) ----------
    (13, "pagi3", "eli", "Friday shared morning tea at work.\nEveryone: homemade cakes and slices.\nMe: one packet of biscuits.",
     "Office break room with a long table covered in a lavish shared morning tea: a tall homemade sponge cake with cream and "
     "strawberries, trays of caramel slice, fresh scones with jam and a quiche, while Eli in a crisp white shirt, a navy knitted "
     "tie and his navy pom-pom beanie places a single plain unbranded packet of biscuits at the very end of the table with an "
     "awkward, embarrassed smile, blurred colleagues admiring the cakes, bright morning office light",
     "It's the thought that counts, right? 🍪😅\n\nWhat do you bring to a shared morning tea?", False),
    (13, "sore", "friends", "Gave Grandpa Ram a page of\nwatering instructions for the weekend.\nHe made it into a paper plane.",
     "Sunny afternoon at the wooden fence between two back yards: Grandpa Ram in his tweed flat cap, round wire-rimmed glasses "
     "and tweed waistcoat launching a neatly folded paper plane into the air with a cheeky twinkle in his eye, Eli in a navy "
     "hoodie and his navy pom-pom beanie on the other side of the fence watching it glide away with his mouth open, pots of "
     "herbs and seedlings on a little garden table beside him, blue sky, warm afternoon light",
     "Fair enough. He was growing things before I was born 👴🌱 Our plants are in good hooves this weekend.\n\n"
     "Have you ever over-explained something to an expert?", False),

    # ---------- Sabtu 17 Okt (hari 14) ----------
    (14, "pagi3", "couple", "Her: in the car at 8 sharp.\nMe at 9:40: “Has anyone seen my sunnies?”\n(They were on my beanie.)",
     "Sunny suburban driveway on a Saturday morning: Ruthie in a denim jacket and a straw sunhat with her pink daisy behind her "
     "ear sitting in the passenger seat of a packed little hatchback with her seatbelt on, tapping her watch and pointing up at "
     "Eli's head with an exasperated laugh, while Eli in a red puffer vest, shorts and his navy pom-pom beanie stands at the open "
     "front door frantically patting his pockets, a pair of sunglasses perched right on top of his beanie the whole time, "
     "bright morning sun",
     "Weekend away, take two 😎🙃\n\nWhat do you always lose right before you leave the house?", False),
    (14, "sore", "couple", "Asked the little country dairy\nfor a single scoop.\nThis is a single scoop.",
     "Outside a quaint little country dairy with a wooden veranda and a bench, rolling green hills behind: Ruthie in a white "
     "T-shirt and a sunhat with her pink daisy behind her ear holding an ice-cream cone with an enormous towering scoop as big as "
     "her head, eyes wide with delight, Eli in a sweaty hiking T-shirt, shorts, hiking boots and his navy pom-pom beanie beside "
     "her with an equally giant cone, licking a drip off the side, both a bit dusty and very happy after a long walk, sunny "
     "afternoon light, no signs",
     "Country dairy scoops are a national treasure 🍦🇳🇿 We earned it after that “two-hour” walk.\n\n"
     "What's the biggest scoop you've ever been given?", False),

    # ================= MINGGU 3: 5 tambahan/hari =================
    # "pagi3" 09:00, "siang0" 10:30, "sore" 15:00, "sore2" 17:00, "larut" 21:30 (Reel, cosy)
    # ---------- Minggu 18 Okt (hari 15) ----------
    (15, "pagi3", "eli", "Watched a bow tie tutorial\nfour times.\nResult:",
     "Hallway mirror on a bright Sunday morning: Eli in a crisp white shirt, a navy blazer and his navy pom-pom beanie staring "
     "at his reflection in defeat, his little red bow tie twisted into a lopsided tangled knot under his chin with one end "
     "sticking straight out, his phone propped against the mirror with the screen facing away, polished church shoes by the "
     "door, warm morning light",
     "Ruthie fixed it in ten seconds 🎀 And the three alarms worked: we're EARLY for once ⛪\n\nCan you tie a bow tie?", False),
    (15, "siang0", "friends", "Grandpa Ram doesn't need the hymn book.\nHe's sung bass from the same pew\nsince 1968.",
     "Inside a small white wooden country church filled with soft morning sunlight through tall clear windows, simple wooden "
     "pews: Grandpa Ram in a brown tweed jacket, his flat cap respectfully held against his chest and round glasses on his nose, "
     "singing with his eyes closed and a deep, joyful, rumbling expression, a closed hymn book resting on the pew beside him, "
     "Eli next to him in his navy blazer, red bow tie and navy pom-pom beanie holding a hymn book and gazing up at him in awe, "
     "gentle golden light",
     "Some voices just make a building feel like home 🎶👴\n\nWho's the voice you can always pick out at your church?", False),
    (15, "sore", "couple", "Sunday beach walk.\nShe collects the shells.\nI carry the shells.",
     "Wide golden-sand beach on a breezy spring afternoon, gentle waves and a grassy headland: Ruthie in a white linen shirt with "
     "rolled-up sleeves and cropped trousers, pink daisy behind her ear, crouching happily to pick up yet another seashell, "
     "while Eli in a navy windbreaker, rolled-up chinos and his navy pom-pom beanie walks barefoot beside her with both hooves "
     "cupped full of shells and his jacket pockets bulging with more, a patient, amused smile, wool ruffled by the sea breeze, "
     "bright afternoon sunshine",
     "First beach walk of the season 🐚🌊 We now own 74 shells.\n\nAre you a shell collector or a shell carrier?", False),
    (15, "sore2", "couple", "Sunday 5pm: meal prep done.\nFive lunches, ready for the week.\nOne lamb is watching them very closely.",
     "Tidy home kitchen in the late afternoon: Ruthie in a lemon-yellow apron over a striped top, pink daisy behind her ear, "
     "proudly snapping the lid onto the last of five neat glass lunch containers of pasta salad lined up on the bench, while "
     "behind her Eli in a grey T-shirt and his navy pom-pom beanie peeks around the doorframe with big hungry eyes fixed on the "
     "containers, a fork already in his hoof, warm golden late-afternoon light",
     "Nothing suspicious here 👀🍱 (Stay tuned tonight.)\n\nWhat's your favourite work lunch?", False),
    (15, "larut", "eli", "9:30pm.\nThe suspect is asleep\nwith a fork in his hoof. Case closed.",
     "Cosy dim bedroom at night: Eli in navy flannel pyjamas and his navy pom-pom beanie fast asleep on his back under a thick "
     "duvet with a blissful, satisfied smile, a fork still loosely held in one hoof on top of the covers, a few pasta crumbs on "
     "his chin and pillow, a small bedside lamp casting a warm glow, moonlight through the curtains",
     "I still tucked him in 😴🍴 (He's making his own lunch tomorrow.)\n\nWho's the late-night snacker in your house?", False),

    # ---------- Senin 19 Okt (hari 16) ----------
    (16, "pagi3", "ruthie", "Monday, 9:01am:\nchecking my lunch\nis still in my bag.",
     "Open-plan office in the morning: Ruthie in a cream blouse and a navy cardigan, pink daisy behind her ear, sitting at her "
     "desk peeking cautiously into her work bag at a glass lunch container with narrowed, suspicious eyes and the hint of a "
     "relieved smile, a laptop with the screen facing away and a mug of tea on the desk, blurred colleagues behind, soft "
     "morning office light",
     "After last night, I trust no one 🍱👀\n\nDo you have to hide your snacks at home?", False),
    (16, "siang0", "eli", "Her text: “Call me when you get a sec.”\nMe: imagining 40 worst-case scenarios.\nHer: “Pasta or curry tonight?”",
     "Eli in a navy quarter-zip jumper over a collared shirt and his navy pom-pom beanie sitting frozen at his office desk, "
     "staring at his phone with huge panicked eyes and a bead of sweat on his brow, a half-eaten muesli bar dropped on the "
     "keyboard, colleagues blurred in the background, bright mid-morning office light",
     "My heart can't take these texts 📱😰\n\nWhat's the scariest text your partner can send you?", False),
    (16, "sore", "friends", "Nana Dot's Monday:\naqua aerobics, op shop shift, choir practice.\nMy Monday: one bus ride and a nap.",
     "Sunny suburban street in the afternoon: Nana Dot in a lilac tracksuit, her pearl necklace and gold reading glasses on a "
     "beaded chain, power-walking briskly past the front fence with a sports bag over one shoulder and a rolled-up swim towel "
     "under her arm, waving cheerily, while Eli in a grey hoodie and his navy pom-pom beanie sits slumped on the front porch step "
     "holding a mug of tea with tired, heavy-lidded eyes, spring flowers in the front garden, bright late-afternoon light",
     "Retirement looks exhausting 😅👵 Where does she get the energy?\n\nWho's the busiest retiree you know?", False),
    (16, "sore2", "ruthie", "Social netball, week one.\nI forgot you can't run with the ball.\nThree times.",
     "Outdoor netball court in the early evening: Ruthie in a plain teal netball dress and white sneakers with her pink daisy "
     "behind her ear, caught mid-stride sprinting down the court with the ball tucked under her arm and a huge joyful grin, "
     "completely unaware, while a blurred umpire behind her blows a whistle and teammates face-palm, golden light and long "
     "shadows, no letters or numbers on any clothing",
     "I was just so excited 🏐😂\n\nHave you ever played netball?", False),
    (16, "larut", "couple", "Our bedtime routine:\none chapter, read out loud.\nHe does all the voices. Badly. Perfectly.",
     "Cosy bedroom at night lit by a warm bedside lamp: Eli in flannel pyjamas and his navy pom-pom beanie sitting up against the "
     "pillows reading a thick hardback adventure novel aloud with a big dramatic expression and one hoof raised mid-performance, "
     "Ruthie in soft pink pyjamas with her pink daisy behind her ear snuggled under the duvet against his shoulder, eyes sleepy "
     "and smiling, a mug of cocoa on the bedside table",
     "Small things I love about him, part 2 📖💕 (Tonight the dragon had a Southland accent.)\n\nDo you read before bed?", False),

    # ---------- Selasa 20 Okt (hari 17) - Pip datang jam 12 ----------
    (17, "pagi3", "couple", "The good towels are out.\nI've lived here four years\nand never touched the good towels.",
     "Bright, freshly made-up spare bedroom in the morning: Ruthie in a lilac knitted cardigan with her pink daisy behind her ear "
     "and a tissue tucked up her sleeve proudly placing fluffy white towels folded into a swan on the guest bed, a vase of fresh "
     "spring flowers and a little bowl of chocolates on the bedside table, while Eli in his navy Fair Isle jumper and his navy "
     "pom-pom beanie reaches longingly towards the towels from the doorway as Ruthie lightly swats his hoof away, soft morning "
     "sunlight",
     "Someone special is coming to stay… 👀 More at lunchtime.\n\nDo you have “guest towels” nobody's allowed to use?", False),
    (17, "siang0", "friends", "Grandpa Ram and Nana Dot at bowls:\nmarried 52 years.\nStill won't let each other win.",
     "Immaculate green lawn bowls club on a sunny spring morning, a white wooden clubhouse behind: Nana Dot in crisp bowls whites, "
     "her pearl necklace and gold reading glasses on a beaded chain doing a little triumphant hoof pump as her bowl rests right "
     "against the small white jack, Grandpa Ram in white bowls clothes with his tweed flat cap and round glasses crouched beside "
     "the jack with a tape measure, squinting suspiciously, bright morning sunshine",
     "Love, honour and measure every single shot 👵👴💚\n\nWho's the most competitive couple you know?", False),
    (17, "sore", "eli", "The sisters have been reunited\nfor three hours.\nI'm having my tea in the garden now.",
     "Peaceful back garden in the afternoon: Eli in his navy Fair Isle jumper and his navy pom-pom beanie sitting on an upturned "
     "bucket among the vegetable beds with a mug of tea and a calm, serene face, eyes half closed, while far behind him through "
     "the open lounge window two blurry lamb shapes, one caramel with a tiny pink flower and one honey-blonde, are jumping up and "
     "down and hugging, spring sunshine and a lemon tree over the fence",
     "Love them both. Also love my quiet garden 🫖😂\n\nWhere do you go for five minutes of peace?", False),
    (17, "sore2", "friends", "Pip met Grandpa Ram over the fence.\nFive minutes later she was calling him Grandpa.\nHe's pretending not to love it.",
     "Sunny late afternoon at the wooden fence between the back yards: Pip in her bright pink raincoat and yellow gumboots "
     "standing on an upturned crate to reach over the fence, chattering excitedly and hugging a bag of lemons, Grandpa Ram in his "
     "flat cap, round glasses and tweed waistcoat on the other side trying to keep a straight face but clearly beaming, Eli in "
     "his navy Fair Isle jumper and navy pom-pom beanie and Ruthie in her lilac cardigan with her pink daisy behind her ear "
     "watching from the lawn and smiling, golden late-afternoon light",
     "Grandpa Ram has gained another grandkid 👴💕 (She also left with a bag of lemons.)\n\n"
     "Do you have an “adopted” grandparent?", False),
    (17, "larut", "couple", "Sister sleepover night.\nShe still popped in to say goodnight\nand straighten my beanie.",
     "Cosy dark bedroom at night lit by a small bedside lamp: Eli in striped pyjamas and his navy pom-pom beanie sitting up in bed "
     "with a book on his lap, smiling with his eyes closed as Ruthie in pink pyjamas with her pink daisy behind her ear leans in "
     "from the side of the bed to gently straighten his beanie and kiss the top of it, the warm glow of fairy lights spilling "
     "in from the lounge through the half-open door",
     "Small things I love about her, part 2 💕 (Then she went straight back to the party.)\n\nWhat's your goodnight ritual?", False),

    # ---------- Rabu 21 Okt (hari 18) - Pip menginap ----------
    (18, "pagi3", "eli", "Three lambs, one bathroom.\nOur guest's “quick shower”:\nminute 41.",
     "Narrow hallway in the morning: Eli in a grey T-shirt with a towel slung over his shoulder and his navy pom-pom beanie "
     "leaning against the wall outside a closed bathroom door with a toothbrush in his mouth, staring at his watch with a flat, "
     "defeated face, clouds of steam pouring out from under the door, a pink shower cap hanging on the door handle, soft "
     "morning light",
     "I leave for work in six minutes 🚿😩\n\nHow long is a “quick shower” in your house?", False),
    (18, "siang0", "friends", "Nana Dot is teaching Pip to knit.\nThe plan: a scarf.\nSo far: one very big knot.",
     "Nana Dot's cosy cottage lounge in the morning with lace curtains and a floral armchair: Pip in a pink hoodie sitting "
     "cross-legged on the rug completely tangled in bright pink yarn, holding up a lumpy knotted ball of wool on two needles with "
     "a proud, hopeful grin, Nana Dot in her lilac cardigan, pearls and reading glasses on a beaded chain leaning forward from "
     "the armchair with a patient, twinkly smile, a teapot and a plate of biscuits on a side table, soft morning light",
     "Nana Dot says everyone's first one looks like this 🧶😂\n\nCan you knit, or are you more of a “big knot” person?", False),
    (18, "sore", "ruthie", "Avocado shopping:\nrock, rock, rock, rock…\nmush.",
     "Supermarket produce section in the afternoon: Ruthie in a camel trench coat with her pink daisy behind her ear holding an "
     "avocado up to her ear and gently squeezing it with intense, narrowed-eyed concentration, a small basket on her arm, a big "
     "pile of avocados in front of her, other shoppers blurred, bright store lighting, no logos",
     "There's a four-minute window and I always miss it 🥑😩\n\nRipen them on the bench or in a paper bag?", False),
    (18, "sore2", "friends", "Pip made us dinner!\nEvery pot, pan and bowl we own: used.\nDinner: cheese on toast.",
     "Chaotic home kitchen in the early evening, every bench piled high with dirty pots, pans, mixing bowls and a flour-dusted "
     "chopping board: Pip in a frilly pink apron over her pink hoodie proudly presenting three plates of golden cheese on toast "
     "with a huge beaming smile, Eli in a grey T-shirt and his navy pom-pom beanie and Ruthie in a camel trench coat with her "
     "pink daisy behind her ear, just home from work, standing in the doorway with their jaws dropped but trying to smile, warm "
     "evening light",
     "It was honestly delicious 🧀🍞 The dishes took two hours.\n\nWhat's your “can't be bothered” dinner?", False),
    (18, "larut", "couple", "The spare room is next to ours.\nHer little sister snores like a tractor.\nHer: “She does NOT snore.”",
     "Dark cosy bedroom at night lit only by moonlight and a dim bedside lamp: Eli in tartan flannel pyjamas and his navy pom-pom "
     "beanie lying in bed with a pillow pressed over his ears and his eyes wide open in exhausted disbelief, Ruthie in matching "
     "tartan pyjamas with her pink daisy behind her ear lying beside him with her eyes peacefully closed and a serene, innocent "
     "little smile, the shared wall right behind the headboard",
     "Family loyalty is a powerful thing 😴🚜\n\nWho's the loudest snorer in your family?", False),

    # ---------- Kamis 22 Okt (hari 19) - Pip menginap; Kiwi Kev baru muncul jam 20:00 ----------
    (19, "pagi3", "friends", "Pip is helping Grandpa Ram feed the chooks.\nThe chooks have never been so excited.\nGrandpa Ram has never been so tired.",
     "Sunny morning in Grandpa Ram's farmyard next door: Pip in her bright pink raincoat and yellow gumboots joyfully flinging "
     "handfuls of grain into the air like confetti, a flurry of brown and speckled hens flapping and clucking all around her, "
     "Grandpa Ram in his flat cap, round glasses and tweed waistcoat leaning on a wooden rake beside the chicken coop with a "
     "tired but fond smile, a few feathers floating in the air, fresh golden morning light",
     "Nine eggs today. Grandpa Ram says that's a record 🐔💛\n\nDid you grow up with chooks?", False),
    (19, "siang0", "ruthie", "Spring in NZ:\nmagpie season.\nThis is how I walk to the shops now.",
     "Leafy suburban footpath on a bright mid-morning: Ruthie in a pastel blue blouse and white jeans with her pink daisy behind "
     "her ear walking briskly while holding an open pink umbrella low over her head on a completely sunny day, eyes darting "
     "sideways at a black-and-white magpie perched on a power line above her, a cautious, determined face, tall trees and "
     "spring blossom, bright sunshine",
     "Swooping season is no joke 🐦☂️ It's protecting its babies. I'm protecting my wool.\n\nHave you ever been swooped?", False),
    (19, "sore", "couple", "Her: “Look at this gorgeous vintage jumper\nI found at the op shop!”\nMe: “That's mine. You donated it.”",
     "Cluttered, cheerful op shop with racks of second-hand clothes, shelves of old crockery and a basket of knitted toys: Ruthie "
     "in a pastel blue blouse with her pink daisy behind her ear holding up a chunky green knitted jumper with a delighted face, "
     "Eli in his orange hi-vis vest, flannel shirt and his navy pom-pom beanie, on his way home from work, standing beside her "
     "pointing at the jumper with an incredulous, half-laughing face, soft afternoon light through the shop window, no signs",
     "Paid $6 to buy back my own jumper 🧶😂 I'm keeping it this time.\n\nHave you ever bought something back by accident?", False),
    (19, "sore2", "couple", "Her: “How was your day?”\nMe: a 20-minute story\nabout my smoko sandwich.",
     "Kitchen in the early evening: Eli still in his orange hi-vis vest, flannel shirt and his navy pom-pom beanie standing at the "
     "bench gesturing passionately with both hooves held wide apart to show the size of a sandwich, eyes shining with "
     "excitement, Ruthie in a pastel blue blouse with her pink daisy behind her ear, her curls still a little frizzy, leaning on "
     "the bench with her chin in her hoof and listening with a patient, amused, loving smile, a pot simmering on the stove, "
     "warm evening light",
     "She listened to the whole thing. That's love 🥪💕\n\nWhat's the most boring story you've told with total passion?", False),
    (19, "larut", "friends", "Pip declared it spa night.\nI was not consulted.\n(My pores have never looked better.)",
     "Cosy lounge at night lit by fairy lights and candles: Eli in a fluffy white bathrobe with a pink spa headband pulled over "
     "his navy pom-pom beanie, a green face mask on and cucumber slices over his eyes, sitting stiffly upright on the couch "
     "between Ruthie (fluffy white robe, green face mask, pink daisy behind her ear) and Pip (pink robe, green face mask, fluffy "
     "fringe clipped back), who are both relaxed and giggling, a bowl of cucumber slices and mugs of herbal tea on the coffee "
     "table, soft warm glow",
     "Honestly? I'd do it again 🧖‍♂️🥒\n\nWould you join a spa night?", False),

    # ---------- Jumat 23 Okt (hari 20) - hari terakhir Pip, persiapan Labour Weekend ----------
    (20, "pagi3", "ruthie", "The fuel light came on Tuesday.\nIt's Friday.\nWe're still going. Somehow.",
     "Ruthie in a denim jacket with sunglasses pushed up on her head, pink daisy behind her ear, behind the wheel of a small car "
     "on a suburban road in the morning, gripping the steering wheel with both hooves and a tight nervous smile, glancing down "
     "at the dashboard where the fuel needle sits below empty and a little orange warning light glows, bright morning sun "
     "through the windscreen",
     "Filling up before the road trip, I promise ⛽😬\n\nHow far do you push it after the light comes on?", False),
    (20, "siang0", "eli", "Friday before a long weekend:\nphysically at work.\nMentally already in Rotorua.",
     "Office desk on a sunny Friday morning: Eli in a short-sleeved light-blue business shirt, a travel neck pillow already "
     "around his neck and sunglasses perched on his navy pom-pom beanie, leaning back in his chair with his chin on his hoof and "
     "a dreamy, far-away smile, gazing out of the window, a packed backpack under the desk and a laptop with the screen facing "
     "away left untouched, bright mid-morning light",
     "Three-day weekend loading… 🚗♨️\n\nWhat are your Labour Weekend plans?", False),
    (20, "sore", "friends", "Asked Kev to house-sit this weekend.\nHe said yes.\nWe think. He was asleep.",
     "Kiwi Kev's shady front porch next door in the middle of the afternoon: Kiwi Kev in his black singlet and tiny black "
     "gumboots fast asleep curled up in a woven hammock with a sleep mask over his eyes and his long beak resting on a cushion, "
     "while Eli in a navy hoodie and his navy pom-pom beanie tiptoes beside the hammock holding out a spare house key on a "
     "little ring and a folded sheet of paper, whispering, dappled afternoon sunlight through the trees",
     "Kev's a night bird, so we'll try again at 11pm 🥝🔑\n\nAre you a morning person or a night owl?", False),
    (20, "sore2", "friends", "Pip is packing to go home.\nHer suitcase now includes\nthree of Ruthie's cardigans.",
     "Spare bedroom in the late afternoon: Pip in her bright pink raincoat sitting on top of an overstuffed suitcase trying to "
     "zip it shut with a sweet, innocent smile, a lilac cardigan sleeve and a pink cardigan sleeve poking out of the zip, Ruthie "
     "in a soft cream cardigan with her pink daisy behind her ear standing with her hooves on her hips and one eyebrow raised, "
     "recognising her own cardigans, Eli in his navy Fair Isle jumper and navy pom-pom beanie kneeling and pushing the suitcase "
     "lid down with both hooves, trying not to laugh, warm golden light",
     "Sisters share everything. Whether you agree or not 😂🧶\n\nDo you “borrow” your sibling's clothes?", False),
    (20, "larut", "couple", "The spare room's quiet again.\nUnder the pillow she left us a drawing:\nthree lambs and about forty hearts.",
     "Spare bedroom at night lit by a soft bedside lamp, the bed neatly made: Ruthie in a soft cream cardigan over pyjamas with "
     "her pink daisy behind her ear sitting on the edge of the bed holding a child-like crayon drawing of three little lambs "
     "(one white with a navy beanie, one caramel with a pink flower, one honey-blonde in a pink raincoat) surrounded by lots of "
     "red and pink hearts, no words on it, Eli in his navy Fair Isle jumper and navy pom-pom beanie sitting beside her with his "
     "arm around her, both smiling with misty eyes",
     "Already counting down to the next visit 🥹💕\n\nWhat's the sweetest thing a sibling has ever left for you?", False),

    # ---------- Sabtu 24 Okt (hari 21) - Labour Weekend, road trip ke Rotorua (Kev jaga rumah) ----------
    (21, "pagi3", "couple", "Road trip rule:\nthe driver picks the music.\nRuthie: “Cute rule.”",
     "Inside a small hatchback on an open country highway in the morning: Ruthie in a denim jacket and her straw sunhat with her "
     "pink daisy behind her ear singing her heart out into a banana like a microphone with her eyes closed and one hoof in the "
     "air, Eli in a navy puffer vest, sunglasses and his navy pom-pom beanie driving with a patient, long-suffering half-smile, "
     "a phone plugged into the dashboard with the screen hidden, green farmland rolling past the windows, bright morning sun",
     "Three hours of her playlist. I know all the words now 🎤🚗\n\nDriver picks the music: yes or no?", False),
    (21, "siang0", "eli", "Road trip stop:\na giant sheep made of corrugated iron.\nFamily photo, obviously.",
     "Small country town main street on a sunny late morning: Eli in a navy puffer vest, shorts, sunglasses and his navy pom-pom "
     "beanie standing proudly in front of a huge building shaped like a sheep made entirely of crinkly corrugated iron, copying "
     "its pose with his chin up and chest out, blue sky, a few parked cars, bright sunshine, no signs",
     "Had to stop for a family photo 🐑📸 (If you know, you know.)\n\nWhat's your favourite big roadside thing in NZ?", False),
    (21, "sore", "couple", "Her: “I'll keep you company\nthe whole drive.”\nHer, ten minutes later:",
     "Inside a small car on a sunny afternoon country highway: Ruthie in her denim jacket fast asleep in the passenger seat with "
     "her straw sunhat tipped down over half her face, mouth slightly open, her caramel wool squished against the window and her "
     "pink daisy peeking out from under the hat brim, empty lolly bags on her lap, Eli in his navy puffer vest, sunglasses and "
     "his navy pom-pom beanie driving and glancing at her with a soft, fond smile, rolling green hills and a distant lake "
     "through the windscreen, warm afternoon light",
     "Best road trip company ever 😴🚗💕\n\nWho falls asleep first on road trips in your family?", False),
    (21, "sore2", "friends", "Kev's house-sitting update, 5pm:\n“Just woke up.\nHouse is still here.”",
     "Cosy suburban lounge in the late afternoon with the curtains still drawn and golden light peeking through: Kiwi Kev in an "
     "oversized fluffy dressing gown and his tiny black gumboots, eyes still half shut and mid-yawn, watering a big leafy potted "
     "fern with a teacup while holding a tiny phone out at arm's length to take a sleepy selfie",
     "That's all we needed to hear, Kev 😂🥝 (Gregory the fern says hi.)\n\nWould you trust your neighbour with your plants?", False),
    (21, "larut", "couple", "Long weekend, night one.\nNo alarms tomorrow.\nI could cry.",
     "Cosy motel room at night: Eli in navy flannel pyjamas and his navy pom-pom beanie and Ruthie in pink pyjamas with her pink "
     "daisy behind her ear tucked up in bed under a thick white duvet, both holding mugs of hot chocolate, Ruthie's head resting "
     "on Eli's shoulder, blissful sleepy smiles, soft lamp light, a window beside the bed showing gentle wisps of geothermal "
     "steam drifting past the streetlights outside",
     "A sleep-in has never felt so close 😴💕\n\nWhat's your favourite part of a long weekend?", False),
]
