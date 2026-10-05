<div align="center">

# ⌨️ Клавиатура саха для macOS

**Печатайте на саха на Mac, не теряя ни одной русской или английской буквы.**

[![Release](https://img.shields.io/github/v/release/carbongo/sakha-keyboard-macos?label=release)](https://github.com/carbongo/sakha-keyboard-macos/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

[English](README.md) · **Русский**

</div>

Четыре раскладки, одна установка, без перезагрузки:

| Раскладка | Основа | Где буквы саха |
|---|---|---|
| **Sakha (Russian)** | Русская (Mac) | Цифровой ряд, как в «Саха» для Windows |
| **Russian (Sakha)** | Русская (Mac) | **Opt** + похожая русская буква |
| **Sakha (Latin)** | US | Общетюркская латиница |
| **Sakha (Novgorodov)** | US | Алфавит Новгородова (1920-е) |

> В macOS 27 есть своя раскладка *Yakut*, но она занимает места ц, г, ъ, ф и ж. Эти раскладки ничего не заменяют.

## 🚀 Установка

### Вариант 1: Терминал

```sh
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash
```

Скрипт спросит, какие раскладки добавить. Переключение: **Ctrl+Пробел** или **🌐 Globe**. Выходить из системы не нужно.

Удаление: `… | bash -s -- -u`. Все параметры: `… | bash -s -- -h`.

### Вариант 2: Скачать и дважды щёлкнуть

1. Скачайте **[Sakha-Keyboard.zip](https://github.com/carbongo/sakha-keyboard-macos/releases/latest/download/Sakha-Keyboard.zip)** и откройте его.
2. Дважды щёлкните **Install Sakha Keyboard.command** и отметьте нужные раскладки.

> **«Не удалось проверить разработчика»?** Нажмите «Готово», откройте «Системные настройки» → «Конфиденциальность и безопасность», нажмите «Всё равно открыть» и запустите установщик снова.

## 🗺️ Раскладки

Крупная подпись — что печатает клавиша сама по себе (с Shift — заглавная). Мелкая розовая подпись — **Opt**, а верхняя из них — **Shift+Opt**. Синие клавиши отличаются от исходной раскладки.

### Sakha (Russian)
![Sakha (Russian)](docs/layouts/sakha-russian.svg)

### Russian (Sakha)
Opt+г ҕ · Opt+н ҥ · Opt+о ө · Opt+у ү · Opt+х һ · Opt+д дь · Opt+ь нь

![Russian (Sakha)](docs/layouts/russian-sakha.svg)

### Sakha (Latin)
ҕ ğ · ҥ ñ · ө ö · ү ü · ы ı · ч ç · дь j · нь ń · й y

![Sakha (Latin)](docs/layouts/sakha-latin.svg)

### Sakha (Novgorodov)
**Opt+гласная** печатает долгую гласную (aː), **Opt+согласная** удваивает её (tt).

![Sakha (Novgorodov)](docs/layouts/sakha-novgorodov.svg)

## 🤝 Участие

Предложения и ошибки присылайте в [Issues](https://github.com/carbongo/sakha-keyboard-macos/issues). Подробности — в [CONTRIBUTING.md](CONTRIBUTING.md).
