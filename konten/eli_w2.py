"""Akun Eli - minggu 2 (Sun 4 Oct - Sat 10 Oct 2026), all ENGLISH. Theme: "Brave & Loved".

Big idea for the week: you can be brave because you are loved. God is with you
(so you don't have to be afraid) and God loves you (so you don't have to earn it).
Morning posts are cheerful "be brave" verses, bedtime posts are calm "you are loved / safe" verses.

5 posts per day:
  06:00 pagi   VERSE (slot "pagi")  - Eli verse image / Reel, cheerful
  09:00 pagi2  EDUKASI "Eli Learns" - carousel (question -> 2 answer slides -> close + verse)
  12:00 siang  SARAN   list carousel (relatable / shareable: nostalgic church-kid lists + practical tips)
  17:00 sore   KUIS    Bible quiz, 1 image, answer at the end of the caption
  21:00 malam  VERSE (slot "malam") - Eli verse image / Reel, calm bedtime

Schemas mirror konten/eli_variasi.py exactly (EDUKASI / SARAN / KUIS keys). As in week 1,
EDUKASI and SARAN captions have NO hashtags (the renderer appends "\\n.\\n.\\n" + TAGS) and
KUIS has no caption (the renderer builds it, answer hidden at the end). VERSE captions
already include TAGS.

Bible quotes: World English Bible (WEB, public domain) unless marked KJV in a comment
(KJV is used where WEB says "Yahweh", which is harder for young kids to read aloud).
Facts in EDUKASI were checked; measurements are approximate and say "about".
Christmas (about 11 weeks away) is only gently anticipated once: EDUKASI day 7 (Immanuel).
"""

TAGS = ("#sahabateli #bibleforkids #kidsdevotional #sundayschool #christianparenting "
        "#faithfamily #christiankids #bibleverse #braveandloved #kidsmin")

_T = "\n.\n.\n" + TAGS

