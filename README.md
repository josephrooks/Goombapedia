# Goombario's Encyclopedia — Paper Mario Tattle Checker

Tools for tracking Goombario tattle progress toward the [Encyclopedia](https://retroachievements.org/achievement/XXXXX) RetroAchievements achievement in Paper Mario (N64). Compatible with the Feb 21, 2026 revision of the achievement.

---

## Web version

A browser-based tool. Upload a RetroArch save state and see exactly which enemies you have and haven't tattled, mostly organized by the earliest chapter you can access them. No data is uploaded anywhere.

### How to use

1. In RetroArch with Paper Mario running and the save file you want to check loaded, open **Quick Menu → Save State** (or press your hotkey).
2. Find the `.stateN` file in your `states/` folder and upload it to the tool.
3. Works with MupenPlusNext on RetroArch. Other emulators may work but have not been tested. Save states only — `.srm` files are not supported.

---

## Command line version (`src/tattle_checker.py`)

A Python proof-of-concept that does the same thing from the terminal. Requires Python 3.

```bash
python3 src/tattle_checker.py "Paper Mario.state1"
python3 src/tattle_checker.py "Paper Mario.state1" --missing-only
```

Point it at any `.stateN` file from RetroArch MupenPlusNext. The `--missing-only` flag prints only the enemies you haven't tattled yet.

---

## Credits

**Flag data** from [Paper Mario Code Notes](https://retroachievements.org/codenotes.php?g=10154) on RetroAchievements.

**Tattle lists** compiled by RetroAchievements community members whose detailed work made this tool accurate:

- **Lycanroc** — [Forum post](https://retroachievements.org/forums/topic/4701?comment=133026#133026)
- **SiIverLeaf** — [Forum post](https://retroachievements.org/forums/topic/4701?comment=302175#302175) · [Tattle List (Google Sheets)](https://docs.google.com/spreadsheets/d/1OPmL7gzbdHWyk-J1AXRJtTXpU0pqxHzNAmle1tJ734g)
- **Bubbajub** — [Forum post](https://retroachievements.org/forums/topic/4701?comment=362745#362745) · [Tattle List (Google Sheets)](https://docs.google.com/spreadsheets/d/1WW-y7pxvJXqks_NMnqZ5eVbCXGx9mP3jwOI2ZMA0oOo)