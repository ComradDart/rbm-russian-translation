# RBM — Русский перевод / Realistic Battle Mod Russian Translation

Полный русский перевод для **Realistic Battle Mod (RBM)** для
Mount & Blade II: Bannerlord, сделанный с нуля.

## Что переведено

- **Названия предметов:** луки, арбалеты, стрелы и болты, метательное оружие,
  копья, щиты, доспехи, кузнечные детали, а также юниты и снаряжение нордской фракции.
- **Подсказки** и блок «Статистика RBM» в описании предметов (сила натяжения,
  скорость снаряда, зоны брони и т.д.).
- **Боевые сообщения и ИИ:** стойка/выносливость, пробой стойки, тактические приказы.
- **Настройки в MCM.**

## Возможности

- **534 строки**, все файлы проходят проверку XML.
- Все игровые токены (переменные `{DMG}` и условные конструкции) сохранены — проверено автоматически.
- **Грамматическое согласование модификаторов** по роду и числу (Легендарн**ый** лук /
  Легендарн**ые** стрелы), как в ванильной локализации.
- Исправлена ванильная опечатка модификатора «Надломленный».

## Установка

1. Скопируйте папку `RBM_Russian_Translation` в `...\Modules\`
   (или установите zip через Vortex).
2. Включите модуль и **загрузите его ПОСЛЕ** модуля RBM.
3. Язык игры — Русский.

## Известные ограничения

Небольшая часть предметов RBM (*Repeating Crossbow, Imperial Cheirosiphon,
Poisoned Repeater Bolts* и др.) и три опции в MCM (*Sneak Attack Insta-Kill,
Slow Motion in Combat, Stamina System*) заданы в коде мода **без идентификаторов
локализации**, поэтому технически не переводятся языковым файлом. Всё остальное на русском.

## Требования / совместимость

Realistic Battle Mod (v4.3.x). Перевод не содержит кода и не меняет баланс.
Совместим с переводом Open Source Armory.

## Структура репозитория

```
RBM_Russian_Translation/   — готовый модуль (SubModule.xml + ModuleData/Languages/RU/LOC-rus.xml)
tools/                     — скрипты сборки и грамматической разметки
```

## Пересборка перевода (tools/)

- `tools/tagger.py` — определяет главное существительное и его род/число, ставит грамматическую разметку.
- `tools/build_rbm.py` — собирает `LOC-rus.xml` из английской базы RBM, применяет
  разметку к названиям предметов, добавляет строки предметов, у которых в RBM нет
  идентификатора в LOC-eng, и правит ванильную опечатку.
- `tools/rbm_translations.json` — перевод строк из LOC-eng RBM.
- `tools/rbm_extra_items.json` — предметы RBM с `{=id}`, отсутствующие в LOC-eng RBM.

Пути к источникам (staging Vortex / установка игры) заданы в начале скриптов и
настроены под окружение автора — при необходимости поправьте их.

## Благодарности

Авторам **Realistic Battle Mod** за оригинальный мод. Этот репозиторий содержит
только русские языковые файлы для RBM и не содержит ассетов или кода мода. См. `NOTICE`.

## Лицензия

Оригинальные материалы (скрипты и строки перевода) — под лицензией **MIT** (см. `LICENSE`).
Переведённые строки являются производными от RBM; см. `NOTICE`.

---

### English (short)

Complete, from-scratch Russian translation for **Realistic Battle Mod**: item names
(bows, crossbows, arrows, shields, armor, throwables, Nord-faction units and gear),
tooltips ("RBM Stats"), combat/AI text, and MCM options. 534 strings, grammatical
gender/number agreement for item modifiers, all `{TOKEN}` placeholders preserved.
Load **after** RBM. Text-only, no DLL. A few RBM items and three MCM options are
hardcoded in the mod's DLL without localization ids and therefore cannot be translated
by a language file. Tooling in `tools/`; see `NOTICE` and `LICENSE` (MIT).