VERSE = [
    # ---- Hari 1 - Sunday 4 Oct ----
    {"hari": 1, "slot": "pagi", "bubble": "It's a brand new week!",
     "kutipan": "“This is the day which the LORD hath made; we will rejoice and be glad in it.”",  # KJV
     "ref": "Psalm 118:24",
     "caption": "Good morning, friends! ☀️\n\nEli is starting a brand new week, and this week's theme is BRAVE & LOVED 💙\n\n📖 Psalm 118:24\n“This is the day which the LORD hath made; we will rejoice and be glad in it.”\n\nIt's Sunday! Whether you're at church, at home, or on the road, today is a gift from God 🎁\n\nWhat's one happy thing about your Sunday? Tell Eli below 👇" + _T},
    {"hari": 1, "slot": "malam", "bubble": "You are God's child!",
     "kutipan": "“See how great a love the Father has given to us, that we should be called children of God!”",
     "ref": "1 John 3:1",
     "caption": "Goodnight, little friend 🌙\n\nBefore you sleep, Eli wants you to remember who you are.\n\n📖 1 John 3:1\n“See how great a love the Father has given to us, that we should be called children of God!”\n\nNot because you were perfect today. Just because He loves you 💙\n\nParents: whisper this one to your kids tonight. Type 💙 if you did!" + _T},

    # ---- Hari 2 - Monday 5 Oct ----
    {"hari": 2, "slot": "pagi", "bubble": "Brave Monday, go!",
     "kutipan": "“Don’t you be afraid, for I am with you. Don’t be dismayed, for I am your God.”",
     "ref": "Isaiah 41:10",
     "caption": "Happy Monday! 🌤️\n\nNew week, new things, maybe a few wobbly feelings too. That's okay!\n\n📖 Isaiah 41:10\n“Don’t you be afraid, for I am with you. Don’t be dismayed, for I am your God.”\n\nEli's brave plan for today: take a deep breath and remember God is right there 🙌\n\nWhat's one thing you need to be brave for this week? 👇" + _T},
    {"hari": 2, "slot": "malam", "bubble": "Sweet dreams!",
     "kutipan": "“When you lie down, you will not be afraid. Yes, you will lie down, and your sleep will be sweet.”",
     "ref": "Proverbs 3:24",
     "caption": "Time for bed, friends 🌙✨\n\nLights off, blankets up, and one sweet promise to hold onto.\n\n📖 Proverbs 3:24\n“When you lie down, you will not be afraid. Yes, you will lie down, and your sleep will be sweet.”\n\nEli is saying a little prayer for everyone reading this 🙏\n\nWho do you want Eli to pray for tonight? Write their first name below 👇" + _T},

    # ---- Hari 3 - Tuesday 6 Oct ----
    {"hari": 3, "slot": "pagi", "bubble": "God made me brave!",
     "kutipan": "“For God didn’t give us a spirit of fear, but of power, love, and self-control.”",
     "ref": "2 Timothy 1:7",
     "caption": "Good morning! 💪☀️\n\nEli found a superpower verse today!\n\n📖 2 Timothy 1:7\n“For God didn’t give us a spirit of fear, but of power, love, and self-control.”\n\nPower to do hard things. Love for the people around you. Self-control when you feel grumpy 😅\n\nWhich one do YOU need most today: POWER, LOVE, or SELF-CONTROL? 👇" + _T},
    {"hari": 3, "slot": "malam", "bubble": "When I'm scared...",
     "kutipan": "“When I am afraid, I will put my trust in you.”",
     "ref": "Psalm 56:3",
     "caption": "Goodnight, friends 🌙\n\nIs it a little dark? A little quiet? Eli has a tiny verse that's easy to remember:\n\n📖 Psalm 56:3\n“When I am afraid, I will put my trust in you.”\n\nIt's only 11 words. Can you say it with your eyes closed? 😴\n\nParents: this is a perfect first memory verse. Save it for bedtime 🔖" + _T},

    # ---- Hari 4 - Wednesday 7 Oct ----
    {"hari": 4, "slot": "pagi", "bubble": "God knows my name!",
     "kutipan": "“Don’t be afraid, for I have redeemed you. I have called you by your name. You are mine.”",
     "ref": "Isaiah 43:1",
     "caption": "Happy Wednesday! 🌈\n\nDid you know God knows your name? Not just \"a kid\" but YOU 💙\n\n📖 Isaiah 43:1\n“Don’t be afraid, for I have redeemed you. I have called you by your name. You are mine.”\n\nEli loves that last part: You are mine 🥹\n\nWrite your first name in the comments and Eli will say hi! 👋" + _T},
    {"hari": 4, "slot": "malam", "bubble": "Angels on guard!",
     "kutipan": "“For he will put his angels in charge of you, to guard you in all your ways.”",
     "ref": "Psalm 91:11",
     "caption": "Goodnight, little one 🌙⭐\n\nWhile you sleep, God is still wide awake and taking care of you.\n\n📖 Psalm 91:11\n“For he will put his angels in charge of you, to guard you in all your ways.”\n\nSnuggle in and rest. You are safe in God's hands 💙\n\nSend this to a family who could use a peaceful night 🤍" + _T},

    # ---- Hari 5 - Thursday 8 Oct ----
    {"hari": 5, "slot": "pagi", "bubble": "God is on my team!",
     "kutipan": "“If God is for us, who can be against us?”",
     "ref": "Romans 8:31",
     "caption": "Good morning, team! 🙌\n\nEli has the BEST teammate ever.\n\n📖 Romans 8:31\n“If God is for us, who can be against us?”\n\nWhen something feels too big today, remember whose team you're on 💪\n\nType \"TEAM GOD\" if you're in! 👇" + _T},
    {"hari": 5, "slot": "malam", "bubble": "Loved forever!",
     "kutipan": "“Yes, I have loved you with an everlasting love.”",
     "ref": "Jeremiah 31:3",
     "caption": "Goodnight, friends 🌙\n\nForever is a really, really long time. And that's how long God's love lasts 💙\n\n📖 Jeremiah 31:3\n“Yes, I have loved you with an everlasting love.”\n\nNo bad day, no mistake, no grumpy moment can switch it off.\n\nDrop a 💙 for someone you love, and tag them so they see it" + _T},

    # ---- Hari 6 - Friday 9 Oct ----
    {"hari": 6, "slot": "pagi", "bubble": "I'm wonderfully made!",
     "kutipan": "“I will give thanks to you, for I am fearfully and wonderfully made.”",
     "ref": "Psalm 139:14",
     "caption": "Happy Friday! 🎉\n\nLook in the mirror today and say it with Eli: \"God made me WONDERFUL!\" 🪞\n\n📖 Psalm 139:14\n“I will give thanks to you, for I am fearfully and wonderfully made.”\n\nYour freckles, your laugh, your curly hair or straight hair: God made it all on purpose ✨\n\nWhat's one thing you like about how God made you? 👇" + _T},
    {"hari": 6, "slot": "malam", "bubble": "Love beats fear!",
     "kutipan": "“There is no fear in love; but perfect love casts out fear.”",
     "ref": "1 John 4:18",
     "caption": "Goodnight, brave friends 🌙\n\nEli learned something tonight: love is stronger than fear 💙\n\n📖 1 John 4:18\n“There is no fear in love; but perfect love casts out fear.”\n\nWhen you feel scared, remember how much God loves you. His love pushes the scary feelings out 🤍\n\nWhat helps you feel safe at night? A nightlight? A cuddle? Tell Eli 👇" + _T},

    # ---- Hari 7 - Saturday 10 Oct ----
    {"hari": 7, "slot": "pagi", "bubble": "Morning, God!",
     "kutipan": "“Cause me to hear your loving kindness in the morning, for I trust in you.”",
     "ref": "Psalm 143:8",
     "caption": "Saturday morning! 🥞☀️\n\nPancakes, playtime, and a little chat with God before the fun starts.\n\n📖 Psalm 143:8\n“Cause me to hear your loving kindness in the morning, for I trust in you.”\n\nEli's weekend challenge: say \"Good morning, God!\" before you get out of bed 😄\n\nWhat are you doing this weekend? 👇" + _T},
    {"hari": 7, "slot": "malam", "bubble": "Always with you!",
     "kutipan": "“Behold, I am with you always, even to the end of the age.”",
     "ref": "Matthew 28:20",
     "caption": "Goodnight, friends 🌙\n\nWhat a week! We learned we can be BRAVE because we are LOVED 💙\n\n📖 Matthew 28:20\n“Behold, I am with you always, even to the end of the age.”\n\nJesus is with you tonight, tomorrow at church, and every single day.\n\nWhich verse from this week was your favourite? Tell Eli 👇 See you tomorrow!" + _T},
]

