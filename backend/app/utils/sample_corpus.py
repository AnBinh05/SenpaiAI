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
        "source_url": "https://www.tofugu.com/japanese/japanese-greetings/"
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
        "source_url": "https://guidetojapanese.org/learn/grammar/particlesintro"
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
        "source_url": "https://www.jlptsensei.com/japanese-numbers/"
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
        "source_url": "https://guidetojapanese.org/learn/grammar/particlesintro"
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
        "source_url": "https://www.jlptsensei.com/japanese-family-members/"
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
        "source_url": "https://guidetojapanese.org/learn/grammar/teform"
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
        "source_url": "https://www.imabi.net/conditionals.htm"
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
        "source_url": "https://guidetojapanese.org/learn/grammar/keigo"
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
        "source_url": "https://www.imabi.net/advancedpatterns.htm"
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
        "source_url": "https://www.tofugu.com/japanese/japanese-business-culture/"
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
        "source_url": "https://www.jlptsensei.com/japanese-colors/"
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
        "source_url": "https://www.jlptsensei.com/japanese-time-expressions/"
    }
]

# Additional new documents with real URLs
NEW_DOCUMENTS = [
    {
        "id": 13,
        "title": "Hiragana Chart - N5",
        "content": """
Hiragana is one of the three Japanese writing systems. It consists of 46 basic characters.

Basic Hiragana:
あ (a) い (i) う (u) え (e) お (o)
か (ka) き (ki) く (ku) け (ke) こ (ko)
さ (sa) し (shi) す (su) せ (se) そ (so)
た (ta) ち (chi) つ (tsu) て (te) と (to)
な (na) に (ni) ぬ (nu) ね (ne) の (no)
は (ha) ひ (hi) ふ (fu) へ (he) ほ (ho)
ま (ma) み (mi) む (mu) め (me) も (mo)
や (ya) ゆ (yu) よ (yo)
ら (ra) り (ri) る (ru) れ (re) ろ (ro)
わ (wa) を (wo) ん (n)

Hiragana is used for native Japanese words and grammatical elements.
        """,
        "document_type": "lesson",
        "jlpt_level": "N5",
        "tags": ["hiragana", "writing", "alphabet", "beginner"],
        "source_url": "https://www.tofugu.com/japanese/learn-hiragana/"
    },
    {
        "id": 14,
        "title": "Katakana Chart - N5",
        "content": """
Katakana is used for foreign words, loanwords, and emphasis.

Basic Katakana:
ア (a) イ (i) ウ (u) エ (e) オ (o)
カ (ka) キ (ki) ク (ku) ケ (ke) コ (ko)
サ (sa) シ (shi) ス (su) セ (se) ソ (so)
タ (ta) チ (chi) ツ (tsu) テ (te) ト (to)
ナ (na) ニ (ni) ヌ (nu) ネ (ne) ノ (no)
ハ (ha) ヒ (hi) フ (fu) ヘ (he) ホ (ho)
マ (ma) ミ (mi) ム (mu) メ (me) モ (mo)
ヤ (ya) ユ (yu) ヨ (yo)
ラ (ra) リ (ri) ル (ru) レ (re) ロ (ro)
ワ (wa) ヲ (wo) ン (n)

Katakana is often used for foreign names, technical terms, and onomatopoeia.
        """,
        "document_type": "lesson",
        "jlpt_level": "N5",
        "tags": ["katakana", "writing", "alphabet", "beginner"],
        "source_url": "https://www.tofugu.com/japanese/learn-katakana/"
    },
    {
        "id": 15,
        "title": "Particle が (ga) - N5",
        "content": """
The particle が (ga) has several important functions:

1. Subject marker:
   - 雨が降っています (ame ga futte imasu) - It is raining
   - 私が行きます (watashi ga ikimasu) - I will go

2. Contrast marker:
   - コーヒーは飲みますが、お茶は飲みません (koohii wa nomimasu ga, ocha wa nomimasen) - I drink coffee, but I don't drink tea

3. With question words:
   - 誰が来ましたか (dare ga kimashita ka) - Who came?
   - 何が欲しいですか (nani ga hoshii desu ka) - What do you want?

Note: が marks the subject, while は marks the topic.
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["particles", "subject", "contrast", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/particlesintro"
    },
    {
        "id": 16,
        "title": "Particle に (ni) - N5",
        "content": """
The particle に (ni) has multiple uses:

1. Direction/Location:
   - 学校に行きます (gakkou ni ikimasu) - I go to school
   - 机の上に本があります (tsukue no ue ni hon ga arimasu) - There is a book on the desk

2. Time:
   - 三時に会いましょう (sanji ni aimashou) - Let's meet at 3 o'clock
   - 月曜日に始まります (getsuyoubi ni hajimarimasu) - It starts on Monday

3. Purpose:
   - 買い物に行きます (kaimono ni ikimasu) - I go shopping
   - 勉強に来ました (benkyou ni kimashita) - I came to study

4. Indirect object:
   - 友達に手紙を書きます (tomodachi ni tegami wo kakimasu) - I write a letter to my friend
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["particles", "location", "time", "purpose", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/particlesintro"
    },
    {
        "id": 17,
        "title": "Particle で (de) - N5",
        "content": """
The particle で (de) indicates:

1. Location of action:
   - 図書館で勉強します (toshokan de benkyou shimasu) - I study at the library
   - レストランで食べます (resutoran de tabemasu) - I eat at a restaurant

2. Means/Method:
   - 電車で行きます (densha de ikimasu) - I go by train
   - 日本語で話します (nihongo de hanashimasu) - I speak in Japanese

3. Tool/Instrument:
   - ペンで書きます (pen de kakimasu) - I write with a pen
   - 箸で食べます (hashi de tabemasu) - I eat with chopsticks

4. Cause/Reason:
   - 風邪で休みました (kaze de yasumimashita) - I took a day off due to a cold
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["particles", "location", "method", "tool", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/particlesintro"
    },
    {
        "id": 18,
        "title": "Food Vocabulary - N5",
        "content": """
Common Japanese food vocabulary:

主食 (shushoku) - Staple foods:
ご飯 (gohan) - Rice
パン (pan) - Bread
麺 (men) - Noodles

料理 (ryouri) - Dishes:
寿司 (sushi) - Sushi
刺身 (sashimi) - Sashimi
天ぷら (tenpura) - Tempura
ラーメン (raamen) - Ramen
うどん (udon) - Udon noodles
そば (soba) - Soba noodles

飲み物 (nomimono) - Drinks:
水 (mizu) - Water
お茶 (ocha) - Tea
コーヒー (koohii) - Coffee
ビール (biiru) - Beer
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["food", "vocabulary", "daily", "culture"],
        "source_url": "https://www.jlptsensei.com/japanese-food-vocabulary/"
    },
    {
        "id": 19,
        "title": "Body Parts - N5",
        "content": """
Body parts in Japanese:

頭 (atama) - Head
目 (me) - Eye
耳 (mimi) - Ear
鼻 (hana) - Nose
口 (kuchi) - Mouth
顔 (kao) - Face
首 (kubi) - Neck
肩 (kata) - Shoulder
手 (te) - Hand
腕 (ude) - Arm
胸 (mune) - Chest
お腹 (onaka) - Stomach
足 (ashi) - Leg/Foot
背中 (senaka) - Back

Example sentences:
- 頭が痛いです (atama ga itai desu) - My head hurts
- 手を洗います (te wo araimasu) - I wash my hands
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["body", "vocabulary", "health", "daily"],
        "source_url": "https://www.jlptsensei.com/japanese-body-parts/"
    },
    {
        "id": 20,
        "title": "Adjectives - い and な - N5",
        "content": """
Japanese has two types of adjectives:

1. い-adjectives (i-adjectives):
   - 高い (takai) - expensive/tall
   - 安い (yasui) - cheap
   - 大きい (ookii) - big
   - 小さい (chiisai) - small
   - 暑い (atsui) - hot
   - 寒い (samui) - cold

   Conjugation:
   - Present: 高いです (takai desu) - is expensive
   - Negative: 高くないです (takakunai desu) - is not expensive
   - Past: 高かったです (takakatta desu) - was expensive

2. な-adjectives (na-adjectives):
   - 静か (shizuka) - quiet
   - 元気 (genki) - healthy/energetic
   - きれい (kirei) - beautiful/clean
   - 便利 (benri) - convenient

   Usage: 静かです (shizuka desu) - is quiet
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["adjectives", "grammar", "conjugation", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/adjectives"
    },
    {
        "id": 21,
        "title": "Past Tense - N5",
        "content": """
Past tense in Japanese:

1. Verbs - Past form:
   - 食べる (taberu) → 食べました (tabemashita) - ate
   - 行く (iku) → 行きました (ikimashita) - went
   - する (suru) → しました (shimashita) - did
   - 来る (kuru) → 来ました (kimashita) - came

2. い-adjectives - Past form:
   - 高い (takai) → 高かったです (takakatta desu) - was expensive
   - 暑い (atsui) → 暑かったです (atsukatta desu) - was hot

3. な-adjectives - Past form:
   - 静か (shizuka) → 静かでした (shizuka deshita) - was quiet
   - 元気 (genki) → 元気でした (genki deshita) - was healthy

4. Noun + です - Past form:
   - 学生です → 学生でした (gakusei deshita) - was a student
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["past tense", "grammar", "conjugation", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/past"
    },
    {
        "id": 22,
        "title": "Negative Forms - N5",
        "content": """
Negative forms in Japanese:

1. Verbs - Negative:
   - 食べる (taberu) → 食べません (tabemasen) - don't eat
   - 行く (iku) → 行きません (ikimasen) - don't go
   - する (suru) → しません (shimasen) - don't do

2. い-adjectives - Negative:
   - 高い (takai) → 高くないです (takakunai desu) - is not expensive
   - 暑い (atsui) → 暑くないです (atsukunai desu) - is not hot

3. な-adjectives - Negative:
   - 静か (shizuka) → 静かじゃないです (shizuka janai desu) - is not quiet
   - 元気 (genki) → 元気じゃないです (genki janai desu) - is not healthy

4. Noun + です - Negative:
   - 学生です → 学生じゃないです (gakusei janai desu) - is not a student
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["negative", "grammar", "conjugation", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/negative"
    },
    {
        "id": 23,
        "title": "Potential Form - N4",
        "content": """
Potential form expresses ability or possibility "can do":

Formation:
- Group 1 verbs: Change final う to える
  - 書く (kaku) → 書ける (kakeru) - can write
  - 読む (yomu) → 読める (yomeru) - can read
  - 話す (hanasu) → 話せる (hanaseru) - can speak

- Group 2 verbs: Replace る with られる
  - 食べる (taberu) → 食べられる (taberareru) - can eat
  - 見る (miru) → 見られる (mirareru) - can see

- Irregular:
  - する (suru) → できる (dekiru) - can do
  - 来る (kuru) → 来られる (korareru) - can come

Usage:
- 日本語が話せます (nihongo ga hanasemasu) - I can speak Japanese
- ピアノが弾けます (piano ga hikemasu) - I can play piano
        """,
        "document_type": "grammar",
        "jlpt_level": "N4",
        "tags": ["potential", "ability", "conjugation", "verbs"],
        "source_url": "https://guidetojapanese.org/learn/grammar/potential"
    },
    {
        "id": 24,
        "title": "Passive Form - N4",
        "content": """
Passive form expresses being affected by an action:

Formation:
- Group 1: Change final う to あれる
  - 書く (kaku) → 書かれる (kakareru) - is written
  - 読む (yomu) → 読まれる (yomareru) - is read

- Group 2: Replace る with られる
  - 食べる (taberu) → 食べられる (taberareru) - is eaten

- Irregular:
  - する (suru) → される (sareru) - is done
  - 来る (kuru) → 来られる (korareru) - is come

Usage:
- 私は先生に褒められました (watashi wa sensei ni homeraremashita) - I was praised by the teacher
- この本は多くの人に読まれています (kono hon wa ooku no hito ni yomarete imasu) - This book is read by many people
        """,
        "document_type": "grammar",
        "jlpt_level": "N4",
        "tags": ["passive", "grammar", "conjugation", "verbs"],
        "source_url": "https://guidetojapanese.org/learn/grammar/passive"
    },
    {
        "id": 25,
        "title": "Causative Form - N3",
        "content": """
Causative form expresses making or letting someone do something:

Formation:
- Group 1: Change final う to あせる
  - 書く (kaku) → 書かせる (kakaseru) - make/let write
  - 読む (yomu) → 読ませる (yomaseru) - make/let read

- Group 2: Replace る with させる
  - 食べる (taberu) → 食べさせる (tabesaseru) - make/let eat

- Irregular:
  - する (suru) → させる (saseru) - make/let do
  - 来る (kuru) → 来させる (kosaseru) - make/let come

Usage:
- 子供に本を読ませます (kodomo ni hon wo yomasemasu) - I make the child read a book
- 学生に宿題をさせました (gakusei ni shukudai wo sasemashita) - I made the students do homework
        """,
        "document_type": "grammar",
        "jlpt_level": "N3",
        "tags": ["causative", "grammar", "conjugation", "advanced"],
        "source_url": "https://www.imabi.net/causative.htm"
    },
    {
        "id": 26,
        "title": "Kanji Basics - N5",
        "content": """
Introduction to Kanji (漢字):

Kanji are Chinese characters used in Japanese writing. Each kanji has:
- Meaning(s)
- Reading(s): On-yomi (Chinese reading) and Kun-yomi (Japanese reading)

Common N5 Kanji:
人 (hito/jin) - person
日 (hi/nichi) - day/sun
月 (tsuki/gatsu) - month/moon
年 (toshi/nen) - year
水 (mizu/sui) - water
火 (hi/ka) - fire
木 (ki/moku) - tree
金 (kane/kin) - money/gold
土 (tsuchi/do) - earth/ground

Learning tips:
- Start with basic kanji
- Learn radicals (components)
- Practice writing
- Use mnemonics
        """,
        "document_type": "lesson",
        "jlpt_level": "N5",
        "tags": ["kanji", "writing", "characters", "beginner"],
        "source_url": "https://www.tofugu.com/japanese/learn-kanji/"
    },
    {
        "id": 27,
        "title": "Weather Vocabulary - N5",
        "content": """
Weather-related vocabulary:

天気 (tenki) - weather
晴れ (hare) - sunny
曇り (kumori) - cloudy
雨 (ame) - rain
雪 (yuki) - snow
風 (kaze) - wind
雷 (kaminari) - thunder
霧 (kiri) - fog

Temperature:
暑い (atsui) - hot
寒い (samui) - cold
暖かい (atatakai) - warm
涼しい (suzushii) - cool

Example sentences:
- 今日は晴れです (kyou wa hare desu) - Today is sunny
- 昨日は雨でした (kinou wa ame deshita) - Yesterday it rained
- 暑いですね (atsui desu ne) - It's hot, isn't it?
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["weather", "vocabulary", "daily", "conversation"],
        "source_url": "https://www.jlptsensei.com/japanese-weather-vocabulary/"
    },
    {
        "id": 28,
        "title": "Days of the Week - N5",
        "content": """
Days of the week in Japanese:

月曜日 (getsuyoubi) - Monday
火曜日 (kayoubi) - Tuesday
水曜日 (suiyoubi) - Wednesday
木曜日 (mokuyoubi) - Thursday
金曜日 (kinyoubi) - Friday
土曜日 (doyoubi) - Saturday
日曜日 (nichiyoubi) - Sunday

Week:
今週 (konshuu) - this week
来週 (raishuu) - next week
先週 (senshuu) - last week

Usage:
- 月曜日に会いましょう (getsuyoubi ni aimashou) - Let's meet on Monday
- 今週は忙しいです (konshuu wa isogashii desu) - This week is busy
        """,
        "document_type": "vocabulary",
        "jlpt_level": "N5",
        "tags": ["time", "vocabulary", "days", "calendar"],
        "source_url": "https://www.jlptsensei.com/japanese-days-of-the-week/"
    },
    {
        "id": 29,
        "title": "Counters - N5",
        "content": """
Japanese uses counters (助数詞) for counting different objects:

本 (hon) - for long, thin objects (pencils, bottles)
- 一本 (ippon) - one
- 二本 (nihon) - two
- 三本 (sanbon) - three

枚 (mai) - for flat objects (paper, shirts)
- 一枚 (ichimai) - one
- 二枚 (nimai) - two

個 (ko) - for small objects (apples, eggs)
- 一個 (ikko) - one
- 二個 (niko) - two

人 (nin) - for people
- 一人 (hitori) - one person
- 二人 (futari) - two people
- 三人 (sannin) - three people

匹 (hiki) - for small animals
- 一匹 (ippiki) - one
- 二匹 (nihiki) - two
        """,
        "document_type": "grammar",
        "jlpt_level": "N5",
        "tags": ["counters", "grammar", "numbers", "basic"],
        "source_url": "https://guidetojapanese.org/learn/grammar/counters"
    },
    {
        "id": 30,
        "title": "Japanese Writing System Overview",
        "content": """
Japanese uses three writing systems:

1. Hiragana (ひらがな):
   - 46 basic characters
   - Used for native Japanese words
   - Used for grammatical particles and endings
   - Example: こんにちは (konnichiwa)

2. Katakana (カタカナ):
   - 46 basic characters (same sounds as Hiragana)
   - Used for foreign words and loanwords
   - Used for emphasis
   - Example: コーヒー (koohii - coffee)

3. Kanji (漢字):
   - Thousands of characters from Chinese
   - Each character has meaning and readings
   - Used for nouns, verb stems, adjectives
   - Example: 日本語 (nihongo - Japanese language)

All three systems are used together in Japanese text.
        """,
        "document_type": "lesson",
        "jlpt_level": "N5",
        "tags": ["writing", "hiragana", "katakana", "kanji", "beginner"],
        "source_url": "https://www.tofugu.com/japanese/japanese-writing-system/"
    }
]

# Combine all documents
ALL_DOCUMENTS = SAMPLE_DOCUMENTS + VOCABULARY_SETS + NEW_DOCUMENTS


