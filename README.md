# Goombario's Encyclopedia — Paper Mario Tattle Checker

A tool for checking progress toward the [Encyclopedia](https://retroachievements.org/achievement/79592) RA achievement in Paper Mario (N64) in detail.

### Notes

- Compatible with the Feb 21, 2026 revision of the achievement
- Save states only! `.srm` "battery save" files are not supported.
- You can create save states while RA Hardcore Mode is on; you just cannot load them in Hardcore Mode
- Confirmed working with save states from MupenPlusNext on RetroArch. Others probably work but have not been tested. If you have save states from another emulator and want to help test compatibility, feel free to open an issue with emulator details and save states attached.

---

## Web version

[Link](https://josephrooks.github.io/Goombapedia/)

Upload a RetroArch save state and see exactly which enemies you have and haven't tattled, mostly organized by the earliest chapter you can access them. No data is uploaded from your computer.

You can also save the html file locally and it _should_ work fine.

### How to use

1. In RetroArch with Paper Mario running and the save file you want to check loaded, open **Quick Menu → Save State** (or press your hotkey).
2. Find the `.stateN` file in your `states/` folder and upload it to the tool.
3. The page will show your overall progress, a chapter-by-chapter breakdown of every tracked enemy, and which ones you still need — with notes on missables and special conditions.

---

## Command line version (`src/tattle_checker.py`)

A Python proof-of-concept that does the same thing from the terminal. Requires Python 3.

Point it at any `.stateN` file from RetroArch MupenPlusNext. The `--missing-only` flag prints only the enemies you haven't tattled yet.

```bash
python3 tattle_checker.py "Paper Mario.state1"
python3 tattle_checker.py "Paper Mario.state1" --missing-only
```

---

## Credits

**Flag data** from [Paper Mario Code Notes](https://retroachievements.org/codenotes.php?g=10154) on RetroAchievements.

**Tattle lists and research** from the RetroAchievements community. The following members compiled detailed lists or contributed key information in the [achievement comments](https://retroachievements.org/achievement/79592) and the [Encyclopedia forum thread](https://retroachievements.org/forums/topic/4701):

- **Lycanroc** — [Forum post](https://retroachievements.org/forums/topic/4701?comment=133026#133026)
- **SiIverLeaf** — [Forum post](https://retroachievements.org/forums/topic/4701?comment=302175#302175) · [Tattle List (Google Sheets)](https://docs.google.com/spreadsheets/d/1OPmL7gzbdHWyk-J1AXRJtTXpU0pqxHzNAmle1tJ734g)
- **Bubbajub** — [Forum post](https://retroachievements.org/forums/topic/4701?comment=362745#362745) · [Tattle List (Google Sheets)](https://docs.google.com/spreadsheets/d/1WW-y7pxvJXqks_NMnqZ5eVbCXGx9mP3jwOI2ZMA0oOo)
- **hawkjames** — [Tattle List (Google Sheets)](https://docs.google.com/spreadsheets/d/1Ni2bjCvM0Dy0-02uZf8OmuOg6CfUtHyQznv-efYBuvk/edit?gid=0#gid=0)
- **Chows** — [Tattle List (Google Sheets)](https://docs.google.com/spreadsheets/d/1cH7ypzzxFmIhvH42v4IRMWttBjRxIxX7hm7QHvSWBdo/edit?gid=0#gid=0)