EDUKASI = [
    {"tanya": "What does “Gospel” mean?",
     "jawab": [("Good news!", "“Gospel” means “good news.” The word in the New Testament is the Greek word euangelion, and the old English word “godspel” meant good news too."),
               ("Four Gospels", "Matthew, Mark, Luke, and John are called the Gospels. They tell the good news about Jesus: how He lived, loved people, died, and rose again.")],
     "tutup": "The best news ever is about Jesus!",
     "ayat": "“For God so loved the world, that he gave his one and only Son…”", "ref": "John 3:16",
     "caption": "Eli learned a new word today: GOSPEL 📖\n\nIt means \"good news\"! Matthew, Mark, Luke, and John are the four Gospels, and they tell the good news about Jesus.\n\n📖 John 3:16\n\nWhich Gospel story is your favourite? Tell Eli 👇"},
    {"tanya": "How big was Goliath?",
     "jawab": [("Super tall!", "The Bible says Goliath was “six cubits and a span” tall (1 Samuel 17:4). That's about 3 metres, or over 9 feet!"),
               ("Five small stones", "David picked five smooth stones from a stream (1 Samuel 17:40). He was brave because he trusted God, not because he was big.")],
     "tutup": "Big problems are small to God!",
     "ayat": "“…for the battle is the LORD’s…”", "ref": "1 Samuel 17:47",
     "caption": "Eli learned about the bravest shepherd boy 🪨\n\nGoliath was about 3 metres (over 9 feet) tall! But David wasn't scared, because he knew God was bigger 💪\n\n📖 1 Samuel 17:47 (KJV)\n\nWhat's a \"Goliath\" you're facing this week? Eli will pray for you 🙏"},
    {"tanya": "Who was brave Queen Esther?",
     "jawab": [("A girl who became queen", "Esther was a Jewish girl raised by her cousin Mordecai (Esther 2:7). She became queen of Persia."),
               ("She spoke up", "Going to the king without being called was very dangerous. But Esther was brave and asked him to save her people, and God used her to rescue them.")],
     "tutup": "God can use you, right where you are!",
     "ayat": "“…Who knows if you haven’t come to the kingdom for such a time as this?”", "ref": "Esther 4:14",
     "caption": "Eli learned about a brave queen 👑\n\nEsther spoke up for her people even though she was scared, and God used her to save them 💙\n\n📖 Esther 4:14\n\nWho is someone brave you look up to? Tell Eli 👇"},
    {"tanya": "How big was Noah's ark?",
     "jawab": [("Really, really big", "God told Noah to make it 300 cubits long, 50 wide, and 30 high (Genesis 6:15). That's about 135 metres long, longer than a soccer field!"),
               ("A rainbow promise", "After the flood, God put a rainbow in the sky as a promise to Noah and to the whole earth (Genesis 9:13).")],
     "tutup": "Every rainbow says: God keeps His promises!",
     "ayat": "“I set my rainbow in the cloud, and it will be a sign of a covenant between me and the earth.”", "ref": "Genesis 9:13",
     "caption": "Eli learned how BIG Noah's ark was 🚢\n\nAbout 135 metres long! That's longer than a soccer field 😮 And after the flood, God gave the rainbow as His promise 🌈\n\n📖 Genesis 9:13\n\nNext time you see a rainbow, what will you remember? 👇"},
    {"tanya": "Why wasn't Daniel scared?",
     "jawab": [("He kept praying", "Even when a law said not to, Daniel kept praying to God three times a day, with his windows open (Daniel 6:10)."),
               ("Lions with shut mouths", "Daniel was thrown into the lions' den. But God sent His angel and shut the lions' mouths, and Daniel was safe (Daniel 6:22).")],
     "tutup": "Keep talking to God, like Daniel!",
     "ayat": "“My God has sent his angel, and has shut the lions’ mouths, and they have not hurt me…”", "ref": "Daniel 6:22",
     "caption": "Eli learned about Daniel and the lions 🦁\n\nDaniel prayed three times a day, even when it was against the rules. And God kept him safe in the lions' den!\n\n📖 Daniel 6:22\n\nWhen do you like to pray: morning, lunch, or bedtime? 👇"},
    {"tanya": "Did Jesus have time for kids?",
     "jawab": [("Let them come!", "When people brought children to Jesus, His disciples tried to send them away. Jesus wasn't happy about that at all! (Mark 10:13-14)"),
               ("Big hugs", "Jesus took the children in His arms and blessed them (Mark 10:16). Kids matter to Jesus!")],
     "tutup": "Jesus always has time for you!",
     "ayat": "“Allow the little children to come to me! Don’t forbid them, for God’s Kingdom belongs to such as these.”", "ref": "Mark 10:14",
     "caption": "Eli's favourite fact this week 💙\n\nWhen the disciples tried to send kids away, Jesus said \"Let them come!\" Then He hugged and blessed them 🤗\n\n📖 Mark 10:14\n\nParents: tell your kids today that Jesus has time for them. Share with a family who needs this 🤍"},
    {"tanya": "What does “Immanuel” mean?",
     "jawab": [("God with us", "“Immanuel” means “God with us.” It's one of the special names for Jesus (Matthew 1:23)."),
               ("An old promise", "The prophet Isaiah wrote about Immanuel (Isaiah 7:14) about 700 years before Jesus was born. God kept His promise at the very first Christmas!")],
     "tutup": "God with us, every single day!",
     "ayat": "“…They shall call his name Immanuel; which is, being interpreted, ‘God with us.’”", "ref": "Matthew 1:23",
     "caption": "Eli learned a beautiful name for Jesus: IMMANUEL ✨\n\nIt means \"God with us.\" Christmas is still about 11 weeks away, but this name is true every day of the year 💙\n\n📖 Matthew 1:23\n\nDo you know another name for Jesus? Write it below 👇"},
]

