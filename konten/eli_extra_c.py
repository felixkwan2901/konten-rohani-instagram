"""@eliandruthie - post EXTRA minggu 6-7: Minggu 8 Nov s/d Sabtu 21 Nov 2026 (hari 36-49), 5 extra/hari = 70 post.
Melengkapi konten/eli_lamb_w6.py (slot utama pagi 07:00, pagi2 12:00, malam 20:00). Slot extra (waktu NZ):
  "pagi3" 09:00, "siang0" 10:30, "sore" 15:00, "sore2" 17:00, "larut" 21:30 (larut = Reel, suasana tidur yang cozy).
Bahasa Inggris, humor NZ yang wholesome. Semua faith=False (rohani Minggu sudah ada di slot utama); momen gereja boleh.

Mengikuti alur cerita w6 (urutan jam dijaga supaya tidak bentrok dengan post utama):
  - 36 Diwali (rangoli dengan tetangga, manisan), Mei baru muncul jam 12 -> extra pagi belum ada Mei/Big Tama
  - 37-41 bangun dek dengan Big Tama (sepatu bot raksasa, Mei pindah ke kepala Tama, Grandpa Ram "mandor pagar",
    sepupu wētā di gudang, siput, bekal chilly bin, Nana Dot akhirnya punya lawan), 41 World Kindness Day
  - 42-43 kemah DOC + pantai (tenda dua orang, istana pasir ber-dek, bisikan Big Tama, ibadah di tepi sungai)
  - 44-49 float Santa parade (rapat rencana, kostum elf tidak muat -> topi Santa, naik float untuk anak-anak),
    video wētā viral (47), Natal +-1/3 minggu 7 (Advent, kartu, Secret Santa teman, paduan suara carols, jumper Nana Dot)
Komposisi: friends 29 (+-41%), couple 18, ruthie 12, eli 11. Nama teman ditulis persis di adegan (Big Tama, Mei,
Grandpa Ram, Nana Dot, Kiwi Kev, Pip) supaya deskripsi FRIENDS/FRIENDS_NEW ikut masuk ke prompt.
Eli SELALU pakai navy pom-pom beanie; Ruthie SELALU pakai bunga daisy pink. Tanpa merek dan tanpa tulisan di adegan."""

