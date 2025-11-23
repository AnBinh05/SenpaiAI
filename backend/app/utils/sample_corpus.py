# Sample Japanese Learning Corpus
# This file contains Japanese learning materials for SenpaiAI

SAMPLE_DOCUMENTS = [
    {
        "id": 1,
        "title": "Basic Greetings - N5",
        "content": """
こんにちは (konnichiwa) - Hello (used during the day)
おはよう (ohayou) - Good morning
こんばんは (konbanwa) - Good evening
さようなら (sayounara) - Goodbye
ありがとう (arigatou) - Thank you
すみません (sumimasen) - Excuse me / Sorry
ごめんなさい (gomennasai) - I'm sorry
はい (hai) - Yes
いいえ (iie) - No
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["greetings", "basic", "polite"],
        "source_url": "https://example.com/basic-greetings"
    },
    {
        "id": 2,
        "title": "Particle は (wa) - N5",
        "content": """
The particle は (wa) is used to mark the topic of a sentence.

Examples:
- わたしは学生です (watashi wa gakusei desu) - I am a student
- これは本です (kore wa hon desu) - This is a book
- 今日は暑いです (kyou wa atsui desu) - Today is hot

Note: は is pronounced "wa" when used as a particle, not "ha"
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["particles", "topic", "basic"],
        "source_url": "https://example.com/particle-wa"
    },
    {
        "id": 3,
        "title": "Numbers 1-10 - N5",
        "content": """
いち (ichi) - 1
に (ni) - 2
さん (san) - 3
よん/し (yon/shi) - 4
ご (go) - 5
ろく (roku) - 6
なな/しち (nana/shichi) - 7
はち (hachi) - 8
きゅう/く (kyuu/ku) - 9
じゅう (juu) - 10

Note: 4 can be pronounced as either よん or し, and 7 as なな or しち
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["numbers", "counting", "basic"],
        "source_url": "https://example.com/numbers"
    },
    {
        "id": 4,
        "title": "Particle を (wo/o) - N5",
        "content": """
The particle を (wo/o) marks the direct object of a verb.

Examples:
- 本を読みます (hon wo yomimasu) - I read a book
- コーヒーを飲みます (koohii wo nomimasu) - I drink coffee
- 音楽を聞きます (ongaku wo kikimasu) - I listen to music

Note: を is pronounced "o" when used as a particle
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["particles", "object", "basic"],
        "source_url": "https://example.com/particle-wo"
    },
    {
        "id": 5,
        "title": "Family Members - N5",
        "content": """
お父さん (otousan) - Father
お母さん (okaasan) - Mother
お兄さん (oniisan) - Older brother
お姉さん (oneesan) - Older sister
弟 (otouto) - Younger brother
妹 (imouto) - Younger sister
祖父 (sofu) - Grandfather
祖母 (sobo) - Grandmother

Note: お父さん and お母さん are polite forms used when referring to someone else's parents
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["family", "relationships", "polite"],
        "source_url": "https://example.com/family"
    },
    {
        "id": 6,
        "title": "Te-form Conjugation - N4",
        "content": """
The te-form is used to connect verbs and express various meanings.

Rules for te-form:
- Group 1 verbs (五段動詞): Change the last syllable
  - 書く (kaku) → 書いて (kaite)
  - 読む (yomu) → 読んで (yonde)
  - 話す (hanasu) → 話して (hanashite)

- Group 2 verbs (一段動詞): Replace る with て
  - 食べる (taberu) → 食べて (tabete)
  - 見る (miru) → 見て (mite)

- Irregular verbs:
  - する (suru) → して (shite)
  - 来る (kuru) → 来て (kite)

Uses: Progressive tense, requests, connecting sentences
        """,
        "document_type": "grammar",
        "jlpt_level": "N4",
        "tags": ["te-form", "conjugation", "verbs"],
        "source_url": "https://example.com/te-form"
    },
    {
        "id": 7,
        "title": "Conditional Forms - N3",
        "content": """
There are several ways to express conditions in Japanese:

1. ば (ba) form - General condition
   - 安ければ買います (yasukereba kaimasu) - If it's cheap, I'll buy it

2. たら (tara) form - Specific condition
   - 時間があったら行きます (jikan ga attara ikimasu) - If I have time, I'll go

3. なら (nara) form - Assumption-based condition
   - 日本に行くなら桜を見たい (nihon ni iku nara sakura wo mitai) - If I go to Japan, I want to see cherry blossoms

4. と (to) form - Natural consequence
   - 春になると桜が咲きます (haru ni naru to sakura ga sakimasu) - When spring comes, cherry blossoms bloom
        """,
        "document_type": "grammar",
        "jlpt_level": "N3",
        "tags": ["conditionals", "advanced", "complex"],
        "source_url": "https://example.com/conditionals"
    },
    {
        "id": 8,
        "title": "Keigo (Honorific Language) - N2",
        "content": """
Keigo is the polite language system in Japanese with three main types:

1. 尊敬語 (sonkeigo) - Respectful language
   - いらっしゃる (irassharu) - to go/come/be (respectful)
   - おっしゃる (ossharu) - to say (respectful)

2. 謙譲語 (kenjougo) - Humble language
   - 参る (mairu) - to go/come (humble)
   - 申す (mousu) - to say (humble)

3. 丁寧語 (teineigo) - Polite language
   - です/ます forms

Examples:
- 先生がおっしゃいました (sensei ga osshaimashita) - The teacher said (respectful)
- 私が申し上げます (watashi ga moushiagemasu) - I will say (humble)
        """,
        "document_type": "grammar",
        "jlpt_level": "N2",
        "tags": ["keigo", "honorific", "business", "formal"],
        "source_url": "https://example.com/keigo"
    },
    {
        "id": 9,
        "title": "Advanced Sentence Patterns - N1",
        "content": """
Complex sentence patterns for advanced learners:

1. ～ば～ほど (ba hodo) - The more... the more...
   - 勉強すればするほど難しくなります (benkyou sureba suru hodo muzukashiku narimasu) - The more you study, the more difficult it becomes

2. ～に限らず (ni kagirazu) - Not limited to
   - 日本人に限らず、誰でも参加できます (nihonjin ni kagirazu, dare demo sanka dekimasu) - Not limited to Japanese people, anyone can participate

3. ～を問わず (wo towazu) - Regardless of
   - 年齢を問わず応募できます (nenrei wo towazu oubo dekimasu) - You can apply regardless of age

4. ～に応じて (ni oujite) - According to
   - 能力に応じて給料が決まります (nouryoku ni oujite kyuuryou ga kimarimasu) - Salary is determined according to ability
        """,
        "document_type": "grammar",
        "jlpt_level": "N1",
        "tags": ["advanced", "complex", "patterns", "formal"],
        "source_url": "https://example.com/advanced-patterns"
    },
    {
        "id": 10,
        "title": "Japanese Culture - Business Etiquette",
        "content": """
Important aspects of Japanese business culture:

1. 名刺交換 (meishi koukan) - Business card exchange
   - Always exchange cards with both hands
   - Read the card carefully before putting it away
   - Never write on someone's business card

2. お辞儀 (ojigi) - Bowing
   - 15 degrees for casual greeting
   - 30 degrees for business greeting
   - 45 degrees for apology or deep respect

3. 時間厳守 (jikan genshu) - Punctuality
   - Always arrive 5-10 minutes early
   - Being late is considered very rude

4. 和室 (washitsu) - Traditional Japanese rooms
   - Remove shoes before entering
   - Sit in seiza position if possible
   - Don't step on the threshold
        """,
        "document_type": "culture",
        "jlpt_level": "N2",
        "tags": ["business", "culture", "etiquette", "social"],
        "source_url": "https://example.com/business-culture"
    }
]

# Additional vocabulary sets
VOCABULARY_SETS = [
    {
        "id": 11,
        "title": "Colors - N5",
        "content": """
赤 (aka) - Red
青 (ao) - Blue
黄色 (kiiro) - Yellow
緑 (midori) - Green
黒 (kuro) - Black
白 (shiro) - White
茶色 (chairo) - Brown
灰色 (haiiro) - Gray
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["colors", "basic", "descriptive"],
        "source_url": "https://example.com/colors"
    },
    {
        "id": 12,
        "title": "Time Expressions - N5",
        "content": """
今日 (kyou) - Today
昨日 (kinou) - Yesterday
明日 (ashita) - Tomorrow
今 (ima) - Now
朝 (asa) - Morning
昼 (hiru) - Noon/Afternoon
夜 (yoru) - Night
午前 (gozen) - AM
午後 (gogo) - PM
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["time", "basic", "daily"],
        "source_url": "https://example.com/time"
    }
]

# Combine all documents
ALL_DOCUMENTS = SAMPLE_DOCUMENTS + VOCABULARY_SETS


