"""@eliandruthie - slot TAMBAHAN hari 22-35 (Minggu 25 Okt s/d Sabtu 7 Nov 2026), 5 post ekstra/hari = 70 post.
Slot: "pagi3" 09:00, "siang0" 10:30, "sore" 15:00, "sore2" 17:00, "larut" 21:30 (larut = Reel, suasana tidur/cosy).
Melengkapi alur di konten/eli_lamb_w3.py (dan EVENTS di eli_lamb.py), tanpa mengulang lelucon yang sudah ada.

Alur yang diikuti:
  - hari 22-23: masih di Rotorua (gereja tamu, geyser, pounamu, motel), pulang Labour Day, Kev jaga rumah,
    Grandpa Ram "mengadopsi" tomat kami
  - hari 24: Pip lulus learner licence (lanjut ke pelajaran menyetir hari 26)
  - hari 25-28: alur BBQ (kursi kurang, 7 salad, undangan Kev, grup chat Nana Dot, baju sosis, roti 96 buah),
    Halloween hari 27-28 (kostum kantor, kostum rahasia Pip = serigala, butternut diukir, mangkuk permen,
    Bo-Peep & domba hilang, trick-or-treaters dapat sosis, Kev si "vampir" cuci piring)
  - hari 29: Sekolah Minggu (permen sisa), cerita Grandpa Ram, jalan sore di pantai
  - hari 30-33: Movember (kumis tempel hari 33), jandal putus, sunscreen, sprinkler, Guy Fawkes (domba
    dipindah ke paddock sepi, Kev terganggu, sparkler saja tanpa dentuman)
  - Natal +-1/4 minggu 5: kado yang hilang, rencana Natal 2 keluarga, lampu Natal, latihan elf dengan Pip,
    kartu Natal ke luar negeri, advent calendar, kaleng shortbread Nana Dot, jumper rusa ber-beanie, hiasan pie
Teman (FRIENDS dari eli_lamb_w3.py: Grandpa Ram, Nana Dot, Kiwi Kev, Pip) di +-1/3 post, nama disebut persis di adegan.
Eli SELALU pakai navy pom-pom beanie; Ruthie SELALU pakai bunga daisy pink di belakang telinga.
Tidak ada post rohani di slot ini (faith = False); momen gereja boleh, dengan hormat.
Tanpa merek di adegan; tanpa teks/tulisan di gambar (teks meme ditambahkan otomatis)."""