# (hari, slot, who, teks meme, adegan untuk prompt gambar, caption, rohani?)
# who = "eli" | "ruthie" | "couple" | "friends"
DATA_C = [
    # ---------- Minggu 8 Nov (hari 36) - Diwali ----------
    (36, "pagi3", "friends", "First hot Sunday at church.\nThe one pew under the ceiling fan?\nTaken since 8:45.",
     "Inside a small white wooden country church on a hot summer Sunday morning, sunlight pouring through tall arched "
     "windows: Grandpa Ram in a crisp short-sleeved checked shirt with his flat cap resting on his knee and Nana Dot in a "
     "lilac floral dress and pearls sitting smugly in the one wooden pew directly under a slowly turning ceiling fan, eyes "
     "closed in bliss as the breeze ruffles their wool, while Eli in a crisp white short-sleeved shirt, navy chinos and his "
     "navy pom-pom beanie and Ruthie in a cornflower-blue Sunday dress with a white Peter Pan collar, pink daisy behind her "
     "ear, stand in the aisle beside them looking hot, wilting and slightly betrayed, other sheep fanning themselves in the "
     "warm pews behind",
     "Church veterans know the best seat in the house 😅⛪ (Love you, Grandpa Ram & Nana Dot.)\n\n"
     "Where do you sit at church: front, middle or back?", False),
    (36, "siang0", "ruthie", "New summer sunglasses.\nNow every walk to the letterbox\nis a red carpet.",
     "Ruthie in a breezy coral sundress and huge glamorous white-framed sunglasses, pink daisy behind her ear, strutting "
     "down a sunny suburban front path towards a wooden letterbox like a film star, chin up, one hoof raised in a little "
     "wave, a light breeze lifting her caramel curls, a plump sparrow on the fence watching her completely unimpressed, "
     "bright late-morning summer sun",
     "Sunglasses on, confidence up 😎✨\n\nWhat's one small thing that instantly makes you feel fabulous?", False),
    (36, "sore", "couple", "Our neighbour taught us rangoli for Diwali.\nRuthie's half: a lotus.\nMy half: a very colourful puddle.",
     "Sunny front path of the house next door on a warm afternoon: the kind neighbour ewe in an elegant emerald-and-gold "
     "saree kneeling and gently guiding Ruthie's hoof as they sprinkle bright coloured powder and marigold petals into a "
     "beautiful symmetrical lotus rangoli, Ruthie in a coral dress with her pink daisy behind her ear concentrating "
     "happily, while on the other half Eli in a smart navy shirt and his navy pom-pom beanie kneels proudly beside a "
     "lopsided, smudged swirl of every colour mixed together, coloured powder all over his hooves and nose, a basket of "
     "little clay diyas waiting nearby, warm golden afternoon light",
     "Thank you for your patience, lovely neighbour 🪔🌸 She said mine was “very creative.”\n\n"
     "Have you ever tried making a rangoli?", False),
    (36, "sore2", "eli", "The deck builder starts tomorrow.\nMe, practising my\n“yep, solid joists, mate” face.",
     "Eli in a navy T-shirt, shorts and his navy pom-pom beanie standing in front of the bathroom mirror wearing a "
     "brand-new, completely empty tool belt with a carpenter's pencil tucked behind his ear and a shiny unused tape "
     "measure clipped on, hooves on hips, squinting and nodding at his reflection with an exaggerated knowing expression, "
     "warm late-afternoon light through a small window",
     "Must not let the builder find out I don't know what a joist is 🔨😅\n\n"
     "Are you genuinely handy, or a professional nodder?", False),
    (36, "larut", "couple", "Diwali sweets from next door.\n“Let's save some for tomorrow.”\n20 minutes later:",
     "Cosy bedroom at night: Eli in soft navy pyjamas and his navy pom-pom beanie and Ruthie in a pale-pink nightie with "
     "her pink daisy behind her ear sitting up in bed side by side, an empty decorative tray between them with only crumbs "
     "and a sticky syrup ring left, Eli caught mid-bite of the very last round golden ladoo, Ruthie licking syrup off her "
     "hoof with a guilty giggle, a borrowed clay diya glowing safely on the windowsill beside warm fairy lights, soft "
     "golden glow",
     "Thank you, neighbours 🪔💛 The sweets did not survive the night.\n\nWhat treat can you NEVER save for later?", False),

    # ---------- Senin 9 Nov (hari 37) - Big Tama datang ----------
    (37, "pagi3", "friends", "Big Tama politely took his boots off\nat the front door.\nI could live in one.",
     "Sunny front porch in the morning: Eli in a grey hoodie, track pants and his navy pom-pom beanie standing inside one "
     "of Big Tama's enormous dusty work boots, the boot coming up to his chest like a little tower, peering over the top "
     "with an astonished face, while Big Tama in his orange hi-vis vest and thick grey socks bends down with a shy "
     "apologetic smile, his other giant boot lying beside the doormat and dwarfing it, Ruthie in a white cotton sundress "
     "with her pink daisy behind her ear laughing in the doorway with a mug of tea, bright morning light",
     "Very polite. Very big 🥾🐏\n\nShoes off inside: is that the rule at your place?", False),
    (37, "siang0", "eli", "Working from home\nwhile the deck gets built.\nMy coffee hasn't stopped vibrating.",
     "Eli in a collared work shirt and his navy pom-pom beanie at a home office desk on a video call (laptop seen from "
     "behind), holding a strained professional smile while his coffee mug rattles and creeps across the desk with little "
     "ripples in the coffee, a framed photo knocked crooked and a pot plant trembling, a window behind him showing a sunny "
     "back yard with stacks of fresh timber, bright late-morning light",
     "“Sorry, can you say that again?” — me, every 30 seconds 💻🔨\n\n"
     "What's the noisiest thing that's ever interrupted your work call?", False),
    (37, "sore", "ruthie", "Packed away all my cardigans.\nThe weather, one hour later:\na southerly. 14°C.",
     "Ruthie in a thin white cotton sundress, pink daisy behind her ear, shivering beside a rain-streaked window with grey "
     "skies and trees bending in the wind outside, frantically digging through a big storage bag of folded pastel "
     "cardigans on the bedroom floor, one lilac cardigan half pulled out, her caramel wool puffed up against the chill, a "
     "mug of hot tea steaming on the windowsill, cool grey afternoon light",
     "NZ weather always knows when you pack the winter clothes 🌧️🧶\n\n"
     "Have you packed your winter clothes away yet, or are you wiser than me?", False),
    (37, "sore2", "friends", "Introduced Mei to Big Tama.\nShe landed on his head.\nShe lives there now.",
     "Back yard in warm late-afternoon light beside stacks of fresh timber: Big Tama in his orange hi-vis vest standing "
     "perfectly still with huge delighted eyes rolled upwards, afraid to move, while tiny Mei nestles in his fluffy woolly "
     "topknot like a cosy nest with her tail fanned, filming a selfie of the two of them on her tiny phone, Eli in a grey "
     "hoodie and his navy pom-pom beanie and Ruthie in a white cotton sundress with her pink daisy behind her ear holding "
     "takeaway coffees and grinning up at them, golden glow",
     "Our biggest friend and our tiniest friend, already inseparable 🐦🐏\n\n"
     "Who's the unlikely duo in your friend group?", False),
    (37, "larut", "couple", "Her bedtime routine: 11 steps.\nMine: 1.\nFall face-first onto the bed.",
     "Cosy bedroom at night: Ruthie in silky lilac pyjamas with her pink daisy behind her ear sitting at a little vanity "
     "covered in small jars of wool cream, a silk scrunchie and a jade roller, carefully patting cream onto her cheeks in "
     "the mirror, while behind her Eli in flannel pyjama shorts, a faded T-shirt and his navy pom-pom beanie lies "
     "face-down and starfished across the duvet, already asleep, one slipper still dangling from a hoof, warm bedside lamp "
     "glow",
     "And yes, the beanie stays on 🧶😴\n\nHow many steps is your bedtime routine?", False),

    # ---------- Selasa 10 Nov (hari 38) ----------
    (38, "pagi3", "friends", "Grandpa Ram has supervised the deck build\nsince 7am.\nTools lifted: 0. Cups of tea: 6.",
     "Sunny back yard with the old deck half pulled up: Grandpa Ram in his flat cap, round glasses and tweed waistcoat "
     "leaning comfortably on the wooden fence between the yards with a cup of tea, pointing helpfully with a biscuit, a "
     "teapot and five empty cups lined up on the fence post beside him, while Big Tama in his orange hi-vis vest carries "
     "an enormous stack of old deck boards on one shoulder with ease and Eli in work gloves, an old grey T-shirt and his "
     "navy pom-pom beanie staggers past under one single plank, bright morning sun",
     "Every Kiwi building site needs a fence supervisor 👴☕\n\nWho's the unofficial supervisor on your street?", False),
    (38, "siang0", "ruthie", "Outside: 26°C.\nOffice aircon: Antarctica.\n(Glad I kept one cardigan.)",
     "Bright modern city office: Ruthie in a sleeveless summer blouse with a lilac cardigan pulled tightly around her and "
     "a small knitted blanket over her knees, pink daisy behind her ear, hunched at her desk cradling a steaming mug of tea "
     "with a deadpan face, an air-conditioning vent blowing straight down on her and frosting the tips of her curls, while "
     "through the big window behind her the sunny street is full of sheep in shorts and sunhats, bright midday light",
     "Summer in the street, winter at my desk 🥶☀️\n\nIs your office freezing or boiling?", False),
    (38, "sore", "eli", "Found the wētā's cousin in the shed.\nI'm telling no one.\nBig Tama must never know.",
     "Dim, dusty garden shed lit by a beam of afternoon sunlight: Eli in an old grey T-shirt, work gloves and his navy "
     "pom-pom beanie standing very still with one hoof pressed to his lips in a 'shh' gesture, eyes darting sideways "
     "towards the door, while a big spiky brown wētā sits calmly on a shelf among old tins and flowerpots right at his eye "
     "level, cobwebs and garden tools around, conspiratorial mood",
     "What happens in the shed stays in the shed 🦗🤫\n\nWhat secret are you keeping to protect a friend?", False),
    (38, "sore2", "couple", "Too hot to cook.\nDinner tonight: watermelon.\nWe are adults. Apparently.",
     "Back steps of the house at golden hour beside the half-built timber deck frame: Eli in a white singlet, shorts and "
     "his navy pom-pom beanie and Ruthie in a lemon sundress with her pink daisy behind her ear sitting side by side, each "
     "biting into an enormous wedge of watermelon with juice dripping down their chins, a little pile of rinds and black "
     "seeds on a plate between them, both laughing, warm golden evening light",
     "Hydration AND dinner. Efficient 🍉😂\n\nWhat's your too-hot-to-cook dinner?", False),
    (38, "larut", "couple", "Light off.\nBzzzzzz.\nLight on. Nothing. Silence.",
     "Dim bedroom on a hot summer night with the window open: Eli in a white singlet, boxer shorts and his navy pom-pom "
     "beanie standing on the bed in a ninja pose holding a slipper high, scanning the ceiling with narrowed suspicious "
     "eyes, while Ruthie in a light cotton nightie with her pink daisy behind her ear sleeps peacefully beside him under a "
     "sheet with a sleep mask on, a tiny mosquito silhouetted against the bedside lamp glow just behind Eli's head, a "
     "little fan in the corner",
     "Summer's smallest villain 🦟😤 The window was open for ONE minute.\n\nTeam mosquito net or team slipper?", False),

    # ---------- Rabu 11 Nov (hari 39) ----------
    (39, "pagi3", "friends", "Big Tama stopped work for 20 minutes\nto move one snail\nout of the way. Very gently.",
     "Sunny back yard beside fresh pale timber deck joists in the morning: Big Tama in a plain black rugby jersey crouched "
     "low in the grass, holding a tiny garden snail on the very tip of his enormous hoof and carrying it ever so carefully "
     "towards a leafy garden bed, his huge face full of tender concentration, Eli in an orange singlet, board shorts and "
     "his navy pom-pom beanie crouched beside him holding out a lettuce leaf for the snail, dew sparkling on the grass, "
     "soft morning light",
     "Gentle giant. Emphasis on gentle 🐌💛\n\nWho's the softest 'tough' person you know?", False),
    (39, "siang0", "friends", "Mei asked Big Tama\nto film her latte art.\nResult: 47 photos of his thumb.",
     "Mei's sunny corner café with pastel tiles and pot plants: Big Tama in a plain black rugby jersey hunched over the "
     "counter, pinching Mei's tiny phone between two enormous hoof-fingers and squinting at it in total confusion, his "
     "giant thumb covering the whole camera, while Mei stands on the counter beside a flat white with a perfect latte-art "
     "fern, tail fanned and wings on hips, unimpressed, and Eli in an orange singlet, board shorts and his navy pom-pom "
     "beanie peeking over Big Tama's arm and laughing, bright late-morning light",
     "Tiny phone, giant hooves 📱🐏 Mei is reviewing her camera crew.\n\n"
     "Who takes the worst photos in your friend group?", False),
    (39, "sore", "ruthie", "Hung the towels out at lunch.\nDry by 1pm.\nThey can stand up on their own.",
     "Sunny back yard with a rotary clothesline: Ruthie in a red gingham apron over a summer dress, pink daisy behind her "
     "ear, holding up a bath towel so sun-baked and crispy that it stands stiffly upright by itself like a board, her eyes "
     "wide, other stiff towels sticking straight out sideways on the line, a peg between her teeth, bright hot afternoon "
     "sun and a cloudless blue sky",
     "Kiwi summer: free towel exfoliation included 🌞🧺\n\nCrispy towels or fabric-softener person?", False),
    (39, "sore2", "couple", "Her: “Let's not do presents this year.”\nMe: I've been married long enough\nto know that's a trap.",
     "Sunny lounge in the late afternoon: Ruthie in a sundress with her pink daisy behind her ear lounging on the couch, "
     "casually sipping iced tea with an innocent smile, while Eli in an olive polo shirt, shorts and his navy pom-pom "
     "beanie sits beside her with narrowed suspicious eyes, slowly noticing the corner of a beautifully wrapped present "
     "with a gold bow peeking out from under the cushion behind her, soft golden light",
     "I'm buying a present. I'm buying TWO presents 🎁😅\n\nDo you and your partner do Christmas presents?", False),
    (39, "larut", "friends", "9:30pm. We're off to bed.\nKiwi Kev, next door:\n“Morning!”",
     "Night time: Eli in flannel pyjamas and his navy pom-pom beanie and Ruthie in a pink nightie with her pink daisy "
     "behind her ear leaning sleepily out of their open bedroom window holding toothbrushes and yawning, while next door "
     "under a bright moon Kiwi Kev in his black singlet and tiny black gumboots stands on his porch wide awake and full of "
     "energy, stretching with a mug of coffee and a head torch on, waving cheerily up at them, moths around the porch "
     "light, starry deep-blue sky",
     "Different body clocks, same great neighbour 🥝🌙\n\nAre you a night owl or an early bird?", False),

    # ---------- Kamis 12 Nov (hari 40) ----------
    (40, "pagi3", "friends", "Smoko with the builder.\nMy lunch box: one sandwich.\nHis lunch box: a chilly bin.",
     "Sunny back yard, sitting side by side on the edge of freshly laid pale timber deck boards: Eli in a white polo "
     "shirt, shorts and his navy pom-pom beanie holding one small neat triangle sandwich and staring sideways in awe at "
     "Big Tama in his orange hi-vis vest, who has a huge chilly bin open on his lap packed with giant doorstop sandwiches, "
     "a whole loaf of bread, a bunch of bananas and a big flask, kindly holding out one enormous sandwich to Eli, bright "
     "morning sun",
     "He offered to share. One of his sandwiches would last me till Thursday 🥪🐏\n\n"
     "Are you a big-lunch or a little-lunch person?", False),
    (40, "siang0", "eli", "First iced coffee of summer.\nDrank it in 10 seconds.\nBrain freeze level: Southern Alps.",
     "Eli in a white polo shirt, shorts, sunglasses and his navy pom-pom beanie sitting on a sunny city bench clutching "
     "his forehead through his beanie with both eyes squeezed shut and mouth open in a silent scream, a tall iced coffee "
     "with a straw in his other hoof already nearly empty, condensation dripping, bright late-morning sun",
     "Lesson learned. Lesson will be forgotten tomorrow 🧊🥶\n\nIced coffee: yes or never?", False),
    (40, "sore", "friends", "Nana Dot has baked for us for years.\nThen she met Big Tama.\nShe's finally met her match.",
     "Sunny back yard beside the nearly finished timber deck in the afternoon: Nana Dot in her lilac cardigan, pearls and "
     "reading glasses on a beaded chain beaming with pure joy as she holds out a tray of golden scones, while Big Tama in "
     "his orange hi-vis vest pops a whole scone into his mouth in one bite, cheeks full, giving her a happy thumbs up, a "
     "tower of empty biscuit tins stacked beside him, Eli in a white polo shirt and his navy pom-pom beanie and Ruthie in "
     "a sundress with her pink daisy behind her ear each holding a single tiny crumb with mock-sad faces, warm afternoon "
     "light",
     "Nana Dot has never been happier 🧁👵 Tama has never been fuller.\n\nWho feeds everyone in your family?", False),
    (40, "sore2", "ruthie", "Bought my Christmas Day dress.\nIt's November 12.\nI've already worn it twice.",
     "Sunny bedroom in the late afternoon: Ruthie twirling joyfully in front of a full-length mirror in a red-and-white "
     "summer sundress with a tiny holly print, pink daisy behind her ear, the skirt flaring out, an open shopping bag and "
     "tissue paper on the bed, a pair of red sandals waiting on the floor, warm golden light",
     "It needed a test run. Two test runs 💃🎄\n\n"
     "Do you save new clothes for a special day, or wear them straight away?", False),
    (40, "larut", "friends", "Looked over the fence at 9:30pm.\nGrandpa Ram and Nana Dot,\nslow dancing in the kitchen.",
     "Warm summer night: through the glowing kitchen window of the cottage next door, Grandpa Ram in his checked shirt and "
     "Nana Dot in her lilac cardigan slow dancing cheek to cheek beside the sink, eyes closed and smiling; in the "
     "foreground on the dark back lawn by the fence, Eli in pyjamas and his navy pom-pom beanie, a few caramel-brown "
     "deck-stain splotches still on his white wool, and Ruthie in a nightie with her pink daisy behind her ear leaning on "
     "the fence watching with soft teary smiles, her head on his shoulder, stars twinkling above",
     "Over fifty years married and still dancing 🥹💕 That's the goal.\n\n"
     "What's the sweetest thing you've seen an older couple do?", False),

    # ---------- Jumat 13 Nov (hari 41) - World Kindness Day ----------
    (41, "pagi3", "friends", "World Kindness Day.\nKiwi Kev weeded Grandpa Ram's garden\nat 3am. Grandpa thinks it was elves.",
     "Early morning in the vegetable garden next door: Grandpa Ram in a tartan dressing gown, slippers and his flat cap "
     "standing amazed with his round glasses pushed up, teacup frozen mid-air, staring at perfectly weeded rows of "
     "tomatoes and lettuces, while a few steps away Kiwi Kev is curled up fast asleep in a wheelbarrow piled with pulled "
     "weeds, soil on his beak and his tiny head torch still on, Eli in a crisp light-blue work shirt, navy tie and his "
     "navy pom-pom beanie and Ruthie in a sundress with her pink daisy behind her ear peeking over the fence with hooves "
     "to their lips, soft golden morning light",
     "Kev's kindness works the night shift 🥝🌱 Happy World Kindness Day!\n\n"
     "What's a secret kindness someone once did for you?", False),
    (41, "siang0", "ruthie", "World Kindness Day:\ncold drinks on the porch for the couriers.\nOne did a little happy dance.",
     "Sunny front porch at midday: Ruthie in a white tank top and denim shorts, pink daisy behind her ear, smiling warmly "
     "as she sets down a small chilly bin full of ice, bottles of water and ice blocks beside the front step, while at the "
     "front gate a delivery driver ram in a plain grey polo shirt and cap, holding a parcel and a cold bottle, does a "
     "joyful little happy dance, bright hot summer sunlight",
     "It's hot out there and they work so hard 💛🧊\n\nWho's an everyday hero you'd like to thank today?", False),
    (41, "sore", "eli", "Let someone merge in traffic.\nThey gave me the little wave.\nI'm emotional.",
     "Eli in a crisp light-blue work shirt, navy tie and his navy pom-pom beanie behind the wheel of a small hatchback in "
     "afternoon traffic on a sunny suburban road, graciously gesturing for another small car to merge in front of him, a "
     "hoof waving thank-you out of the other car's window, Eli's eyes glistening with emotion and one hoof pressed to his "
     "heart, golden afternoon light",
     "The Kiwi thank-you wave fixes everything 🚗👋 Happy World Kindness Day!\n\nDo you always do the thank-you wave?", False),
    (41, "sore2", "couple", "World Kindness Day.\nI let her have the fan.\nThe whole fan. All evening.",
     "Hot lounge in the early evening: Ruthie in a floral sundress with her pink daisy behind her ear lounging blissfully "
     "in front of a little oscillating fan with her eyes closed, her caramel wool and daisy fluttering in the breeze, "
     "while Eli in a mustard-yellow T-shirt, shorts and his navy pom-pom beanie sits nobly beside her, sweating and "
     "fanning himself with a paper plate, wearing a brave, saintly smile, warm golden light through the window",
     "True love is giving up the fan 🌀🥵\n\nWhat's the most loving thing you've ever sacrificed?", False),
    (41, "larut", "friends", "First night on the new deck.\nNo phones. No noise.\nJust friends and a sky full of stars.",
     "Warm summer night on the brand-new stained timber deck: Big Tama in a plain black rugby jersey lying on his back and "
     "taking up most of the deck, Eli in a mustard-yellow T-shirt and his navy pom-pom beanie and Ruthie in a floral "
     "sundress with her pink daisy behind her ear lying beside him on cushions, all three gazing up at a sky full of stars "
     "and the Milky Way, Mei fast asleep in Big Tama's fluffy woolly topknot with her tail tucked in, festoon lights dimmed "
     "low, glasses of lemonade beside them, peaceful",
     "Thank you for the deck, Tama 🪵✨ Best seat in the house.\n\nWhat's your favourite way to end a big week?", False),

    # ---------- Sabtu 14 Nov (hari 42) - kemah DOC ----------
    (42, "pagi3", "couple", "Road trip rule:\nwe stop for every real fruit ice cream.\nEven at 9am.",
     "Rustic roadside berry farm stand in the countryside: Eli in a khaki fishing vest over a T-shirt, shorts and his navy "
     "pom-pom beanie and Ruthie in a denim jacket and sunhat with her pink daisy behind her ear standing beside a small "
     "packed hatchback, each holding a huge swirl of pink real-fruit ice cream in a waffle cone studded with berries, "
     "Ruthie with a dab of pink ice cream on her nose, rows of berry plants behind, bright morning sunshine",
     "Breakfast of road-trip champions 🍓🍦\n\nWhat's your must-stop spot on a road trip?", False),
    (42, "siang0", "friends", "Big Tama brought\na two-person tent.\nHe is both persons.",
     "Grassy DOC campsite clearing surrounded by native bush and tree ferns: Big Tama in a black hoodie lying inside a "
     "small green dome tent stretched tight around him like a sleeping bag, his huge hooves sticking out of one end and "
     "his head and woolly topknot poking out of the door, smiling peacefully, Mei sitting on the tent roof with her tail "
     "fanned and filming, Eli in a khaki fishing vest and his navy pom-pom beanie on his knees hammering in a tent peg, "
     "Ruthie in a denim jacket and sunhat with her pink daisy behind her ear holding a mallet and laughing, bright "
     "late-morning light",
     "We may need a bigger tent. Or a marquee ⛺🐏\n\nWhat's the funniest camping fail you've ever seen?", False),
    (42, "sore", "friends", "Big Tama built a sandcastle.\nIt has a deck.\nAnd building consent.",
     "Golden-sand beach with turquoise water in the afternoon: Big Tama in giant floral board shorts with a stripe of "
     "white sunscreen on his nose kneeling proudly beside an amazingly detailed sandcastle with a tiny driftwood deck, a "
     "little railing and shell steps, carefully checking it with a small spirit level, Mei standing on the tiny deck with "
     "her tail fanned like a proud homeowner, Eli in board shorts, a rash vest and his navy pom-pom beanie holding a "
     "bucket beside his own lumpy collapsed sand blob, Ruthie in a pink striped swimsuit and sunhat with her pink daisy "
     "behind her ear laughing, sparkling sea, bright afternoon sun",
     "Once a builder, always a builder 🏰🪵\n\nWhat's the best thing you've ever built on the beach?", False),
    (42, "sore2", "eli", "Jandal blowout on hot sand.\nCar: 300 metres away.\nThis is my villain origin story.",
     "Scorching golden beach in the late afternoon: Eli in board shorts, a rash vest and his navy pom-pom beanie hopping "
     "desperately across the hot sand on one hoof, holding up a broken jandal with its strap popped out, the other leg "
     "tucked up, face scrunched in agony, heat shimmer rising from the sand, a beach towel flapping over his shoulder and "
     "the car park far away beyond the dunes, bright low sun",
     "The hot-sand hop 🩴🔥 Every Kiwi knows the dance.\n\n"
     "Have you ever had a jandal blowout at the worst possible moment?", False),
    (42, "larut", "friends", "Campsite quiet time, 9:30pm.\nBig Tama's whisper:\nheard at the next campsite.",
     "DOC campsite at night lit by warm lanterns hanging between tents: Big Tama in a black hoodie crouched low with one "
     "enormous hoof cupped beside his mouth, whispering to Eli, whose wool and navy pom-pom beanie are blown back as if by "
     "a gust of wind, Eli in a camping hoodie squinting, Ruthie in a fleece jumper with her pink daisy behind her ear "
     "pressing a hoof to her lips going 'shhh', a few sleepy campers poking their heads out of a tent in the distance, "
     "Mei curled up asleep inside a tin camping mug, stars above the tree ferns",
     "He's trying his best 🤫🐏 The whole campsite now knows his marshmallow opinions.\n\n"
     "Who has the loudest 'whisper' you know?", False),

    # ---------- Minggu 15 Nov (hari 43) ----------
    (43, "pagi3", "friends", "Sunday at the campsite.\nOne ukulele, a riverbank\nand Big Tama singing bass.",
     "Morning at a DOC campsite beside a clear river with tree ferns and soft mist: a small circle of camp chairs, Eli in "
     "a navy hooded fleece and his navy pom-pom beanie strumming a ukulele, Ruthie wrapped in a cream knitted blanket with "
     "her pink daisy behind her ear singing with a gentle smile, Big Tama in a black hoodie singing with his eyes closed "
     "and a hoof on his heart, Mei perched on his head with her tail fanned, a few other camping sheep families joining in "
     "with mugs of tea, golden morning light through the bush",
     "No building, no pews, still church 🎶⛺ Some of our favourite Sundays happen outdoors.\n\n"
     "Have you ever worshipped somewhere unexpected?", False),
    (43, "siang0", "ruthie", "Camping morning:\nno emails, no alarms.\nJust a bellbird and a cup of tea.",
     "Ruthie in a fleece jumper and leggings, pink daisy behind her ear, sitting alone in a camp chair at the edge of a "
     "quiet river in native bush, cradling an enamel mug of tea in both hooves with her eyes closed and a peaceful smile, "
     "a small olive-green bellbird singing on a nearby branch, soft dappled sunlight and mist drifting over the water, "
     "calm and still",
     "Sometimes the best thing you can do is nothing at all 🍵🐦\n\nWhere do you go to switch off?", False),
    (43, "sore", "couple", "Tent out of the bag: 2 minutes.\nTent back in the bag:\nscientifically impossible.",
     "DOC campsite on a sunny afternoon: Eli in a T-shirt, shorts and his navy pom-pom beanie on his knees desperately "
     "stuffing a billowing green tent into a tiny drawstring bag, tent poles sticking out everywhere, while Ruthie in a "
     "beach cover-up and sunhat with her pink daisy behind her ear sits on top of the bulging pile of fabric trying to "
     "squash it down, both laughing and exasperated, the packed hatchback behind them, bright afternoon light",
     "Physics says it came out of there. I don't believe physics ⛺😩\n\nNeat packer or stuff-it-all-in packer?", False),
    (43, "sore2", "friends", "Driving home from camping.\nBig Tama fell asleep in 4 minutes.\nThe whole car leans left.",
     "A small hatchback driving along a winding country road through green hills in golden late-afternoon light, the whole "
     "car tilting noticeably to one side, Big Tama asleep in the back seat with his huge face squashed peacefully against "
     "the rear window, Mei asleep on the tip of his nose, and through the windscreen Eli in a T-shirt and his navy pom-pom "
     "beanie driving with a fond smile and Ruthie in a beach cover-up with her pink daisy behind her ear looking back at "
     "them and giggling",
     "Sweet dreams, big fella 😴🚗 Best camping weekend ever.\n\nWho always falls asleep on road trips?", False),
    (43, "larut", "couple", "Our own bed after camping.\nReal pillows. No rocks. No leaks.\nI might cry.",
     "Cosy bedroom at night: Eli in soft navy pyjamas and his navy pom-pom beanie and Ruthie in pastel pyjamas with her "
     "pink daisy behind her ear sinking deep into a puffy white duvet and fluffy pillows, eyes closed with blissful melted "
     "smiles, a few stray grains of sand sparkling on the pillowcase, warm bedside lamp glow",
     "Camping is great. Coming home is greater 🛏️😌\n\nWhat's the best part of coming home after a trip?", False),

    # ---------- Senin 16 Nov (hari 44) ----------
    (44, "pagi3", "friends", "Mei's café Christmas menu is out.\nThe gingerbread latte\ncomes iced. It's 26 degrees.",
     "Mei's sunny corner café freshly decorated for Christmas with tinsel along the counter, a tiny potted Christmas tree "
     "and red baubles hanging in the window: Mei hovering proudly beside a tall iced gingerbread latte topped with whipped "
     "cream and a little gingerbread sheep biscuit, tail fanned, Eli in a short-sleeved white business shirt, a loosened "
     "navy tie and his navy pom-pom beanie leaning on the counter with wide eyes, about to take the first sip, bright "
     "morning light",
     "Summer Christmas hits different 🎄🧊☕\n\nIced or hot: what's your festive drink?", False),
    (44, "siang0", "ruthie", "Bought an Advent calendar.\nIt's November 16.\nWe're already on day 9.",
     "Sunny kitchen in the late morning: Ruthie in a sage-green T-shirt and denim shorts, pink daisy behind her ear, "
     "holding a festive cardboard Advent calendar with several little paper doors already torn open, a chocolate in her "
     "hoof and a smear of chocolate on her lips, a guilty but unrepentant smile, a few empty foil wrappers on the bench, "
     "bright midday light",
     "It's called quality control 🎄🍫\n\nAdvent calendars: one door a day, or no rules?", False),
    (44, "sore", "eli", "Asked the dairy for a single scoop.\nThe Kiwi single scoop:",
     "Sunny afternoon outside a small corner dairy shop: Eli in a short-sleeved white business shirt, a loosened navy tie "
     "and his navy pom-pom beanie holding up a cone with a towering, wobbling mountain of creamy vanilla ice cream almost "
     "as tall as his head, gazing at it with wide astonished eyes, drips running down the cone onto his hoof, bright "
     "afternoon sun",
     "Single in name only 🍦😂 Kiwi dairies don't do small.\n\nWhat's your go-to ice cream flavour?", False),
    (44, "sore2", "friends", "Float planning meeting.\nPip's plan: one crayon drawing.\nBig Tama's plan: 14 pages, to scale.",
     "Eli and Ruthie's dining table in the late afternoon: Pip in a pink T-shirt, denim shorts and yellow gumboots kneeling "
     "on a chair proudly holding up her crayon drawing of a sparkly gold sleigh, Big Tama in his orange hi-vis vest "
     "squeezed onto a small dining chair carefully unrolling a thick stack of neat technical sketches of a sleigh float "
     "with a tiny pencil in his hoof, Mei perched on the lampshade above, Eli in a T-shirt and his navy pom-pom beanie "
     "holding a calculator with a lost expression, Ruthie in a sundress with her pink daisy behind her ear bringing a jug "
     "of lemonade, warm golden light",
     "Pip's the creative director. Tama's the engineer. I'm… holding a calculator 🛷📐\n\n"
     "Are you a big-picture person or a details person?", False),
    (44, "larut", "ruthie", "Too hot to sleep.\nNew bedtime routine:\nstand in front of the open fridge.",
     "Dark kitchen at night lit only by the cool glow of an open fridge: Ruthie in pastel striped summer pyjamas, pink "
     "daisy behind her ear, standing in front of it with her eyes closed in bliss, the cold air ruffling her caramel wool, "
     "holding a little bowl of strawberries, bare hooves on the cool tiles, moonlight through the window",
     "The fridge door alarm and I are not friends 🍓❄️\n\nWhat's your go-to late-night snack?", False),

    # ---------- Selasa 17 Nov (hari 45) ----------
    (45, "pagi3", "couple", "Christmas shopping status.\nHer: bought, wrapped, hidden.\nMe: “It's still November, babe.”",
     "Sunny bedroom in the morning: Ruthie in a white linen dress with her pink daisy behind her ear sitting proudly beside "
     "a neat tower of beautifully wrapped presents with ribbons and bows, holding a roll of shiny wrapping paper, while "
     "Eli in a white T-shirt, shorts and his navy pom-pom beanie, a few fallen red pōhutukawa stamens still caught in his "
     "wool, leans in the doorway sipping coffee with a relaxed shrug, bright morning light",
     "There's heaps of time. Right? Right?? 🎁😅\n\nEarly shopper or Christmas Eve legend?", False),
    (45, "siang0", "couple", "Summer moulting season.\nEmptied the vacuum cleaner.\nWe found a third sheep.",
     "Bright lounge in the late morning: Eli in a T-shirt, shorts and his navy pom-pom beanie and Ruthie in a linen "
     "sundress with her pink daisy behind her ear staring in shock at a clear-canister vacuum cleaner packed solid with "
     "fluffy white and caramel-brown wool, a huge fluffy two-tone wool ball the size of a lamb sitting on the rug beside "
     "it, little tufts of wool drifting across the floor like tumbleweeds, sunlight streaming in",
     "It's us. We're the problem 🐑🌀\n\nHow often do you vacuum in summer? Be honest.", False),
    (45, "sore", "eli", "Watering the lawn.\nAccidentally ran through the sprinkler.\nAccidentally did it 11 more times.",
     "Sunny back yard on a hot afternoon beside the new timber deck: Eli in board shorts, a white singlet and his navy "
     "pom-pom beanie leaping joyfully through the sparkling arc of a garden sprinkler, hooves in the air and a huge grin, "
     "water droplets glittering in the sunlight, damp wool, green lawn and bright blue sky",
     "Very important grown-up responsibilities 💦😆\n\nWhen did you last run through a sprinkler?", False),
    (45, "sore2", "ruthie", "Evening plan:\n10 peaceful minutes watering the garden.\nThe hose had other plans.",
     "Golden-hour vegetable garden: Ruthie in a sundress and gardening gloves with her pink daisy behind her ear, "
     "completely drenched, caramel curls dripping and flattened, frozen with her mouth open in shock as a kinked green "
     "garden hose bursts at the tap and sprays wildly in every direction, tomato plants and a watering can nearby, warm "
     "golden evening light glittering on the water",
     "Refreshing, actually 💦😂\n\nWho does the garden watering at your place?", False),
    (45, "larut", "couple", "Summer thunderstorm.\nHer: “I'm not scared.”\nAlso her:",
     "Dark bedroom during a summer thunderstorm, lightning flashing through the rain-streaked window: Ruthie in pink "
     "pyjamas with her pink daisy behind her ear clinging tightly to Eli under the duvet with wide eyes, Eli in striped "
     "pyjamas and his navy pom-pom beanie holding her protectively with a calm, smug little smile, a little gold glitter "
     "still sparkling in his wool, warm bedside lamp glow",
     "My job: be brave. Her job: squeeze 😂⛈️💕\n\nDo you love thunderstorms or hide from them?", False),

    # ---------- Rabu 18 Nov (hari 46) ----------
    (46, "pagi3", "friends", "Mei took one sip\nof Big Tama's coffee order.\nShe's been vibrating for an hour.",
     "Mei's sunny corner café in the morning: Mei a buzzing, slightly motion-blurred streak zipping around the room in "
     "loops with huge eyes and her tail fanned, little coffee splashes in the air, Big Tama in a grey T-shirt sitting at "
     "the counter beside a row of six empty espresso cups with a worried frown, Eli in a sky-blue singlet, sunglasses and "
     "his navy pom-pom beanie ducking as Mei whizzes past his head, bright morning light",
     "Tama's order: a six-shot flat white. Mei's new rule: never again ☕⚡\n\nHow many shots in your coffee?", False),
    (46, "siang0", "ruthie", "Writing Christmas cards.\nCard 1: a heartfelt letter.\nCard 40: “Merry Xmas, R.”",
     "Sunny dining table in the late morning: Ruthie in a cherry-print apron over a summer dress, pink daisy behind her "
     "ear, slumped in her chair surrounded by a mountain of blank Christmas cards and sealed envelopes, shaking out her "
     "writing hoof with an exhausted face, a pen in the other hoof, a cup of tea gone cold, bright midday light",
     "Started strong. Finished… efficient 🎄✉️\n\nDo you still send Christmas cards?", False),
    (46, "sore", "friends", "Big Tama asked to try my hammock.\nThe trees are now\n30cm closer together.",
     "Sunny back yard on a hot afternoon: two trees bent dramatically inwards towards each other, the rope hammock between "
     "them stretched all the way down to the grass, Big Tama in a grey T-shirt lying in it with a blissful smile, eyes "
     "closed and his bottom resting on the lawn, Eli in a sky-blue singlet, shorts and his navy pom-pom beanie standing "
     "beside one bent tree with both hooves on his head in horror, cicadas on the bark, hazy afternoon sun",
     "He said it was “the comfiest thing ever.” The trees disagree 🌳😂\n\n"
     "Where's the best afternoon nap spot at your place?", False),
    (46, "sore2", "couple", "Summer marriage test:\nwho refills the ice cube trays?\n(Not him.)",
     "Sunny kitchen in the late afternoon: Ruthie in a cherry-print apron with her pink daisy behind her ear standing at "
     "the open freezer holding up two completely empty ice cube trays with a long deadpan stare, while Eli in a sky-blue "
     "singlet, shorts and his navy pom-pom beanie stands beside her mid-sip of a tall glass full of ice cubes with a "
     "guilty, innocent face, golden afternoon light",
     "I take the last ice and I live with the guilt 🧊😇\n\nWho's the ice-tray refiller in your house?", False),
    (46, "larut", "couple", "Too hot to sleep inside.\nDragged the mattress out\nonto the new deck.",
     "Warm summer night on the new stained timber deck: Eli in a white singlet, pyjama shorts and his navy pom-pom beanie "
     "and Ruthie in a light cotton nightie with her pink daisy behind her ear lying side by side on a mattress under a "
     "thin sheet, a mosquito net draped from the festoon lights above, pointing up at the stars and smiling, a big bright "
     "moon, peaceful and cosy",
     "Best room in the house tonight 🌙✨ (Thanks again, Tama.)\n\nHave you ever slept outside on a hot night?", False),

    # ---------- Kamis 19 Nov (hari 47) ----------
    (47, "pagi3", "eli", "Big Tama's video: 2.4 million views.\nMy most-liked post ever:\na pie. 38 likes. 2019.",
     "Eli in a short-sleeved business shirt, a navy tie and his navy pom-pom beanie sitting at his office desk staring at "
     "his phone (screen seen from behind) with a deflated, slightly jealous face, chin resting on one hoof, a lonely "
     "half-eaten muesli bar beside his keyboard, bright morning office light",
     "Proud of you, Tama. A bit jealous. Mostly proud 📱😅\n\nWhat's your most-liked post ever?", False),
    (47, "siang0", "friends", "Secret Christmas project:\nNana Dot is teaching me to knit\na spare beanie for Eli. Shh.",
     "Cosy cottage lounge with lace curtains in the late morning: Nana Dot in her lilac cardigan, pearls and reading "
     "glasses on a beaded chain leaning over Ruthie's shoulder and gently guiding her hooves on the knitting needles, "
     "Ruthie in a lemon-yellow sundress with her pink daisy behind her ear concentrating hard with the tip of her tongue "
     "out, a small lumpy half-finished navy beanie with a tiny pom-pom on the needles, a basket of navy wool at their feet, "
     "Grandpa Ram in his flat cap standing lookout at the window with a cup of tea, warm sunlight",
     "Don't tell him 🧶🤫 (He never reads the captions anyway.)\n\nHave you ever made a handmade Christmas gift?", False),
    (47, "sore", "friends", "Big Tama: “I'm not talking about the video.”\nThe kids at the park:\n“Can we get a photo?!”",
     "Sunny local playground in the afternoon: Big Tama in a black rugby jersey crouched low on the grass with a shy, "
     "bashful smile while a crowd of excited little lambs in summer clothes hug his huge legs and climb onto his shoulders "
     "for a photo, one tiny lamb proudly holding up a plush toy wētā, Mei hovering in front of them filming with her tail "
     "fanned, Eli in a striped T-shirt and his navy pom-pom beanie and Ruthie in a lemon-yellow sundress with her pink "
     "daisy behind her ear watching and laughing, bright afternoon sun",
     "He's pretending to hate being famous. He's loving it 🐏📸\n\nWould you want to go viral, or hide forever?", False),
    (47, "sore2", "friends", "Big Tama joined our church choir\nfor Carols by Candlelight.\nThe low notes rattle the windows.",
     "Bright church hall at choir practice in the late afternoon: a small choir of sheep in summer clothes standing in "
     "rows holding unlit candles, Big Tama in a plain black rugby jersey in the back row with his head almost touching the "
     "ceiling beams, singing a deep low note with his eyes closed as the windows tremble, Eli in a short-sleeved shirt and "
     "his navy pom-pom beanie beside him with his wool vibrating, Ruthie in a lemon-yellow sundress with her pink daisy "
     "behind her ear trying not to giggle, Mei perched on an empty music stand conducting with her fanned tail, warm "
     "golden light",
     "Carols by Candlelight is going to be EPIC 🕯️🎶 The bass section: just Tama.\n\n"
     "What's your favourite Christmas carol?", False),
    (47, "larut", "eli", "Couldn't sleep.\nTried counting sheep.\nThey all wanted a chat.",
     "Dreamy moonlit bedroom: Eli in striped pyjamas and his navy pom-pom beanie lying wide awake in bed with the duvet "
     "pulled up to his chin and an exasperated face, while at the foot of the bed a line of fluffy little sheep wait to "
     "jump over a small wooden fence, one sheep stopped on top of the fence leaning on it and chatting to him, another "
     "waving, soft blue moonlight and a warm glowing bedside lamp",
     "Note to self: never count your own kind 🐑🌙\n\nWhat do you do when you can't sleep?", False),

    # ---------- Jumat 20 Nov (hari 48) ----------
    (48, "pagi3", "friends", "Nana Dot's jumper for Big Tama:\none sleeve finished.\nIt fits me as a sleeping bag.",
     "Cosy cottage lounge in the morning: Eli in a T-shirt and his navy pom-pom beanie standing completely inside one long "
     "red-and-green knitted jumper sleeve like a sleeping bag, only his face and beanie poking out the top, the cuff "
     "pooled around his hooves, Nana Dot in her lilac cardigan, pearls and reading glasses beaming proudly with knitting "
     "needles in hand, Ruthie in a floppy sunhat and summer dress with her pink daisy behind her ear taking a photo and "
     "laughing, mountains of red and green wool balls everywhere, warm sunlight through lace curtains",
     "One sleeve down. One sleeve, a body and a neck to go 🧶🎄 Go Nana Dot!\n\nDoes anyone in your family knit?", False),
    (48, "siang0", "eli", "First cherries of the season.\n$28 a kilo.\nI bought six. Cherries. Not kilos.",
     "Bright fruit shop in the late morning with wooden crates of summer fruit: Eli in a T-shirt, shorts, sunglasses and "
     "his navy pom-pom beanie holding a small paper bag of exactly six glossy dark-red cherries, lifting one up to the "
     "light like a precious jewel with an awed face, his empty wallet open in the other hoof, crates of cherries and "
     "apricots behind him, bright late-morning light",
     "Treating them like rubies 🍒💸\n\nDo you buy the first cherries, or wait till Christmas?", False),
    (48, "sore", "friends", "Friends Secret Santa draw.\nBig Tama got Mei.\nMei got Big Tama.",
     "Mei's sunny corner café in the afternoon decorated with tinsel: Big Tama in an orange hi-vis vest holding a tiny "
     "folded paper slip between two enormous fingers and looking down at Mei with a worried 'what do I buy someone so "
     "small' face, while Mei on the counter holds a folded slip almost as big as herself and stares up at him wide-eyed, "
     "tail fanned, a salad bowl of folded slips between them, Eli in a T-shirt and his navy pom-pom beanie and Ruthie in a "
     "sage-green blouse with her pink daisy behind her ear laughing, bright afternoon light",
     "One needs a gift the size of a thimble. The other needs one the size of a car 🎁😂\n\n"
     "Gift ideas for either of them? Help us out 👇", False),
    (48, "sore2", "couple", "Friday, 5pm.\nThe week is done.\nThe deck is warm. And you're here.",
     "Golden late-afternoon light on the new stained timber deck: Eli in a T-shirt, shorts and his navy pom-pom beanie and "
     "Ruthie in a sage-green blouse and shorts with her pink daisy behind her ear sitting on the edge of the deck with "
     "their hooves dangling in a little inflatable paddling pool, sharing a small bowl of cherries, Ruthie resting her "
     "head on Eli's shoulder, both smiling softly, warm glow and long shadows",
     "Little moments, big blessings 💛\n\nWhat's your favourite Friday ritual?", False),
    (48, "larut", "friends", "Pip's sleeping over before the parade.\nThe head elf can't sleep.\nShe's “just too excited.”",
     "Cosy lounge at night lit by twinkling fairy lights: Pip in green elf pyjamas and a pointy elf hat, wide awake and "
     "bouncing on a mattress made up on the floor, Ruthie in pink pyjamas with her pink daisy behind her ear sitting "
     "beside her stroking her fluffy fringe and laughing softly, Eli in striped pyjamas and his navy pom-pom beanie "
     "slumped half asleep in the armchair holding a storybook, a glass of warm milk on the side table, a little glitter "
     "sparkling on the carpet, soft warm glow",
     "Big day tomorrow 🧝✨ Head elf, please go to sleep.\n\nWhat were you too excited to sleep for as a kid?", False),

    # ---------- Sabtu 21 Nov (hari 49) - Santa parade ----------
    (49, "pagi3", "friends", "Pip ordered Big Tama an elf costume.\n“One size fits all.”\nIt did not.",
     "Sunny front lawn on parade morning: Big Tama in a black rugby jersey holding a tiny green elf tunic up against his "
     "enormous chest where it looks like a bib, with a sheepish, apologetic smile, Pip in her green elf costume staring "
     "up with her mouth open in dismay, Eli in a green elf costume with a jingle-bell collar and his navy pom-pom beanie "
     "pressing his lips together trying not to laugh, Ruthie in a red sundress with her pink daisy behind her ear "
     "stepping in with a red Santa hat as plan B, Mei perched on Big Tama's shoulder filming, bright morning sun",
     "Plan B: a Santa hat. Problem solved 🎅🐏 Parade at noon!\n\nWhat's the funniest costume fail you've ever seen?", False),
    (49, "siang0", "ruthie", "Turned this morning's strawberries into jam.\nThe jam: perfect.\nThe kitchen: a sauna.",
     "Steamy sunny kitchen in the late morning: Ruthie in a red sundress and a strawberry-print apron, pink daisy behind "
     "her ear, triumphantly holding up a glass jar of glossy red strawberry jam, her wool frizzed by the heat and a bead "
     "of sweat on her brow, a big pot bubbling on the stove, rows of filled jars cooling on the bench, a desk fan blowing "
     "at full speed, bright summer light",
     "Worth it. Probably 🍓🥵\n\nJam on toast or jam on scones?", False),
    (49, "sore", "friends", "After the parade,\nBig Tama gave every kid\na ride on the float.",
     "Grassy park after the Santa parade in the warm afternoon: Big Tama in a black rugby jersey and a red Santa hat "
     "slowly pulling the glittering gold sleigh float in a gentle loop, a dozen giggling little lambs riding on it and "
     "waving, Pip in her green elf costume handing out lollies, Mei riding on top of Big Tama's Santa hat, Eli in a green "
     "elf costume and his navy pom-pom beanie walking alongside holding a small lamb's hoof, Ruthie in a red sundress "
     "with her pink daisy behind her ear handing out ice blocks to the waiting queue, golden afternoon light",
     "Forty laps. Not one complaint 🛷💛 Our gentle giant.\n\n"
     "What's your favourite Christmas memory from when you were little?", False),
    (49, "sore2", "couple", "Christmas lunch debate.\nHer: cold ham, salads, pav.\nMe: a full hot roast. In 28°C.",
     "Sunny back deck in the late afternoon: Eli in a T-shirt, shorts and his navy pom-pom beanie, a little gold glitter "
     "still in his wool, standing firm in oven mitts holding an empty roasting dish with a determined face, facing Ruthie "
     "in a red sundress with her pink daisy behind her ear holding a big bowl of fresh summer salad with one eyebrow "
     "raised, a playful standoff, a blooming red pōhutukawa behind them, warm golden light",
     "We'll compromise: both. And pav 🍖🥗🍓\n\nHot Christmas roast or cold ham and salads?", False),
    (49, "larut", "couple", "9:30pm on the deck.\nCicadas off. Ruru on.\nWhat a week.",
     "Peaceful summer night on the new stained timber deck: Eli in navy pyjamas and his navy pom-pom beanie, a few flecks "
     "of gold glitter still in his wool, and Ruthie in pastel pyjamas with her pink daisy behind her ear cuddled under a "
     "light blanket on an outdoor couch, her head on his shoulder, both smiling up at a small brown ruru owl with big "
     "yellow eyes perched on the fence rail, a tiny head torch bobbing far away in the dark bushes, a big full moon and "
     "stars, festoon lights glowing softly",
     "A deck, a beach, a parade and new friends 🦉🌙 Thank you for following along this week.\n\n"
     "What was the best part of your week?", False),
]