SARAN = [
    {"judul": "Church kid signs",
     "tips": [("You know the actions", "“Father Abraham had many sons…” and you still do every move."),
              ("After-church snacks", "Biscuits and cordial after the service hit different."),
              ("The books song", "Genesis, Exodus, Leviticus… you can still sing it!"),
              ("Cotton wool sheep", "Every Sunday school craft needed glue. So much glue.")],
     "ayat": "“Behold, how good and how pleasant it is for brethren to dwell together in unity!”", "ref": "Psalm 133:1",  # KJV
     "caption": "You know you grew up in church when… 😄⛪\n\n1. You still know the \"Father Abraham\" actions\n2. After-church biscuits and cordial were the best part\n3. You can sing the books of the Bible\n4. Cotton wool sheep. Enough said.\n\nWhich one is SO you? Tag a friend who grew up in church too 👇"},
    {"judul": "Ways to be kind",
     "tips": [("Share something", "A snack, a toy, or a turn on the swing."),
              ("“Sit with us!”", "Look for the kid who is alone and invite them in."),
              ("Write a thank-you note", "For a teacher, a grandparent, or the bus driver."),
              ("Help without being asked", "Set the table or pick up toys before anyone says so.")],
     "ayat": "“And be kind to one another, tender hearted, forgiving each other, just as God also in Christ forgave you.”", "ref": "Ephesians 4:32",
     "caption": "Little ways to be kind this week, from Eli 💛\n\n1. Share something\n2. Say \"Sit with us!\"\n3. Write a thank-you note\n4. Help without being asked\n\n📖 Ephesians 4:32\n\nSave this for your family and try one today 🔖 Which one will you pick?"},
    {"judul": "Praying when scared",
     "tips": [("Keep it simple", "“Jesus, please help me” is a real prayer. God hears it."),
              ("Breathe slowly", "Breathe in… and out. Tell God what feels scary."),
              ("Say a verse", "“When I am afraid, I will put my trust in you.”"),
              ("Tell a grown-up", "God often helps us through people who love us.")],
     "ayat": "“I sought the LORD, and he heard me, and delivered me from all my fears.”", "ref": "Psalm 34:4",  # KJV
     "caption": "How to pray when you're scared, from Eli 💙\n\n1. Keep it simple: \"Jesus, help me\"\n2. Breathe slowly and tell God what's scary\n3. Say a verse you know\n4. Tell a grown-up you trust\n\nIf a scared feeling stays for a long time, please talk to a parent, teacher, or counsellor. You don't have to carry it alone 🤍\n\nSave this for tricky nights 🔖"},
    {"judul": "Things church kids know",
     "tips": [("“One last song”", "It was never the last song."),
              ("The rumbly tummy", "Trying not to giggle when your tummy growls in prayer time."),
              ("The best seat", "Near the door, near the snacks, far from the front!"),
              ("Memory verse lollies", "Say it by heart, get a lolly. Totally worth it.")],
     "ayat": "“Make a joyful noise unto the LORD, all ye lands.”", "ref": "Psalm 100:1",  # KJV
     "caption": "Things only church kids understand 😂\n\n1. \"One last song\" is never the last song\n2. The rumbly tummy during prayer\n3. Picking the seat near the snacks\n4. Memory verse = lolly\n\n📖 Psalm 100:1\n\nWhat would you add to the list? 👇 Share with your church friends!"},
    {"judul": "Brave at bedtime",
     "tips": [("Nightlights are okay", "Lots of brave people sleep with a little light on!"),
              ("Say a bedtime verse", "Pick one short verse and say it every night."),
              ("Pray for someone else", "Thinking about others helps our hearts feel calm."),
              ("Talk about bad dreams", "Tell a parent in the morning. Bad dreams can't hurt you.")],
     "ayat": "“I laid me down and slept; I awaked; for the LORD sustained me.”", "ref": "Psalm 3:5",  # KJV
     "caption": "Eli's tips for being brave at bedtime 🌙\n\n1. Nightlights are totally okay\n2. Say a bedtime verse\n3. Pray for someone else\n4. Talk about bad dreams in the morning\n\n📖 Psalm 3:5\n\nParents: what's your family's bedtime routine? Share your tips below 👇"},
    {"judul": "Sunday school memories",
     "tips": [("Felt board stories", "Moses and Noah never looked so fuzzy."),
              ("Songs with big actions", "“My God is so big…” with arms stretched wide!"),
              ("The offering coin", "Holding it tight the whole time so you didn't lose it."),
              ("Gold star stickers", "One more for the chart, please!")],
     "ayat": "“One generation will commend your works to another, and will declare your mighty acts.”", "ref": "Psalm 145:4",
     "caption": "Sunday school memories, anyone? 🥹⭐\n\n1. Felt board Bible stories\n2. \"My God is so big\" with all the actions\n3. Holding your offering coin super tight\n4. Gold star stickers\n\n📖 Psalm 145:4\n\nWhich one brings back memories? Tag your old Sunday school friend 👇"},
    {"judul": "Reminders you are loved",
     "tips": [("God made you on purpose", "You are wonderfully made (Psalm 139:14)."),
              ("God knows your name", "He calls you His own (Isaiah 43:1)."),
              ("Mistakes don't stop His love", "You can say sorry and start again, every time."),
              ("You are never alone", "Jesus is with you always (Matthew 28:20).")],
     "ayat": "“Behold, I have engraved you on the palms of my hands.”", "ref": "Isaiah 49:16",
     "caption": "Little reminders for little hearts 💙\n\n1. God made you on purpose\n2. God knows your name\n3. Mistakes don't stop His love\n4. You are never alone\n\n📖 Isaiah 49:16\n\nSend this to a kid (or a grown-up!) who needs to hear it today 🤍"},
]

