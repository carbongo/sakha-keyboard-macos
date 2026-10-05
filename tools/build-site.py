#!/usr/bin/env python3
"""Render the landing page in every language: tools/site-template.html -> site/[lang/]index.html.

Each {{key}} in the template is looked up in S (per language) or the per-page values below.
Values are trusted HTML. A key missing in any language is an error, so the pages stay in parity.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from build import VERSION  # noqa: E402

BASE = "https://sakha-kb.vercel.app"
REPO = "https://github.com/carbongo/sakha-keyboard-macos"
LANGS = {  # code: (path, switcher label, og:locale, README, CONTRIBUTING)
    "en": ("/", "EN", "en_US", "README.md", "CONTRIBUTING.md"),
    "ru": ("/ru", "RU", "ru_RU", "README.ru.md", "CONTRIBUTING.ru.md"),
    "sah": ("/sah", "САХ", "sah_RU", "README.sah.md", "CONTRIBUTING.sah.md"),
}
ZIP = f"{REPO}/releases/latest/download/Sakha-Keyboard.zip"
SH = f'<a href="{REPO}/blob/main/install.sh"><code>install.sh</code></a>'
K = lambda *keys: "+".join(f"<kbd>{k}</kbd>" for k in keys)  # noqa: E731
OPT = K("Opt")

S = {
    "title": {
        "en": "Sakha Keyboard for macOS",
        "ru": "Клавиатура саха для macOS",
        "sah": "macOS-ка саха клавиатурата",
    },
    "meta_desc": {
        "en": "Four Sakha (Yakut) keyboard layouts for macOS: Windows-style, Russian + Opt, Common Turkic Latin and Novgorodov. Nothing Russian or English is replaced. Free and open source.",
        "ru": "Четыре раскладки саха (якутского языка) для macOS: как в Windows, русская + Opt, общетюркская латиница и алфавит Новгородова. Ни одна русская или английская буква не заменена. Бесплатно и с открытым кодом.",
        "sah": "macOS-ка саха тылын түөрт раскладката: Windows курдук, нуучча + Opt, уопсай түүр латиницата уонна Новгородов алпаабыта. Нуучча да, английскай да буукуба солбуллубат. Босхо, аһаҕас кодтаах.",
    },
    "og_desc": {
        "en": "Type ҕ ҥ ө ү һ on a Mac without losing a single Russian or English letter. Four layouts, one install, no restart.",
        "ru": "Печатайте ҕ ҥ ө ү һ на Mac, не теряя ни одной русской или английской буквы. Четыре раскладки, одна установка, без перезагрузки.",
        "sah": "Mac-ка ҕ ҥ ө ү һ суруй — нууччалыы да, английскайдыы да биир да буукубаны сүтэрбэккэ. Түөрт раскладка, биир туруоруу, перезагрузката суох.",
    },
    "copy": {"en": "Copy", "ru": "Копировать", "sah": "Куопуйалаа"},
    "copied": {"en": "Copied", "ru": "Скопировано", "sah": "Куопуйаланна"},
    "copy_fail": {"en": "Select &amp; copy", "ru": "Выделите и скопируйте", "sah": "Талан баран куопуйалаа"},
    "brand": {"en": "Sakha Keyboard", "ru": "Клавиатура саха", "sah": "Саха клавиатурата"},
    "nav_layouts": {"en": "Layouts", "ru": "Раскладки", "sah": "Раскладкалар"},
    "nav_install": {"en": "Install", "ru": "Установка", "sah": "Туруоруу"},
    "nav_faq": {"en": "FAQ", "ru": "Вопросы", "sah": "Ыйытыылар"},
    "pill": {"en": "macOS 12+ · MIT · free", "ru": "macOS 12+ · MIT · бесплатно", "sah": "macOS 12+ · MIT · босхо"},
    "h1": {
        "en": 'Type in <span class="grad">Sakha</span> on&nbsp;a&nbsp;Mac.',
        "ru": 'Язык <span class="grad">саха</span> на&nbsp;вашем&nbsp;Mac.',
        "sah": 'Mac-ка <span class="grad">сахалыы</span> суруй.',
    },
    "lede": {
        "en": "Four keyboard layouts for Sakha (Yakut) — without losing a single Russian or English letter. One install, no restart.",
        "ru": "Четыре раскладки для языка саха — без потери единой русской или английской буквы. Одна установка, без перезагрузки.",
        "sah": "Саха тылыгар түөрт раскладка — нууччалыы да, английскайдыы да биир да буукубаны сүтэрбэккэ. Биир туруоруу, перезагрузката суох.",
    },
    "btn_install": {"en": "Install", "ru": "Установить", "sah": "Туруор"},
    "btn_zip": {"en": "Download .zip", "ru": "Скачать .zip", "sah": ".zip хачайдаа"},
    "hint_switch": {
        "en": f"Then switch with {K('Ctrl')} {K('Space')} or {K('🌐')}. No logout needed.",
        "ru": f"Переключение: {K('Ctrl')} {K('Пробел')} или {K('🌐')}. Выходить из системы не нужно.",
        "sah": f"Раскладканы {K('Ctrl')} {K('Space')} эбэтэр {K('🌐')} көмөтүнэн уларыт. Систематтан тахсар наадата суох.",
    },
    "why_eyebrow": {"en": "Why this one", "ru": "Почему эти", "sah": "Тоҕо бу"},
    "why_h2": {
        "en": "Sakha letters, added — not swapped in.",
        "ru": "Буквы саха добавлены, а не подменены.",
        "sah": "Саха буукубалара эбиллэллэр — туох да солбуллубат.",
    },
    "why_sub": {
        "en": "macOS 27 ships its own <i>Yakut</i> layout, which replaces ц, г, ъ, ф and ж. These layouts never move a Russian or English letter.",
        "ru": "В macOS 27 есть своя раскладка <i>Yakut</i>, но она занимает места ц, г, ъ, ф и ж. Эти раскладки не трогают ни одной русской или английской буквы.",
        "sah": "macOS 27-гэ бэйэтин <i>Yakut</i> раскладката баар, ол эрээри кини ц, г, ъ, ф уонна ж оннуларын ылар. Бу раскладкалар туох да буукубаны солбуйбаттар.",
    },
    "f1_h": {"en": "Nothing replaced", "ru": "Ничего не заменено", "sah": "Туох да солбуллубат"},
    "f1_p": {
        "en": f"Sakha letters live on the number row, spare keys or {OPT}. Every Russian and English letter stays where your fingers expect it.",
        "ru": f"Буквы саха — на цифровом ряду, свободных клавишах или {OPT}. Все русские и английские буквы остаются на привычных местах.",
        "sah": f"Саха буукубалара цифра кэккэтигэр, босхо клавишаларга эбэтэр {OPT}-ка тураллар. Нуучча уонна английскай буукубалар бары үөрэммит миэстэлэригэр хаалаллар.",
    },
    "f2_h": {"en": "No restart", "ru": "Без перезагрузки", "sah": "Перезагрузката суох"},
    "f2_p": {
        "en": "The installer registers the layouts through macOS's Text Input Sources API, so they show up instantly.",
        "ru": "Установщик регистрирует раскладки через API Text Input Sources в macOS, поэтому они появляются сразу.",
        "sah": "Туруорааччы раскладкалары macOS Text Input Sources API нөҥүө бэлиэтиир, онон кинилэр тута көстөллөр.",
    },
    "f3_h": {"en": "Shortcuts untouched", "ru": "Сочетания не меняются", "sah": "Холбоһуктар уларыйбаттар"},
    "f3_p": {
        "en": f"{K('⌘C')}, {K('⌘V')} and every {K('Ctrl')} shortcut use US QWERTY positions in every layout.",
        "ru": f"{K('⌘C')}, {K('⌘V')} и все сочетания с {K('Ctrl')} во всех раскладках работают по позициям US QWERTY.",
        "sah": f"{K('⌘C')}, {K('⌘V')} уонна {K('Ctrl')} бары холбоһуктара бары раскладкаларга US QWERTY миэстэлэринэн үлэлииллэр.",
    },
    "f4_h": {"en": "No code, nothing collected", "ru": "Ни кода, ни сбора данных", "sah": "Код суох, туох да хомуллубат"},
    "f4_p": {
        "en": "The bundle is plain XML key tables and four icons. Nothing runs while you type — no telemetry, no network.",
        "ru": "Внутри — только XML-таблицы клавиш и четыре значка. Пока вы печатаете, ничего не работает: ни телеметрии, ни сети.",
        "sah": "Иһигэр клавиша XML-таблицалара уонна түөрт значок эрэ баар. Эн бэчээттиир кэмҥэр туох да үлэлээбэт — телеметрия да, ситим да суох.",
    },
    "f5_h": {"en": "Four alphabets", "ru": "Четыре алфавита", "sah": "Түөрт алпаабыт"},
    "f5_p": {
        "en": f"Windows-style Cyrillic, Russian with {OPT}, Common Turkic Latin and the 1920s Novgorodov script.",
        "ru": f"Кириллица как в Windows, русская с {OPT}, общетюркская латиница и алфавит Новгородова 1920-х.",
        "sah": f"Windows курдук кириллица, {OPT}-тах нуучча, уопсай түүр латиницата уонна 1920-с сыллардааҕы Новгородов алпаабыта.",
    },
    "f6_h": {"en": "Open and readable", "ru": "Открыто и понятно", "sah": "Аһаҕас уонна өйдөнүмтүө"},
    "f6_p": {
        "en": "Every layout is generated by one Python script. Changing a key is usually a single line.",
        "ru": "Все раскладки генерирует один скрипт на Python. Изменить клавишу — обычно одна строка.",
        "sah": "Раскладкалары барыларын биир Python скрипт оҥорор. Клавишаны уларытыы үксүгэр биир строка.",
    },
    "lay_eyebrow": {"en": "Layouts", "ru": "Раскладки", "sah": "Раскладкалар"},
    "lay_h2": {"en": "Pick the one that fits your hands.", "ru": "Выберите удобную.", "sah": "Илиигэр табыгастааҕы тал."},
    "lay_sub": {
        "en": "Install any or all four, and switch between them from the input menu.",
        "ru": "Установите любую или все четыре и переключайтесь между ними в меню ввода.",
        "sah": "Биири эбэтэр түөртүөнү барытын туруор, киирии менютугар уларыт.",
    },
    "tab_russian": {"en": "Russian + Opt", "ru": "Русская + Opt", "sah": "Нуучча + Opt"},
    "tab_latin": {"en": "Latin", "ru": "Латиница", "sah": "Латиница"},
    "tab_novgorodov": {"en": "Novgorodov", "ru": "Новгородов", "sah": "Новгородов"},
    "base_ru": {"en": "built on Mac Russian", "ru": "основа: русская (Mac)", "sah": "Mac нуучча раскладкатыгар"},
    "base_us": {"en": "built on US", "ru": "основа: US", "sah": "US раскладкатыгар"},
    "badge": {"en": "badge", "ru": "значок", "sah": "значок"},
    "diagram": {"en": "Keyboard diagram", "ru": "Схема раскладки", "sah": "Раскладка схемата"},
    "win_p1": {
        "en": f"The Windows Sakha layout (KBDYAK), on Mac Russian. Sakha letters sit on the number row, just like on Windows. ё stays on its key, and digits move to {OPT}+{K('1')}…{K('0')}.",
        "ru": f"Раскладка «Саха» из Windows (KBDYAK) на основе русской раскладки Mac. Буквы саха — на цифровом ряду, как в Windows. ё остаётся на своём месте, цифры — на {OPT}+{K('1')}…{K('0')}.",
        "sah": f"Windows саха раскладката (KBDYAK), Mac нуучча раскладкатыгар. Саха буукубалара цифра кэккэтигэр, Windows курдук. ё бэйэтин клавишатыгар хаалар, цифралар — {OPT}+{K('1')}…{K('0')}.",
    },
    "win_p2": {
        "en": "The default — pick this if you already type Sakha on Windows.",
        "ru": "Раскладка по умолчанию — для тех, кто уже печатает на саха в Windows.",
        "sah": "Бастакы талыы — Windows-ка сахалыы суруйар буоллаххына, маны тал.",
    },
    "rus_p": {
        "en": f"Plain Mac Russian. Hold {OPT} for the Sakha letter that looks like it.",
        "ru": f"Обычная русская раскладка Mac. С {OPT} печатается похожая буква саха.",
        "sah": f"Судургу Mac нуучча раскладката. {OPT} тутан туран маарынныыр саха буукубатын бэчээттиигин.",
    },
    "lat_p": {
        "en": f"Common Turkic Latin. The letters have their own keys, as on German or Turkish keyboards; {OPT}+letter works too ({OPT}+{K('o')} → ö).",
        "ru": f"Общетюркская латиница. У букв свои клавиши, как на немецкой или турецкой клавиатуре; {OPT}+буква тоже работает ({OPT}+{K('o')} → ö).",
        "sah": f"Уопсай түүр латиницата. Буукубалар бэйэлэрин клавишалаахтар, немецкэй эбэтэр турецкай клавиатураларга курдук; {OPT}+буукуба эмиэ үлэлиир ({OPT}+{K('o')} → ö).",
    },
    "nov_p": {
        "en": f"The 1920s Novgorodov alphabet, typed with the closest IPA letters. Diphthong keys type <b>ie uo yø ɯa</b>; {OPT}+vowel makes it long (aː), {OPT}+consonant doubles it (tt).",
        "ru": f"Алфавит Новгородова 1920-х годов, набираемый ближайшими буквами МФА. Клавиши дифтонгов печатают <b>ie uo yø ɯa</b>; {OPT}+гласная — долгая гласная (aː), {OPT}+согласная удваивает её (tt).",
        "sah": f"1920-с сыллардааҕы Новгородов алпаабыта, чугас IPA буукубаларынан. Дифтонг клавишалара <b>ie uo yø ɯa</b> бэчээттииллэр; {OPT}+аһаҕас дорҕоон уһун аһаҕаһы бэчээттиир (aː), {OPT}+бүтэй дорҕоон кинини хатылыыр (tt).",
    },
    "legend_diff": {"en": "differs from the base layout", "ru": "отличается от исходной раскладки", "sah": "төрүт раскладкаттан атын"},
    "legend_opt": {
        "en": f"small legend = {OPT} (upper: {K('Shift')}+{OPT})",
        "ru": f"мелкая подпись = {OPT} (верхняя: {K('Shift')}+{OPT})",
        "sah": f"кыра бэлиэ = {OPT} (үөһээ: {K('Shift')}+{OPT})",
    },
    "ins_h2": {"en": "Ready in under a minute.", "ru": "Готово меньше чем за минуту.", "sah": "Биир мүнүүтэ иһигэр бэлэм."},
    "ins_sub": {
        "en": "Both ways install the same files to <code>~/Library/Keyboard Layouts</code>.",
        "ru": "Оба способа ставят одни и те же файлы в <code>~/Library/Keyboard Layouts</code>.",
        "sah": "Икки ньыма тэҥ файллары <code>~/Library/Keyboard Layouts</code> иһигэр туруораллар.",
    },
    "term_h": {"en": "Terminal", "ru": "Терминал", "sah": "Терминал"},
    "recommended": {"en": "recommended", "ru": "рекомендуется", "sah": "сүбэлэнэр"},
    "term_p": {
        "en": f"No security warning. It asks which layouts to add — press {K('Return')} for Sakha (Windows).",
        "ru": f"Без предупреждений. Скрипт спросит, какие раскладки добавить; {K('Return')} — только Sakha (Windows).",
        "sah": f"Сэрэтиитэ суох. Скрипт ханнык раскладкалары эбэри ыйытыа; {K('Return')} баттаатаххына, Sakha (Windows) эрэ эбиллиэ.",
    },
    "flag_all": {"en": "All four layouts, no questions", "ru": "Все четыре раскладки, без вопросов", "sah": "Түөрт раскладка барыта, ыйытыыта суох"},
    "flag_y": {"en": "Don't ask; add Sakha (Windows) only", "ru": "Без вопросов; только Sakha (Windows)", "sah": "Ыйыппат; Sakha (Windows) эрэ эбэр"},
    "flag_v": {"en": "A specific release", "ru": "Конкретный релиз", "sah": "Анал релиз"},
    "flag_u": {"en": "Uninstall everything", "ru": "Удалить всё", "sah": "Барытын сотор"},
    "flags_how": {"en": "Pass flags like this:", "ru": "Флаги передаются так:", "sah": "Флагтары маннык биэр:"},
    "dl_h": {"en": "Download and double-click", "ru": "Скачать и дважды щёлкнуть", "sah": "Хачайдаан баран иккитэ баттаа"},
    "dl_1": {
        "en": f'Download <a href="{ZIP}"><b>Sakha-Keyboard.zip</b></a> and open it.',
        "ru": f'Скачайте <a href="{ZIP}"><b>Sakha-Keyboard.zip</b></a> и откройте его.',
        "sah": f'<a href="{ZIP}"><b>Sakha-Keyboard.zip</b></a> хачайдаа уонна ас.',
    },
    "dl_2": {
        "en": "Double-click <b>Install Sakha Keyboard.command</b>. macOS warns you — click <b>Done</b>.",
        "ru": "Дважды щёлкните <b>Install Sakha Keyboard.command</b>. Появится предупреждение — нажмите <b>Готово</b>.",
        "sah": "<b>Install Sakha Keyboard.command</b> иккитэ баттаа. Сэрэтии тахсыа, <b>Готово</b> баттаа.",
    },
    "dl_3": {
        "en": "Open <b>System Settings → Privacy &amp; Security</b>, find the blocked installer and click <b>Open Anyway</b>.",
        "ru": "Откройте <b>Системные настройки → Конфиденциальность и безопасность</b>, найдите заблокированный установщик и нажмите <b>Всё равно открыть</b>.",
        "sah": "<b>Системные настройки → Конфиденциальность и безопасность</b> ас, бобуллубут туруорааччыны бул уонна <b>Всё равно открыть</b> баттаа.",
    },
    "dl_4": {
        "en": "Double-click the installer again, click <b>Open</b>, and tick the layouts you want.",
        "ru": "Снова дважды щёлкните установщик, нажмите <b>Открыть</b> и отметьте нужные раскладки.",
        "sah": "Туруорааччыны өссө иккитэ баттаа, <b>Открыть</b> баттаа уонна наадалаах раскладкаларгын бэлиэтээ.",
    },
    "dl_note": {
        "en": f"<b>Why the warning?</b> macOS flags any downloaded script that isn't notarised, which needs a paid Apple Developer account. The installer is just {SH} — read it first if you like.",
        "ru": f"<b>Почему предупреждение?</b> macOS помечает любой скачанный скрипт без нотаризации, а она требует платного аккаунта разработчика Apple. Установщик — это просто {SH}, его можно прочитать.",
        "sah": f"<b>Тоҕо сэрэтии тахсар?</b> macOS нотаризацията суох хачайдаммыт ханнык баҕарар скрипкэ итини көрдөрөр, оттон нотаризацияҕа төлөбүрдээх разработчик аккаунта наада. Туруорааччы — {SH} эрэ, кинини ааҕыахха сөп.",
    },
    "dl_remove": {
        "en": "To remove, run <b>Uninstall Sakha Keyboard.command</b> from the same zip.",
        "ru": "Удаление: <b>Uninstall Sakha Keyboard.command</b> из того же архива.",
        "sah": "Сотуу: ол архивтан <b>Uninstall Sakha Keyboard.command</b>.",
    },
    "faq_h2": {"en": "Questions, answered.", "ru": "Ответы на вопросы.", "sah": "Ыйытыыларга хоруйдар."},
    "q1": {
        "en": "Do I really not need to log out?",
        "ru": "Правда не нужно выходить из системы?",
        "sah": "Систематтан тахсар наадата чахчы суох дуо?",
    },
    "a1": {
        "en": "No. The installer registers the bundle through macOS's Text Input Sources API, so the layouts appear immediately. Apps that were already open may pick them up only after a relaunch.",
        "ru": "Не нужно. Установщик регистрирует раскладки через API Text Input Sources в macOS, поэтому они появляются сразу. Некоторые уже открытые программы увидят их только после перезапуска.",
        "sah": "Суох. Туруорааччы бандылы macOS Text Input Sources API нөҥүө бэлиэтиир, онон раскладкалар тута көстөллөр. Урут аһыллыбыт сорох программалар кинилэри саҥаттан холбонно эрэ көрүөхтэрин сөп.",
    },
    "q2": {
        "en": "Why does macOS say it “could not verify” the installer? Is it safe?",
        "ru": "Почему macOS пишет, что «не удалось проверить» установщик? Это безопасно?",
        "sah": "Тоҕо macOS туруорааччыны «бэрэбиэркэлээбэтим» диир? Куттала суох дуо?",
    },
    "a2": {
        "en": "macOS shows that for every downloaded script or app Apple hasn't notarised — it doesn't mean malware was found. The <code>.command</code> files only run <code>install.sh</code>, which copies <code>Sakha.bundle</code> to <code>~/Library/Keyboard Layouts</code> and adds the layouts to your input menu. The Terminal one-liner shows no warning, because files fetched with <code>curl</code> aren't flagged as downloads.",
        "ru": "macOS показывает это сообщение для любого скачанного скрипта или программы, которые Apple не нотаризовала. Это не значит, что найден вирус. Файлы <code>.command</code> только запускают <code>install.sh</code>, который копирует <code>Sakha.bundle</code> в <code>~/Library/Keyboard Layouts</code> и добавляет раскладки в меню ввода. Команда для Терминала обходится без предупреждения: файлы, полученные через <code>curl</code>, не помечаются как скачанные.",
        "sah": "macOS бу суругу Apple нотаризациялаабатах хачайдаммыт хас биирдии скрипкэ эбэтэр программаҕа көрдөрөр. Ол вирус булулунна диэн буолбатах. <code>.command</code> файллар <code>install.sh</code> эрэ холбууллар, кини <code>Sakha.bundle</code>-ы <code>~/Library/Keyboard Layouts</code> иһигэр куопуйалыыр уонна раскладкалары киирии менютугар эбэр. Терминал командата сэрэтиитэ суох, тоҕо диэтэххэ <code>curl</code> нөҥүө ылыллыбыт файллар хачайдаммыт курдук бэлиэтэммэттэр.",
    },
    "q3": {"en": "Will ⌘C / ⌘V still work?", "ru": "⌘C / ⌘V будут работать?", "sah": "⌘C / ⌘V үлэлиэ дуо?"},
    "a3": {
        "en": "Yes. Cmd and Ctrl shortcuts always use the US QWERTY positions in every layout.",
        "ru": "Да. Сочетания с Cmd и Ctrl во всех раскладках работают по позициям US QWERTY.",
        "sah": "Үлэлиир. Cmd уонна Ctrl холбоһуктара бары раскладкаларга куруутун US QWERTY миэстэлэринэн үлэлииллэр.",
    },
    "q4": {
        "en": "System Settings says “The developer can access anything you type”. Do you collect anything?",
        "ru": "В настройках написано «Разработчик сможет получить доступ ко всему, что вы вводите». Вы что-то собираете?",
        "sah": "Настройкаларга «Разработчик сможет получить доступ ко всему, что вы вводите» диэн суруллубут. Тугу эмэ хомуйаҕын дуо?",
    },
    "a4": {
        "en": "<b>No. Nothing is collected, sent or stored.</b> macOS 27 shows that label on every keyboard layout that doesn't come from Apple. These layouts contain no code: an <code>Info.plist</code>, four <code>.keylayout</code> XML tables and four icons. The installer runs once, copies the files and exits — no background process, no telemetry.",
        "ru": "<b>Нет. Ничего не собирается, не отправляется и не хранится.</b> macOS 27 показывает эту надпись для любой раскладки не от Apple. В этих раскладках нет кода: <code>Info.plist</code>, четыре XML-таблицы <code>.keylayout</code> и четыре значка. Установщик запускается один раз, копирует файлы и завершается — без фоновых процессов и телеметрии.",
        "sah": "<b>Суох. Туох да хомуллубат, ыытыллыбат, харайыллыбат.</b> macOS 27 бу суругу Apple оҥорботох ханнык баҕарар раскладкаҕа көрдөрөр. Бу раскладкаларга код суох: <code>Info.plist</code>, түөрт <code>.keylayout</code> XML-таблица уонна түөрт значок. Туруорааччы биирдэ холбонор, файллары куопуйалыыр уонна бүтэр. Кини үлэлии хаалбат уонна телеметрия хомуйбат.",
    },
    "q5": {
        "en": "What do the menu bar badges mean?",
        "ru": "Что означают значки в строке меню?",
        "sah": "Меню строкатыгар значоктар тугу бэлиэтииллэрий?",
    },
    "a5": {
        "en": "Like Apple's <b>РУ</b> and <b>A</b>: <b>СА</b> is Sakha (Windows), <b>СР</b> Sakha (Russian), <b>SA</b> Sakha (Latin) and <b>NV</b> Sakha (Novgorodov). They're plain white letters, so they're hard to see on a light menu bar. If you still see old flag icons, log out and back in once.",
        "ru": "Как у Apple <b>РУ</b> и <b>A</b>: <b>СА</b> — Sakha (Windows), <b>СР</b> — Sakha (Russian), <b>SA</b> — Sakha (Latin), <b>NV</b> — Sakha (Novgorodov). Это белые буквы, поэтому на светлой строке меню их плохо видно. Если всё ещё видны старые флаги, выйдите из системы и войдите снова.",
        "sah": "Apple <b>РУ</b> уонна <b>A</b> курдук: <b>СА</b> — Sakha (Windows), <b>СР</b> — Sakha (Russian), <b>SA</b> — Sakha (Latin), <b>NV</b> — Sakha (Novgorodov). Кинилэр маҥан буукубалар, онон сырдык меню строкатыгар көстөр уустук. Эргэ былаахтар көстө тураллар буоллаҕына, систематтан тахсан баран төттөрү киир.",
    },
    "band_h2": {"en": "Help shape the keyboard.", "ru": "Помогите сделать клавиатуру лучше.", "sah": "Клавиатураны тупсарарга көмөлөс."},
    "band_p": {
        "en": "New letters, better key positions and bug reports are all welcome. The layouts are generated by <code>build.py</code>, so a change is usually a single line.",
        "ru": "Новые буквы, более удобные позиции клавиш и сообщения об ошибках — всё приветствуется. Раскладки генерирует <code>build.py</code>, так что правка обычно занимает одну строку.",
        "sah": "Саҥа буукубалар, ордук табыгастаах миэстэлэр уонна алҕас туһунан суруктар — барыта үөрүүнү кытта ылыллар. Раскладкалары <code>build.py</code> оҥорор, онон уларытыы үксүгэр биир строка.",
    },
    "btn_contribute": {"en": "Contribute", "ru": "Участвовать", "sah": "Кыттыы"},
    "btn_issue": {"en": "Report an issue", "ru": "Сообщить об ошибке", "sah": "Алҕас туһунан суруй"},
    "changelog": {"en": "Changelog", "ru": "Изменения", "sah": "Уларыйыылар"},
    "releases": {"en": "Releases", "ru": "Релизы", "sah": "Релиздэр"},
    "inspired": {"en": "inspired by", "ru": "вдохновлено", "sah": "бастакы санаата:"},
}


def page(lang):
    path, _, locale, readme, contributing = LANGS[lang]
    switcher = "".join(
        f'<a href="{p}" hreflang="{code}" lang="{code}"' + (' aria-current="page"' if code == lang else "") + f">{label}</a>"
        for code, (p, label, *_) in LANGS.items()
    )
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{BASE}{p}">' for code, (p, *_) in LANGS.items()
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    values = {
        "lang": lang, "url": BASE + path, "og_locale": locale, "alternates": alternates,
        "switcher": switcher, "version": VERSION, "zip": ZIP, "readme": readme,
        "contributing": contributing,
        "curl": "curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash",
    }
    values.update({k: v[lang] for k, v in S.items()})

    def sub(m):
        if m.group(1) not in values:
            sys.exit(f"build-site: no value for {{{{{m.group(1)}}}}} ({lang})")
        return values[m.group(1)]

    return re.sub(r"\{\{(\w+)\}\}", sub, (ROOT / "tools/site-template.html").read_text())


def main():
    for k, v in S.items():
        if set(v) != set(LANGS):
            sys.exit(f"build-site: {k} is missing {set(LANGS) - set(v)}")
    for lang, (path, *_) in LANGS.items():
        out = ROOT / "site" / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang))
    print(f"built site v{VERSION}: {', '.join(LANGS)}")


if __name__ == "__main__":
    main()
