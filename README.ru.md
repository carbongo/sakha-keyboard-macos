<div align="center">

# ⌨️ Клавиатура саха для macOS

**Печатайте на саха на Mac, не теряя ни одной русской или английской буквы.**

[![Release](https://img.shields.io/github/v/release/carbongo/sakha-keyboard-macos?label=release)](https://github.com/carbongo/sakha-keyboard-macos/releases/latest)
[![CI](https://github.com/carbongo/sakha-keyboard-macos/actions/workflows/ci.yml/badge.svg)](https://github.com/carbongo/sakha-keyboard-macos/actions/workflows/ci.yml)
![macOS](https://img.shields.io/badge/macOS-12%2B-black?logo=apple)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

[English](README.md) · **Русский** · [Сахалыы](README.sah.md)

</div>

Четыре раскладки, одна установка, без перезагрузки:

| Раскладка | Основа | Где буквы саха |
|---|---|---|
| [**Sakha (Windows)**](#sakha-windows) | Русская (Mac) | Цифровой ряд, как в «Саха» для Windows |
| [**Sakha (Russian)**](#sakha-russian) | Русская (Mac) | **Opt** + похожая русская буква |
| [**Sakha (Latin)**](#sakha-latin) | US | Общетюркская латиница |
| [**Sakha (Novgorodov)**](#sakha-novgorodov) | US | Алфавит Новгородова (1920-е) |

> В macOS 27 есть своя раскладка *Yakut*, но она занимает места ц, г, ъ, ф и ж. Эти раскладки ничего не заменяют.

## 🚀 Установка

### Вариант 1: Терминал (рекомендуется, без предупреждений)

```sh
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash
```

Скрипт спросит, какие раскладки добавить в меню ввода; Return — только **Sakha (Windows)**. Переключение: **Ctrl+Пробел** или **🌐 Globe**. Выходить из системы и перезагружаться не нужно.

<details>
<summary>Параметры</summary>

```sh
# выбрать раскладки без вопросов
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash -s -- -l sakha-windows,sakha-latin

# все четыре раскладки, без вопросов
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash -s -- -l all

# удаление
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash -s -- -u
```

| Флаг | |
|---|---|
| `-l, --layouts` | `sakha-windows`, `sakha-russian`, `sakha-latin`, `sakha-novgorodov` или `all` |
| `-y, --yes` | Без вопросов; только Sakha (Windows) |
| `--no-enable` | Только установить; раскладки добавите в «Системных настройках» сами |
| `-v, --version` | Конкретный релиз, например `v2.0.0` |
| `-u, --uninstall` | Удалить всё |

</details>

### Вариант 2: Скачать и дважды щёлкнуть

> [!WARNING]
> **При первом запуске macOS заблокирует установщик.** Появится сообщение: *«Не удалось проверить, что „Install Sakha Keyboard.command“ не содержит вредоносного ПО»*. Это нормально. macOS показывает его для любого скачанного скрипта, который не нотаризован Apple, а нотаризация требует платного аккаунта разработчика. Установщик — это [`install.sh`](install.sh), его можно прочитать. Чтобы обойтись без предупреждения, используйте [вариант 1](#вариант-1-терминал-рекомендуется-без-предупреждений).

1. Скачайте **[Sakha-Keyboard.zip](https://github.com/carbongo/sakha-keyboard-macos/releases/latest/download/Sakha-Keyboard.zip)** и откройте его.
2. Дважды щёлкните **Install Sakha Keyboard.command**. Появится предупреждение, нажмите «Готово».
3. Откройте «Системные настройки» → «Конфиденциальность и безопасность», прокрутите вниз до сообщения о заблокированном файле и нажмите «Всё равно открыть». Подтвердите паролем или Touch ID.
4. Снова дважды щёлкните **Install Sakha Keyboard.command**, нажмите «Открыть» и отметьте нужные раскладки.

Удаление: **Uninstall Sakha Keyboard.command**. Это отдельный файл, поэтому для него тоже один раз нужен шаг «Всё равно открыть».

> В macOS 15 и новее правый клик → «Открыть» больше не обходит это предупреждение. Используйте «Всё равно открыть» в настройках.

<details>
<summary>Ручная установка</summary>

Скопируйте `Sakha.bundle` в `~/Library/Keyboard Layouts`. Выйдите из системы и войдите снова, затем добавьте раскладки в «Системные настройки» → «Клавиатура» → «Ввод текста» → «Изменить» → «+» (поиск: *Sakha*).

</details>

## 🗺️ Раскладки

Крупная подпись — что печатает клавиша сама по себе (с Shift — заглавная). Мелкая розовая подпись — **Opt**, а верхняя из них — **Shift+Opt**. Синие клавиши отличаются от исходной раскладки.

### Sakha (Windows)

Раскладка «Саха» из Windows (KBDYAK) на основе русской раскладки Mac. ё остаётся на своём месте, цифры — на **Opt+1…0**.

![Sakha (Windows)](docs/layouts/sakha-windows.svg)

### Sakha (Russian)

Обычная русская раскладка Mac. С **Opt** печатается похожая буква саха: г→ҕ, н→ҥ, о→ө, у→ү, х→һ, д→дь, ь→нь.

![Sakha (Russian)](docs/layouts/sakha-russian.svg)

### Sakha (Latin)

Общетюркская латиница: ҕ ğ · ҥ ñ · ө ö · ү ü · ы ı · ч ç · дь j · нь ń · й y. У букв свои клавиши, как на немецкой или турецкой клавиатуре. **Opt+буква** тоже работает (Opt+o → ö). Знаки препинания с этих клавиш переехали на Opt.

![Sakha (Latin)](docs/layouts/sakha-latin.svg)

### Sakha (Novgorodov)

Алфавит Новгородова 1920-х годов, набираемый ближайшими буквами МФА: ɯ ɣ ɟ ŋ ɲ ø и c вместо ч. Клавиши дифтонгов печатают **ie uo yø ɯa**. **Opt+гласная** печатает долгую гласную (aː), **Opt+согласная** удваивает её (tt).

![Sakha (Novgorodov)](docs/layouts/sakha-novgorodov.svg)

## ❓ Вопросы

<details>
<summary><b>Правда не нужно выходить из системы?</b></summary>

Не нужно. Установщик регистрирует раскладки через API Text Input Sources в macOS, поэтому они появляются сразу. Некоторые уже открытые программы увидят их только после перезапуска.

</details>

<details>
<summary><b>Почему macOS пишет, что «не удалось проверить» установщик? Это безопасно?</b></summary>

macOS показывает это сообщение для любого скачанного скрипта или программы, которые Apple не нотаризовала. Это не значит, что найден вирус. Нотаризация требует платного членства Apple Developer, а у этого бесплатного проекта его нет. Файлы `.command` только запускают [`install.sh`](install.sh), который копирует `Sakha.bundle` в `~/Library/Keyboard Layouts` и добавляет раскладки в меню ввода. Команда для Терминала обходится без предупреждения: файлы, полученные через `curl`, не помечаются как скачанные.

</details>

<details>
<summary><b>Cmd+C / Cmd+V будут работать?</b></summary>

Да. Сочетания с Cmd и Ctrl во всех раскладках работают по позициям US QWERTY.

</details>

<details>
<summary><b>В настройках написано «Разработчик сможет получить доступ ко всему, что вы вводите». Вы что-то собираете?</b></summary>

**Нет. Ничего не собирается, не отправляется и не хранится.**

macOS 27 показывает эту надпись для любой раскладки не от Apple, что бы в ней ни было. В этих раскладках нет кода: `Sakha.bundle` — это `Info.plist`, четыре файла `.keylayout` (обычные XML-таблицы вида «эта клавиша печатает ҕ») и четыре значка. Пока вы печатаете, ничего не работает. Установщик запускается один раз, копирует файлы и завершается. Он не остаётся в памяти, после загрузки не выходит в сеть и не собирает телеметрию.

Предупреждение рассчитано на методы ввода — настоящие программы, которые действительно видят нажатия. Apple использует ту же формулировку и для простых раскладок. Все файлы открыты в этом репозитории.

</details>

<details>
<summary><b>Что означают значки в строке меню?</b></summary>

Как у Apple **РУ** и **A**: **СА** — Sakha (Windows), **СР** — Sakha (Russian), **SA** — Sakha (Latin), **NV** — Sakha (Novgorodov). Значки в рамке macOS рисует только для своих раскладок, поэтому у нас — белые буквы. Они всегда белые, поэтому на светлой строке меню их плохо видно. Если всё ещё видны старые флаги, выйдите из системы и войдите снова: macOS обновит свой кэш.

</details>

## 🤝 Участие

Новые буквы, более удобные позиции клавиш и сообщения об ошибках — всё приветствуется. Подробности — в [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md). Раскладки генерирует [`build.py`](build.py), так что правка обычно занимает одну строку.

## Лицензия

[MIT](LICENSE). Изначально вдохновлено [@sandaar/sakha-keylayout-osx](https://github.com/sandaar/sakha-keylayout-osx).