KUIS = [
    {"tanya": "Who walked on water toward Jesus?", "pilihan": ["John", "Peter", "Andrew"],
     "jawab": "B. Peter (Matthew 14:29)"},
    {"tanya": "What did Jesus say to the stormy sea?", "pilihan": ["“Peace! Be still!”", "“Go away!”", "“Stop raining!”"],
     "jawab": "A. “Peace! Be still!” (Mark 4:39)"},
    {"tanya": "How many smooth stones did David pick up?", "pilihan": ["3 stones", "5 stones", "7 stones"],
     "jawab": "B. 5 smooth stones (1 Samuel 17:40)"},
    {"tanya": "Which brave queen saved her people?", "pilihan": ["Ruth", "Miriam", "Esther"],
     "jawab": "C. Queen Esther (Esther 4:14-16)"},
    {"tanya": "What did God put in the sky as a promise?", "pilihan": ["A star", "A rainbow", "A big cloud"],
     "jawab": "B. A rainbow (Genesis 9:13)"},
    {"tanya": "Who was kept safe in the lions' den?", "pilihan": ["Daniel", "Joseph", "Jonah"],
     "jawab": "A. Daniel (Daniel 6:22)"},
    {"tanya": "Who stopped to help the hurt man?", "pilihan": ["The priest", "The Samaritan", "The Levite"],
     "jawab": "B. The Good Samaritan (Luke 10:33-34)"},
]

# hari -> {slot: (format, indeks)}. Slot pagi (06:00) & malam (21:00) come from VERSE.
JADWAL = {h: {"pagi2": ("edukasi", h - 1), "siang": ("saran", h - 1), "sore": ("kuis", h - 1)} for h in range(1, 8)}