# (hari, slot, who, teks meme, adegan untuk prompt gambar, caption, rohani?)
# who = "eli" | "ruthie" | "couple" | "friends"  (friends = minimal satu karakter FRIENDS, namanya disebut di adegan)
DATA_B = [
    # ---------- Minggu 25 Okt (hari 22) - di Rotorua ----------
    (22, "pagi3", "couple", "Visiting a church on holiday.\nGreeter: “You're new!”\n4 lunch invitations later:",
     "Eli in a crisp pale-blue collared shirt, navy chinos and his navy pom-pom beanie and Ruthie in a lavender wrap dress and "
     "white cardigan with her pink daisy behind her ear standing just inside the doorway of a small timber country church, "
     "warmly surrounded by a cluster of beaming elderly church ladies (sheep in floral blouses and pearl necklaces) shaking their "
     "hooves, one offering a plate of scones and another gesturing towards home for lunch, Eli and Ruthie looking happily "
     "overwhelmed, soft morning sunlight through the open doors, faint wisps of geothermal steam drifting outside",
     "Kiwi church hospitality is undefeated 💛⛪ We felt at home in 30 seconds.\n\nDo you visit a church when you're travelling?", False),
    (22, "siang0", "ruthie", "Mountain biking in Rotorua.\n“It's a beginner track,” he said.\nI have mud in my eyelashes.",
     "Ruthie in a bright teal cycling jersey, padded shorts and a white bike helmet over her caramel curls, pink daisy still "
     "tucked behind her ear, standing proudly beside a mountain bike on a forest trail among tall redwoods and lush tree ferns, "
     "splattered from hooves to helmet in brown mud, grinning widely with mud on her cheeks and long eyelashes, a muddy puddle "
     "behind her, dappled late-morning sunlight",
     "Muddy, sore and already planning the next ride 🚵‍♀️😂\n\nHave you tried mountain biking? Brave or never?", False),
    (22, "sore", "eli", "Waited 40 minutes for the geyser.\nLooked at my phone for 1 second.\nYou know what happened.",
     "Eli in a light khaki rain jacket, cargo shorts and his navy pom-pom beanie standing at a wooden viewing platform in a "
     "geothermal valley, looking down at the phone in his hoof while right behind him a huge white geyser erupts high into the "
     "blue sky in a tall plume of steam and spray, other tourists behind him pointing and cheering, pale rocky silica terraces, "
     "bright afternoon sun",
     "Nature has perfect timing. So do I, apparently 🙃♨️\n\nWhat's something amazing you completely missed?", False),
    (22, "sore2", "couple", "They say pounamu should be given,\nnever bought for yourself.\nSo I bought one for her.",
     "Golden hour on the shore of a calm lake: Eli in a cream cable-knit jumper and his navy pom-pom beanie gently fastening a "
     "small green pounamu (greenstone) pendant on a black cord around Ruthie's neck from behind, Ruthie in a soft rose-pink linen "
     "dress with her pink daisy behind her ear holding the smooth teardrop-shaped stone in her hoof and gazing down at it with "
     "happy teary eyes, soft wisps of steam over the water, warm golden light",
     "Pounamu carries the love of the one who gives it 💚 Best souvenir of the weekend.\n\n"
     "What's the most meaningful gift you've ever received?", False),
    (22, "larut", "couple", "Motel pillows:\none is a cloud.\none is a brick.\nWe both know who got the cloud.",
     "Cosy holiday motel room at night lit by a warm bedside lamp: Ruthie in pastel satin pyjamas with her pink daisy behind her "
     "ear sinking blissfully into a huge fluffy pillow with a smug, sleepy smile, while Eli in a grey T-shirt, plaid pyjama pants "
     "and his navy pom-pom beanie sits up beside her punching a flat, rock-hard pillow and trying to fold it in half, a suitcase "
     "open on the floor, simple motel decor",
     "The holiday sleep lottery 😴🛏️ I lost. Again.\n\nDo you bring your own pillow on holiday?", False),

    # ---------- Senin 26 Okt (hari 23) - Labour Day, pulang ----------
    (23, "pagi3", "eli", "Holiday rule:\none fridge magnet per trip.\nOur fridge door now weighs 4kg.",
     "Eli in a navy polo shirt, cargo shorts and his navy pom-pom beanie standing in a cluttered little souvenir shop, solemnly "
     "holding up a tiny fridge magnet shaped like a bubbling mud pool in both hooves like a precious treasure, shelves of soft "
     "toy kiwis, carved wooden trinkets, keyrings and folded tea towels behind him, bright morning light through the shop window",
     "Some people collect memories. I collect magnets 🧲😂\n\nWhat's the one souvenir you always buy?", False),
    (23, "siang0", "couple", "Her: “I'll keep you company\non the drive home.”\n4 minutes later:",
     "Inside a small hatchback on a sunny country highway: Ruthie in an oversized grey hoodie with sunglasses pushed up on her "
     "head and her pink daisy behind her ear, fast asleep against the passenger window with her mouth slightly open and a "
     "travel pillow squashed against her cheek, a bag of souvenir fudge open on her lap, Eli driving in a navy polo shirt and "
     "his navy pom-pom beanie glancing over at her with a fond, resigned smile, rolling green farmland and pine forest through "
     "the windows, bright late-morning light",
     "Best co-pilot ever. Zero conversation 😴🚗\n\nOn road trips: are you the driver or the sleeper?", False),
    (23, "sore", "friends", "Home from Rotorua.\nKev minded the house.\nKev is asleep on our couch. In my slippers.",
     "Bright afternoon in a cosy lounge: Kiwi Kev in his black singlet fast asleep on his back on the couch with his long beak "
     "pointing at the ceiling, wearing Eli's oversized fluffy navy slippers on his tiny feet, a pile of unopened mail resting on "
     "his round tummy and a knitted throw half over him, a watering can beside a very over-watered pot plant; Eli in a navy "
     "polo shirt and his navy pom-pom beanie standing in the doorway loaded with every bag, pillow and the chilly bin in one "
     "trip, and Ruthie beside him in an oversized grey hoodie with her pink daisy behind her ear, both staring at Kiwi Kev with "
     "amused faces, soft afternoon light",
     "House: fine. Plants: VERY watered. Slippers: claimed 🥝🩴\n\nWho looks after your plants when you're away?", False),
    (23, "sore2", "friends", "Grandpa Ram planted our tomatoes.\nWe've been home 2 hours.\nHe's checked on them 6 times.",
     "Golden late-afternoon light in the back garden: Grandpa Ram in his flat cap, round glasses and red-and-black checked "
     "woollen bush shirt crouching beside the row of young staked tomato seedlings, tenderly watering them from a small "
     "watering can and murmuring to them like a proud grandparent, Eli in a T-shirt, shorts and his navy pom-pom beanie "
     "leaning on the fence between the two yards with a cup of tea and a warm grin, long soft shadows",
     "Technically they're our tomatoes. Technically 🍅👴\n\nWho's the keenest gardener on your street?", False),
    (23, "larut", "couple", "Holidays are lovely.\nBut nothing beats\nour own bed.",
     "Cosy bedroom at night: Eli in soft navy-striped pyjamas and his navy pom-pom beanie and Ruthie in a white cotton nightie "
     "with her pink daisy behind her ear lying side by side under a fluffy white duvet, sinking into their own familiar pillows "
     "with eyes closed and blissful contented smiles, Ruthie's hoof resting on Eli's, a small glowing bedside lamp and a framed "
     "photo of the two of them on the bedside table, curtains moving gently in the night breeze",
     "Home sweet home 🤍😴\n\nWhat's the first thing you do when you get home from a trip?", False),

    # ---------- Selasa 27 Okt (hari 24) ----------
    (24, "pagi3", "friends", "Back from holiday.\nFridge: one lemon and some mustard.\nThen Nana Dot knocked.",
     "Bright morning at the front door: Nana Dot in her lilac cardigan, pearls and reading glasses on a beaded chain smiling "
     "sweetly on the doorstep holding a basket of warm golden scones wrapped in a gingham cloth, a jar of homemade jam and a "
     "bottle of milk, Eli in a crisp light-blue work shirt and his navy pom-pom beanie in the doorway with grateful shiny eyes "
     "and a hoof on his heart, the kitchen behind him with the fridge door open on almost-empty shelves, soft morning sunlight",
     "Nana Dot always knows 🥹💕 Every street needs one.\n\nWho's the Nana Dot in your life?", False),
    (24, "siang0", "ruthie", "Colleague: “How was the long weekend?”\nMe: “Got a minute?”\n*opens 312 photos*",
     "Office kitchen at morning tea: Ruthie in a smart cream blouse and high-waisted navy trousers with her pink daisy behind "
     "her ear eagerly holding her phone up in front of a polite colleague (a grey sheep in a cardigan holding a mug) and "
     "swiping with huge enthusiasm, the colleague's polite smile slowly fading, a plate of biscuits on the bench, bright "
     "mid-morning light",
     "And that was just the redwoods 📸😂\n\nAre you a holiday-photo sharer or keeper?", False),
    (24, "sore", "friends", "Pip passed her learner's licence!\nRuthie: “So who's going to teach her?”\nEveryone looked at me.",
     "Sunny front lawn in the afternoon: Pip in her bright pink raincoat and yellow gumboots leaping in the air with joy holding "
     "up a small plastic photo card, Ruthie in a mint cardigan with her pink daisy behind her ear hugging her and pointing "
     "towards Eli, and Eli in a grey hoodie and his navy pom-pom beanie standing very still with a pale, wide-eyed face, "
     "clutching his car keys, bright afternoon light",
     "So proud of her 🥳 Slightly scared for me 😬\n\nDid you pass your licence first try?", False),
    (24, "sore2", "eli", "Washed the car for the first time since April.\nThe sky, 10 minutes later:",
     "Eli in a faded blue T-shirt, rolled-up shorts, black gumboots and his navy pom-pom beanie standing next to a gleaming "
     "freshly washed little hatchback in the driveway, holding a dripping sponge and a bucket, staring up at a sudden dark cloud "
     "dumping heavy rain on him and the car, wool soaked flat, a patch of blue sky still visible in the distance, late-afternoon "
     "light",
     "Want rain in NZ? Wash your car. Works every time 🚗🌧️\n\nWhat's your guaranteed way to make it rain?", False),
    (24, "larut", "couple", "Lights off.\nHer: “Can I ask you something?”\n45 minutes later we've planned\nour whole retirement.",
     "Dark cosy bedroom at night lit only by a soft moonbeam through the curtains: Eli in a navy-and-white striped pyjama top "
     "and his navy pom-pom beanie and Ruthie in a lilac nightie with her pink daisy behind her ear lying on their sides facing "
     "each other under the duvet, heads on their pillows, both wide awake and smiling, talking quietly, Ruthie gesturing "
     "dreamily with one hoof, a glass of water on the bedside table",
     "The best talks happen after lights out 🌙💕 (We're retiring to a beach bach, apparently.)\n\n"
     "What do you two talk about at bedtime?", False),

    # ---------- Rabu 28 Okt (hari 25) - alur BBQ ----------
    (25, "pagi3", "eli", "Guests on Saturday: 14.\nChairs we own: 6.\nOne of them is a bucket.",
     "Sunny back yard in the morning: Eli in a grey hoodie, track pants and his navy pom-pom beanie standing on the lawn with a "
     "hoof on his chin, counting a sad little row of mismatched seating: two plastic outdoor chairs, a wobbly kitchen stool, a "
     "camping chair, a weathered garden bench and an upturned bucket, the empty deck behind him, dewy grass, bright morning sun",
     "The BBQ seating plan is… flexible 🪣😂\n\nBe honest: how many chairs do you own?", False),
    (25, "siang0", "ruthie", "BBQ for 14.\nSalads planned: 7.\nPeople who will eat salad: 2.",
     "Sunny kitchen in the late morning: Ruthie in a sage-green linen shirtdress and a striped apron with her pink daisy behind "
     "her ear standing at the bench surrounded by enormous bowls of colourful salad ingredients, a mountain of lettuce, cherry "
     "tomatoes, beetroot and boiled potatoes, a closed stack of recipe books at her elbow, holding a wooden salad spoon like a "
     "conductor's baton with a determined face, bright light",
     "Kiwi BBQ maths: 7 salads, everyone eats the potato one 🥗🥔\n\nWhat's the best BBQ salad?", False),
    (25, "sore", "friends", "Invited Kev to the BBQ.\n“Saturday, 4 o'clock.”\nKev: “…am?”",
     "Afternoon on the front porch next door: Kiwi Kev peeking out of his barely opened front door in a fluffy dressing gown "
     "with a sleep mask pushed up on his forehead, squinting painfully at the bright daylight with ruffled bed-head feathers, "
     "while Eli in a short-sleeved navy polo shirt and his navy pom-pom beanie stands on the step waving cheerfully, a "
     "flowering hedge and sunny street behind them",
     "Kev's coming. He'll be there for the last 20 minutes 🥝😴\n\nMorning person or night owl?", False),
    (25, "sore2", "friends", "Made a group chat for the BBQ.\nNana Dot replies to every message\nby phoning me.",
     "Late-afternoon lounge: Eli in a navy hoodie and his navy pom-pom beanie sitting on the couch answering his ringing phone "
     "with a patient, amused smile, while through the big window behind him, across the low fence, Nana Dot in her lilac "
     "cardigan and reading glasses on a beaded chain stands on her cottage porch holding an old flip phone to her ear and waving "
     "cheerfully at him, Grandpa Ram behind her in his flat cap holding a teapot, warm golden light",
     "Nana Dot doesn't “do texting” 📞💕 Honestly? Best part of my day.\n\n"
     "Who in your family still rings instead of texting?", False),
    (25, "larut", "couple", "Her: asleep in 30 seconds.\nMe: replaying something awkward\nI said in 2011.",
     "Dark bedroom at night: Ruthie in a peach cotton nightie with her pink daisy behind her ear peacefully asleep on her side "
     "with a tiny smile, cuddling her pillow, while Eli in a grey T-shirt and his navy pom-pom beanie lies on his back beside "
     "her wide awake, eyes open and staring at the ceiling, the duvet pulled up to his chin, a faint glowing nightlight and soft "
     "blue moonlight",
     "Why does my brain save these for bedtime?? 🫠🌙\n\nFast sleeper or overthinker?", False),

    # ---------- Kamis 29 Okt (hari 26) ----------
    (26, "pagi3", "eli", "Ruthie cleaned the lounge for Saturday.\nI'm not allowed in it.\nI live in the hallway now.",
     "Eli in a navy fleece, track pants, fluffy slippers and his navy pom-pom beanie sitting on the hallway floor eating cereal "
     "from a bowl, gazing longingly through the doorway into a spotless gleaming lounge with perfectly plumped cushions, fresh "
     "vacuum lines in the carpet and a vase of fresh flowers, a satin ribbon tied across the doorway like a barrier, bright "
     "morning light",
     "Two more days of hallway life 🥣😂\n\nWho's the clean-freak host in your house?", False),
    (26, "siang0", "ruthie", "Guests in 2 days.\nMe: buys 30 flowers\nto plant “real quick.”",
     "Bright garden centre in the late morning: Ruthie in floral gardening overalls and a wide sunhat with her pink daisy behind "
     "her ear happily pushing a big flat trolley crammed with dozens of punnets of colourful petunias, marigolds and lavender "
     "plus two potted hydrangeas, rows of plants and hanging baskets all around her, a joyful determined face, warm sunshine "
     "through the glasshouse roof",
     "Planting all 30 tomorrow. Before work 🌸😅\n\nWhat do you always overbuy at the garden centre?", False),
    (26, "sore", "friends", "After Pip's lesson with me,\nGrandpa Ram took over. On his paddock.\n“Nothing to hit out here.”",
     "Wide green farm paddock in the afternoon: Pip in her pink raincoat steering an old rusty farm ute very slowly across the "
     "grass with a huge grin, Grandpa Ram in his flat cap, round glasses and tweed waistcoat totally calm in the passenger seat "
     "sipping tea from a thermos lid, a few woolly sheep trotting out of the way, Eli in a light flannel shirt and his navy "
     "pom-pom beanie leaning on the wooden farm gate watching with enormous relief, bright afternoon sun and rolling hills",
     "The sheep might disagree with Grandpa Ram 🐑🚜 But Pip did great!\n\n"
     "Did you learn to drive on a farm, in a car park or on the open road?", False),
    (26, "sore2", "couple", "Her: “What are you wearing Saturday?”\nMe: “My good shirt.”\nHer: “It has sausages on it.”",
     "Bedroom in late-afternoon light: Eli in shorts and his navy pom-pom beanie proudly holding a short-sleeved shirt covered "
     "in a cartoon sausage print against his chest, beaming, while Ruthie in a pale-pink sundress with her pink daisy behind her "
     "ear stands beside him with a deadpan look, holding up a bright tropical-print summer shirt instead, wardrobe doors open "
     "behind them",
     "The sausage shirt lost. This time 🌭👕\n\nDoes your partner veto your outfits?", False),
    (26, "larut", "eli", "Lying in bed\nrehearsing the BBQ timings\nlike it's a rugby final.",
     "Dim bedroom at night: Eli in navy pyjamas and his navy pom-pom beanie sitting up in bed with an intense, focused coach's "
     "face, sketching invisible plays in the air with one hoof, a pair of BBQ tongs and a folded striped apron laid out neatly on "
     "the duvet beside him like a match-day uniform, soft bedside lamp glow",
     "Sausages at 4:15. Steak at 5. Onions? Always 🔥😤\n\nDo you overthink hosting too?", False),

    # ---------- Jumat 30 Okt (hari 27) - malam Halloween ----------
    (27, "pagi3", "ruthie", "Work Halloween dress-up day.\nMe: full pumpkin costume.\nEveryone else: cat ears.",
     "Open-plan office in the morning: Ruthie standing in the middle of the room wearing a huge round orange pumpkin costume "
     "with a little green stem hat, her pink daisy tucked behind her ear, holding her coffee mug, while blurry colleagues at "
     "their desks in normal office clothes wear only simple black cat-ear headbands, Ruthie's face slowly realising, bright "
     "morning light",
     "Committed to the bit 🎃😂 No regrets. Some regrets.\n\nDo you dress up for Halloween at work?", False),
    (27, "siang0", "friends", "Pip won't tell us her Halloween costume.\nShe just keeps saying\n“Grandpa Ram's going to LOVE it.”",
     "Sunny back yard by the fence in the late morning: Pip in her bright pink raincoat and yellow gumboots hugging a zipped-up "
     "garment bag to her chest and giggling mischievously, Ruthie in a white T-shirt and denim shorts with her pink daisy behind "
     "her ear trying to peek inside it, Eli in a navy singlet and his navy pom-pom beanie raising one eyebrow, and Grandpa Ram in "
     "his flat cap and round glasses peering over the fence with a deeply suspicious frown",
     "We find out tomorrow 👀🎃\n\nGuess Pip's costume in the comments 👇", False),
    (27, "sore", "eli", "Halloween in NZ:\nno pumpkins in spring.\nSo I carved a butternut.",
     "Front porch in the afternoon: Eli in a black T-shirt, orange shorts and his navy pom-pom beanie crouching proudly beside "
     "a small carved butternut squash with a tiny wonky jack-o'-lantern face and a tealight glowing inside, a carving knife and "
     "scooped-out seeds on a wooden chopping board, a bowl of lollies beside it, sunny spring garden behind",
     "He's small but he's trying 🎃🥹\n\nPumpkin, butternut or no carving at all?", False),
    (27, "sore2", "couple", "Lolly bowl for the trick-or-treaters.\nIt's Friday.\nIt's already half empty.",
     "Lounge in golden late-afternoon light: Eli in a striped T-shirt and his navy pom-pom beanie and Ruthie in a cosy orange "
     "jumper with her pink daisy behind her ear sitting on the couch on either side of a big glass bowl of lollies that is half "
     "empty, both with bulging cheeks and lolly wrappers in their laps, pointing at each other accusingly, a little carved "
     "butternut glowing on the windowsill",
     "Trick-or-treat is tomorrow. We'll need more lollies 🍬😇\n\nDo your Halloween lollies survive until the night?", False),
    (27, "larut", "couple", "Lights out.\nHer: “Did we get enough bread rolls?”\nMe: “96.”\nHer: “…should we get more?”",
     "Cosy bedroom at night: Ruthie in candy-pink pyjamas with her pink daisy behind her ear sitting bolt upright in bed with "
     "wide worried eyes, while Eli in navy flannel pyjamas and his navy pom-pom beanie lies face-down in his pillow with one "
     "hoof raised in surrender, a stack of bread roll bags piled on the dresser in the background, soft bedside lamp glow",
     "Host brain never switches off 🍞😂 Tomorrow's the big day!\n\nAre you an over-caterer?", False),

    # ---------- Sabtu 31 Okt (hari 28) - hari BBQ + Halloween ----------
    (28, "pagi3", "couple", "Our costume for the trick-or-treaters:\nshe's Little Bo-Peep.\nI'm the sheep she lost.",
     "Sunny front garden in the morning: Ruthie dressed as Little Bo-Peep in a frilly pale-blue dress and a big lacy bonnet tied "
     "under her chin with her pink daisy tucked into the brim, holding a long white shepherd's crook and shading her eyes as if "
     "searching the horizon, while Eli in his navy pom-pom beanie and an extra-fluffy white wool jumper peeks out from behind a "
     "hedge right beside her with a cheeky grin, bright morning light",
     "Effort: minimal. Costume: perfect 🐑🎃\n\nWhat's the best couple costume you've ever seen?", False),
    (28, "siang0", "eli", "BBQ day.\nThird trip to the supermarket.\nThe checkout lady: “You again?”",
     "Bright supermarket checkout in the late morning: Eli in a tropical-print summer shirt, shorts, jandals and his navy pom-pom "
     "beanie unloading yet another armful of sausages, bread rolls, plain unbranded bottles of tomato sauce and bags of ice onto "
     "the conveyor belt with a frazzled, sheepish smile, a friendly older checkout lady (a sheep in a plain work polo) giving him "
     "a knowing smirk, bright store lighting",
     "Fourth trip incoming. I forgot the onions 🧅😩\n\nHow many supermarket runs does your party take?", False),
    (28, "sore", "friends", "Party starts at 4.\nGrandpa Ram and Nana Dot: here at 3.\n“We didn't want to be late.”",
     "Front doorway in the afternoon: Grandpa Ram in a crisp short-sleeved checked shirt, his flat cap and round glasses holding "
     "a chilly bin, and Nana Dot in a floral summer dress, pearls and her lilac cardigan beaming and holding a big pavlova "
     "topped with strawberries and kiwifruit, standing on the doorstep; Ruthie opening the door in a fluffy dressing gown with "
     "big rollers in her caramel curls and her pink daisy behind her ear, and Eli behind her in a singlet and his navy pom-pom "
     "beanie with a half-blown balloon in his mouth, both frozen in surprise, bright afternoon sun",
     "An hour early is “on time” for Grandpa Ram 😂🕒\n\nWho's always early in your family?", False),
    (28, "sore2", "friends", "Trick-or-treaters walked into our BBQ.\nLeft with lollies AND a sausage.\nBest house on the street.",
     "Lively back yard BBQ in golden late-afternoon light under festoon lights: a cluster of tiny lambs in homemade Halloween "
     "costumes (a ghost sheet, a witch hat, a little dinosaur onesie) lining up at the grill with lolly buckets, Eli in a "
     "tropical-print shirt, his navy-and-white striped BBQ apron and navy pom-pom beanie happily handing each one a sausage in "
     "bread with tomato sauce, Ruthie in a floral sundress with her pink daisy behind her ear handing out lollies from a big "
     "bowl, Pip in her fluffy grey wolf onesie with little ears leading the little trick-or-treaters, smoke curling from the "
     "barbecue",
     "Kiwi Halloween hits different 🎃🌭\n\nWould you hand out sausages to trick-or-treaters?", False),
    (28, "larut", "friends", "The party's over.\nKev's night is just beginning.\nHe's washed every dish we own.",
     "Kitchen at night lit by a warm pendant light: Kiwi Kev in his black singlet, a little black vampire cape left over from "
     "the party and yellow rubber gloves standing on a stool at the sink wide awake and humming, a sparkling tower of clean "
     "plates and bowls on the drying rack beside him, and through the doorway behind him Eli in his tropical shirt and navy "
     "pom-pom beanie and Ruthie in her floral sundress with her pink daisy behind her ear fast asleep slumped together on the "
     "couch under a blanket, a few deflated balloons on the floor",
     "Nocturnal neighbour = free dishwasher 🥝🧽 Thank you, Kev!\n\nWho's the clean-up hero after your parties?", False),

    # ---------- Minggu 1 Nov (hari 29) ----------
    (29, "pagi3", "friends", "Brought the leftover Halloween lollies\nto Sunday school.\nNana Dot: “AFTER the lesson, dears.”",
     "Bright church hall in the morning: Nana Dot in a floral Sunday dress, pearls and lilac cardigan sitting on a small chair "
     "reading from a children's picture Bible to a semicircle of little lambs in their Sunday best on a colourful mat, but every "
     "little lamb is staring sideways at a big bowl of lollies held by Eli (collared Sunday shirt and his navy pom-pom beanie) "
     "and Ruthie (soft blue dress with her pink daisy behind her ear) standing at the back with guilty smiles, warm morning "
     "window light",
     "In our defence, the lollies were very quiet 🍬😅 Nana Dot runs a tight (and very loving) ship.\n\n"
     "What do you remember from Sunday school?", False),
    (29, "siang0", "eli", "Day after the BBQ.\nLost property: 1 jandal, 2 hats, 1 salad bowl.\nNobody wants the jandal.",
     "Back deck on a sunny late morning: Eli in a faded T-shirt, track pants and his navy pom-pom beanie holding up a single "
     "lonely jandal between two hooves like evidence, a small pile of forgotten items on the outdoor table beside him (two "
     "sunhats, a salad bowl, a pair of sunglasses, a plastic container), a few deflated balloons on the lawn, bright light",
     "If this is your jandal, it misses you 🩴😂\n\nWhat's the weirdest thing someone's left at your place?", False),
    (29, "sore", "friends", "Sunday afternoon with Grandpa Ram.\nThe '75 flood story. Again.\nI'd happily hear it 100 more times.",
     "Cottage veranda in warm afternoon light: Grandpa Ram in a cardigan, his flat cap and round glasses sitting in a wicker "
     "chair telling a story with both hooves spread wide and an animated, twinkling face, Eli in a collared Sunday shirt and his "
     "navy pom-pom beanie sitting on the step beside him with a cup of tea, listening with a warm smile, Nana Dot knitting in the "
     "chair behind them and quietly mouthing along to the story, a sleepy summer garden full of roses",
     "Some stories get better every time 👴💛\n\nWhat's the story your grandparent always tells?", False),
    (29, "sore2", "couple", "Sunday evening.\nNo phones. No plans.\nJust us and the tide.",
     "Golden-hour beach: Eli in rolled-up linen trousers, a white T-shirt and his navy pom-pom beanie and Ruthie in a flowing "
     "coral sundress with her pink daisy behind her ear walking barefoot along the waterline holding hooves, their jandals "
     "dangling from their free hooves, gentle waves washing over their feet, a headland of pōhutukawa trees in the distance, "
     "warm golden sunset light",
     "The best kind of Sunday evening 🌅🤍\n\nWhere do you go to slow down?", False),
    (29, "larut", "eli", "Nana Dot's lunch was 9 hours ago.\nI'm still full.\nShe sent leftovers.",
     "Cosy bedroom at night: Eli in loose tartan pyjamas and his navy pom-pom beanie lying flat on his back on top of the duvet "
     "with both hooves resting on his very round full tummy, a satisfied but defeated face, a big foil-covered plate of roast "
     "leftovers waiting on the bedside table next to a glass of water, soft lamp light",
     "Nana love is a full-time commitment 🥔😴\n\nDoes your nana send you home with leftovers too?", False),

    # ---------- Senin 2 Nov (hari 30) ----------
    (30, "pagi3", "ruthie", "Everyone hates green smoothies.\n“It tastes like a lawn!”\nMe, a sheep: exactly. Delicious.",
     "Bright kitchen in the morning: Ruthie in a pastel yoga top and leggings with her pink daisy behind her ear happily sipping "
     "a tall glass of bright green smoothie through a straw with blissful closed eyes, a blender full of spinach and fresh grass "
     "beside her, a little pot of wheatgrass on the bench, sunny morning light",
     "Monday health kick: going great 🥬🐑\n\nGreen smoothie: love it or hate it?", False),
    (30, "siang0", "eli", "Bought Ruthie's Christmas present in March.\nHid it so well\nI can't find it.",
     "Messy spare room in the late morning: Eli in a navy knitted vest over a white shirt and his navy pom-pom beanie on his "
     "knees with his head and shoulders inside a cluttered wardrobe, boxes, shoes, suitcases and old Christmas decorations "
     "pulled out all over the floor around him, a torch in one hoof, frantic energy, bright light from the window",
     "It's somewhere. It's definitely somewhere 🎁😰\n\nDo you buy Christmas presents early, or on Christmas Eve?", False),
    (30, "sore", "ruthie", "Jandal blowout:\nthe Kiwi version\nof a flat tyre.",
     "Hot suburban footpath in the afternoon: Ruthie in a white broderie sundress and sunglasses with her pink daisy behind her "
     "ear hopping on one hoof, holding up a pink jandal whose toe strap has popped out of the sole, a tote bag of groceries on "
     "her shoulder, a dismayed face, bright sunny afternoon, heat shimmering off the footpath",
     "Hopping home the last 800 metres 🩴😩\n\nHave you ever fixed a jandal on the spot?", False),
    (30, "sore2", "friends", "5pm. Us: home from work.\nKev: just woke up, waving with his coffee.\n“Morning!”",
     "Suburban street in 5pm golden light: Eli in a work shirt with a loosened navy tie and his navy pom-pom beanie and Ruthie in "
     "a work blazer with her pink daisy behind her ear trudging up their driveway with laptop bags, looking tired, while next "
     "door Kiwi Kev in a fluffy dressing gown with bed-head feathers stands on his porch cheerfully raising a steaming mug of "
     "coffee in greeting with a fresh, energetic face",
     "Same street, different time zones 🥝☕\n\nAre you on Kev time or normal time?", False),
    (30, "larut", "couple", "Her: “Do you think we'll still be\nthis silly when we're 80?”\nMe: “Look next door.”",
     "Cosy bedroom at night: Eli in navy-and-white striped pyjamas and his navy pom-pom beanie and Ruthie in a soft lilac nightie "
     "with her pink daisy behind her ear cuddled up together at an open bedroom window, looking across the dark garden at the "
     "warmly lit kitchen window of the elderly neighbours' cottage, where two old sheep silhouettes are slow-dancing together, "
     "Eli and Ruthie smiling tenderly, starry sky, gentle night breeze",
     "Grandpa Ram and Nana Dot, still dancing in the kitchen after 50+ years 🥹💕 Goals.\n\nWho are your couple goals?", False),

    # ---------- Selasa 3 Nov (hari 31) ----------
    (31, "pagi3", "friends", "Shearing season.\nGrandpa Ram: “I'll give you a quick trim, lad.”\nI've seen his quick trims.",
     "Rustic old wooden woolshed in the morning: Grandpa Ram in a navy shearer's singlet, his flat cap and round glasses holding "
     "a pair of old-fashioned hand blade shears with a twinkly grin, a freshly shorn, very skinny and slightly bewildered sheep "
     "standing behind him looking like a completely different animal, Eli in a light flannel shirt clutching his navy pom-pom "
     "beanie with both hooves and backing slowly towards the door with wide eyes, shafts of morning sun through the slatted "
     "walls and loose wool on the floor",
     "Thanks Grandpa, but I'm keeping the fluff ✂️😅\n\nEver regretted a DIY haircut?", False),
    (31, "siang0", "ruthie", "Him: “I don't need sunscreen,\nit's only November.”\nMe, in SPF 50, a hat and shade: “Okay.”",
     "Sunny back lawn in the late morning: Ruthie in a sleeveless striped linen top, white shorts, big sunglasses and a huge "
     "floppy sunhat with her pink daisy behind her ear lounging in deep shade under a large beach umbrella on a deck chair, a "
     "bottle of sunscreen on the little table beside her and a white dab of sunscreen on her nose, giving a knowing side-eye "
     "while sipping iced tea, blazing bright sun on the lawn beyond the shade",
     "I'll just leave this here ☀️🧴 (Update at lunchtime.)\n\nAre you the sunscreen nag in your house?", False),
    (31, "sore", "couple", "Christmas Day plans:\nher family or mine?\nAnswer: both. 3 hours' drive apart.",
     "Kitchen table in the afternoon: Ruthie in a cherry-red sundress with her pink daisy behind her ear moving two little toy "
     "cars between two toy houses on the table like a military strategist with a determined face, Eli in a white T-shirt and his "
     "navy pom-pom beanie beside her holding a mince pie and looking overwhelmed, two mugs of tea, bright afternoon light",
     "Lunch at hers, dinner at mine, pav in the car 🚗🎄\n\nHow does your family split Christmas Day?", False),
    (31, "sore2", "friends", "Pip turned on the sprinkler.\nMe: “I'm a grown-up.\nI'm not running through that.”\nAlso me:",
     "Sunny back yard at 5pm: Eli in a faded red T-shirt, board shorts and his navy pom-pom beanie leaping joyfully through the "
     "arc of a garden sprinkler with his arms out, water droplets sparkling, his sunburnt pink nose visible, Pip in a "
     "lemon-yellow swimsuit and her yellow gumboots laughing and jumping through the spray beside him, golden late-afternoon "
     "light glittering in the water, green lawn",
     "Best sunburn treatment, I reckon 💦😂\n\nWhen did you last run through a sprinkler?", False),
    (31, "larut", "couple", "Sunburnt nose.\nShe put aloe on it, kissed it better,\nthen sent a photo to her sister.",
     "Cosy bedroom at night: Eli in a white T-shirt, pyjama shorts and his navy pom-pom beanie sitting up in bed with his bright "
     "pink sunburnt nose shining under a blob of cool green aloe gel, wincing bravely, Ruthie in mint pyjamas with her pink daisy "
     "behind her ear sitting beside him with the aloe bottle in one hoof and her phone in the other, taking a sneaky photo with "
     "a giggle, warm bedside lamp light",
     "Love, care and absolutely zero privacy 💚📸\n\nWho do you send your partner's funniest photos to?", False),

    # ---------- Rabu 4 Nov (hari 32) ----------
    (32, "pagi3", "eli", "Tested last year's Christmas lights.\nOne bulb's out.\nSo they're all out.",
     "Lounge in the morning: Eli in a red-and-green checked flannel shirt, shorts and his navy pom-pom beanie sitting "
     "cross-legged on the carpet completely tangled in a long string of dark, unlit fairy lights wrapped around his arms, legs "
     "and beanie, holding up one tiny bulb and squinting at it, an open box of tangled Christmas decorations beside him, bright "
     "morning light",
     "Every. Single. Year. 🎄💡\n\nDo you test your Christmas lights, or just hope?", False),
    (32, "siang0", "friends", "Elf rehearsal #1.\nPip: “More jingle!”\nMe: I'm jingling as hard as I can.",
     "Sunny back yard in the late morning: Pip in a green elf hat with a bell, her pink raincoat and yellow gumboots directing "
     "like a strict choreographer with a whistle in her mouth, Eli in a green elf tunic with a jingle-bell collar, stripy "
     "tights and his navy pom-pom beanie mid-hop with a pained expression, the bells blurring with motion, Ruthie in a white "
     "T-shirt with her pink daisy behind her ear filming from the deck and laughing, bright sun",
     "Santa parade is in 17 days. Pip says I'm “not festive enough” 🧝😩\n\nAre you a reluctant performer too?", False),
    (32, "sore", "ruthie", "Making jam with the leftover strawberries.\nThere were no leftover strawberries.\nI went back for more.",
     "Sunny kitchen in the afternoon: Ruthie in a red gingham apron with her pink daisy behind her ear stirring a big bubbling "
     "pot of ruby-red strawberry jam with a wooden spoon, rows of glass jars with gingham-cloth lids cooling on the bench, three "
     "empty strawberry punnets and one fresh full punnet beside her, a smear of jam on her cheek, warm golden afternoon light",
     "Strawberry season, round two 🍓🫙\n\nDo you make jam, or eat them all straight away?", False),
    (32, "sore2", "couple", "5pm on a Wednesday.\n22 degrees.\nWe went to the beach. Like rebels.",
     "Beach at golden hour: Eli in his work shirt with the sleeves rolled up, rolled-up trousers and his navy pom-pom beanie and "
     "Ruthie in her work blouse and skirt with her pink daisy behind her ear running gleefully across the sand towards the water "
     "with their shoes in their hooves and their laptop bags dumped on the sand behind them, sparkling sea, long golden evening "
     "light, a few surfers in the distance",
     "Midweek beach trips are back 🌊😎\n\nAfter-work swim: yes or no?", False),
    (32, "larut", "couple", "Social touch: 40 minutes.\nRecovery: 3 to 5 business days.",
     "Cosy bedroom at night: Eli in a black rugby jersey, shorts and his navy pom-pom beanie lying stiffly in bed with ice packs "
     "on both knees and a heat pack under his back, wincing, Ruthie in floral pyjamas with her pink daisy behind her ear bringing "
     "him a hot water bottle and a cup of tea with a sympathetic but very amused smile, soft lamp glow",
     "Kev did the diving. I did the limping 🏉😩\n\nWhat sport leaves you sore for days?", False),

    # ---------- Kamis 5 Nov (hari 33) - Guy Fawkes ----------
    (33, "pagi3", "friends", "Guy Fawkes tonight.\nGrandpa Ram's moving the ewes\nto the quietest paddock on the farm.",
     "Misty green farm in the morning: Grandpa Ram in his flat cap, round glasses and red-and-black checked woollen bush shirt "
     "leading a small flock of fluffy ewes and their lambs through an open wooden gate with his walking stick, speaking gently "
     "to them, Eli in a light rain jacket, black gumboots and his navy pom-pom beanie holding the gate open and patting a nervous "
     "little lamb on the head, rolling hills and soft golden morning light",
     "Looking after the flock 🐑💛 If you're doing fireworks tonight, please spare a thought for the animals nearby.\n\n"
     "How do you keep your pets calm on Guy Fawkes?", False),
    (33, "siang0", "eli", "Movember, day 5.\nGrowth: none.\nGoing with plan B.",
     "Office desk in the late morning: Eli in the blue collared shirt he ironed this morning under a navy jumper, and his navy "
     "pom-pom beanie, sitting very upright and dignified with a large curly black stick-on fake moustache on his upper lip, "
     "holding a cup of tea and a pen like a distinguished gentleman, colleagues blurred in the background trying not to laugh, "
     "bright office light",
     "Still raising money for men's health, so it counts 🥸💙\n\nRate the mo out of 10 👇", False),
    (33, "sore", "ruthie", "Overseas Christmas post deadline: soon.\nCards bought: 30.\nCards written: 0.",
     "Dining table in the afternoon: Ruthie in a soft lilac blouse with her pink daisy behind her ear sitting behind a towering "
     "stack of blank Christmas cards decorated with red pōhutukawa flowers and gold stars, envelopes everywhere, a pen in her "
     "hoof and her chin resting on the stack with a defeated face, a cup of tea gone cold, bright afternoon light",
     "Writing them tonight. Definitely. Probably 💌🎄\n\nDo you still send Christmas cards?", False),
    (33, "sore2", "friends", "Guy Fawkes night:\nKev is not a fan.\n“Some of us WORK at night.”",
     "Dusk on the front porch: Kiwi Kev in his black singlet, tiny black gumboots and a head torch, wearing big fluffy earmuffs "
     "and clutching a little lunchbox, glaring grumpily at the first fireworks popping in the purple sky over the rooftops, Eli "
     "in a navy hoodie and his navy pom-pom beanie and Ruthie in a cosy cardigan with her pink daisy behind her ear standing "
     "beside him patting his shoulder sympathetically",
     "Kev would like to lodge a formal complaint 🥝🎆\n\nDoes your neighbourhood go big on Guy Fawkes?", False),
    (33, "larut", "friends", "Sheep-approved Guy Fawkes:\nsparklers only.\nNo bangs.",
     "Back yard at night: Eli in a navy hoodie, pyjama pants and his navy pom-pom beanie, Ruthie in a dressing gown with her pink "
     "daisy behind her ear, Pip in pink pyjamas and her yellow gumboots, and Grandpa Ram and Nana Dot wrapped in tartan blankets "
     "on garden chairs, all holding glowing sparklers and drawing swirling loops and little hearts of light in the dark air, "
     "faces lit warm gold, soft festoon lights on the deck behind them",
     "Once the big bangs settled down, we had our own quiet little show 🎇🐑\n\nSparklers or big fireworks?", False),

    # ---------- Jumat 6 Nov (hari 34) ----------
    (34, "pagi3", "ruthie", "Bought an advent calendar.\nIt's November 6.\nSix doors are already open.",
     "Kitchen in the morning: Ruthie in a red-and-white striped T-shirt with her pink daisy behind her ear standing at the bench "
     "holding a festive cardboard advent calendar with rows of little cardboard doors, six of them already torn open, a tiny "
     "chocolate in her hoof and chocolate on her lips, a guilty but totally unapologetic grin, morning sunlight",
     "I'm just… getting ahead 🍫🎄\n\nCould you resist an advent calendar in November?", False),
    (34, "siang0", "couple", "No anniversary. No birthday.\nJust a Friday.\nAnd she likes daisies.",
     "Outside a little office building at morning tea time: Eli in a smart pale-blue shirt, chinos and his navy pom-pom beanie "
     "holding out a big bunch of white and pink daisies wrapped in brown paper with a shy, proud smile, Ruthie in a work blazer "
     "and skirt with her pink daisy behind her ear covering her mouth with both hooves in surprised delight, sunny late-morning "
     "light, a few colleagues blurred in the window behind",
     "Small things, often 💐💕\n\nWhat's the sweetest no-reason surprise you've ever had?", False),
    (34, "sore", "friends", "Nana Dot's shortbread delivery round.\nKev opened the door at 3pm in his pyjamas:\n“Is it Christmas?”",
     "Afternoon on a neighbour's front doorstep: Nana Dot in her lilac cardigan, pearls, floral apron and reading glasses holding "
     "out a red tartan biscuit tin of shortbread with a sweet smile, a basket full of more tins on her arm, Kiwi Kev in crumpled "
     "striped pyjamas with bed-head feathers squinting sleepily at the daylight but reaching out eagerly for the tin, Ruthie in a "
     "gingham apron with her pink daisy behind her ear carrying another stack of tins behind Nana Dot, bright afternoon sun",
     "Nana Dot's tins are the official start of Christmas on our street 🍪🎄\n\n"
     "Does anyone on your street share their Christmas baking?", False),
    (34, "sore2", "eli", "Friday, 5pm.\nFirst ice block of summer.\nFirst brain freeze of summer.",
     "Front steps at golden hour: Eli in a bright yellow singlet, board shorts, jandals and his navy pom-pom beanie sitting on "
     "the steps holding a red-and-orange fruit ice block, eyes squeezed shut and a hoof pressed to his forehead in agonising "
     "brain freeze, a drip running down the stick, warm late-afternoon sun",
     "Worth it. Every time 🧊🥶\n\nWhat's your go-to summer ice block?", False),
    (34, "larut", "couple", "Lost family games night to Pip.\nRuthie's in bed reading the rule book.\n“She cheated. I'll prove it.”",
     "Cosy bedroom at night: Ruthie in pink pyjamas with her pink daisy behind her ear sitting up in bed with reading glasses on "
     "the end of her nose, intensely studying a thick board-game rule booklet with narrowed eyes, the board game box open on the "
     "duvet, while Eli in pyjamas and his navy pom-pom beanie is fast asleep beside her with a potato chip still in his hoof, "
     "soft lamp light",
     "Sibling rivalry never sleeps 🎲😤\n\nWho's the rule-checker in your family?", False),

    # ---------- Sabtu 7 Nov (hari 35) ----------
    (35, "pagi3", "eli", "Ruthie went to a garage sale with $10.\nShe came home with a lamp,\na chair and a canoe.",
     "Sunny driveway in the morning: Eli in a T-shirt, shorts, jandals and his navy pom-pom beanie standing beside their small "
     "hatchback with his jaw dropped, staring up at a long bright-red vintage canoe strapped precariously to the car roof with "
     "rope, a wicker chair and a vintage lamp sticking out of the open boot, bright morning light",
     "She haggled the canoe down to $4. I have questions 🛶😂\n\nWhat's the most random thing you've bought secondhand?", False),
    (35, "siang0", "friends", "Nana Dot finished our Christmas jumpers.\nMine has a reindeer on it.\nThe reindeer's wearing my beanie.",
     "Cosy cottage lounge in the late morning: Nana Dot in her lilac cardigan, pearls and reading glasses on a beaded chain "
     "beaming with pride as she holds up a bright red-and-green hand-knitted Christmas jumper against Eli's chest, the knitted "
     "reindeer on the front wearing a tiny navy pom-pom beanie, Eli in a T-shirt and his navy pom-pom beanie looking down at it "
     "utterly delighted and touched, Ruthie beside them already wearing her matching red-and-green reindeer jumper with her pink "
     "daisy behind her ear, Grandpa Ram in his armchair chuckling over his teacup, a basket of wool at their feet, warm light",
     "Nana Dot thinks of everything 🧶🦌💙 We're wearing them. Heatwave or not.\n\nDo you own a Christmas jumper?", False),
    (35, "sore", "friends", "Decorating the tree.\nRuthie: colour-coordinated.\nPip: all the tinsel.\nMe: a bauble shaped like a pie.",
     "Sunny lounge in the afternoon around a fresh real pine Christmas tree: Ruthie in her red-and-green reindeer jumper with her "
     "pink daisy behind her ear carefully hanging matching gold and white baubles, Pip in her pink raincoat throwing handfuls of "
     "shiny tinsel at the tree with glee, and Eli in a white T-shirt and his navy pom-pom beanie proudly hanging a little golden "
     "pie-shaped ornament front and centre, pine needles on the carpet, a box of decorations on the floor, warm afternoon light",
     "Every tree needs one pie 🥧🎄\n\nWhat's the weirdest ornament on your tree?", False),
    (35, "sore2", "ruthie", "Saturday, 5pm.\nA book, a blanket,\nnowhere to be.",
     "Golden-hour park: Ruthie in a cream crocheted cardigan over a sage sundress with her pink daisy behind her ear lying on a "
     "picnic blanket under a big leafy tree, reading a paperback with a peaceful smile, a bowl of strawberries and a glass of "
     "lemonade beside her, long golden light filtering through the leaves, soft summer breeze",
     "This is my kind of Saturday 📖🍓\n\nWhat are you reading right now?", False),
    (35, "larut", "couple", "First night with the tree up.\nEvery light off\nexcept the fairy lights.",
     "Dark cosy lounge at night lit only by the warm twinkling fairy lights on a real pine Christmas tree: Eli in navy flannel "
     "pyjamas and his navy pom-pom beanie and Ruthie in soft red pyjamas with her pink daisy behind her ear curled up together "
     "on the couch under a knitted blanket, Ruthie's head on Eli's shoulder, both gazing at the tree with quiet happy smiles, "
     "mugs of hot chocolate on the coffee table, a little golden pie ornament glinting on the tree",
     "Seven weeks to go, and this is already our favourite part 🎄✨\n\nWhat's your favourite part of the Christmas season?", False),
]
