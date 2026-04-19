#!/usr/bin/env python3
"""
Paper Mario (N64) - Goombario Tattle Checker
Reads from a RetroArch Mupen64Plus GLES3 save state file (.stateN).

Usage:
  python3 tattle_checker_state.py "Paper Mario.state1"
  python3 tattle_checker_state.py "Paper Mario.state1" --missing-only

Your save state is in RetroArch's states/ directory.
Save one in-game: Quick Menu -> Save State (or your hotkey).
"""

import sys
import zlib
import struct
import argparse

# RDRAM base offset within the decompressed Mupen64Plus-Next GLES3 save state.
# Found empirically: RDRAM starts at decompressed offset 0x1CC.
# RA tattle addresses map directly: tattle_byte = rdram[ra_address]
RDRAM_BASE = 0x1CC

# RA code note addresses for tattle flags (eldexter)
# These are direct RDRAM offsets (RA addressing = RDRAM offset)
TATTLE_FLAGS = [
    # Tattle Flags 1 (0xdbedc)
    (0xdbedc, 0, "Bill Blaster"),
    (0xdbedc, 1, "Cleft"),
    (0xdbedc, 2, "Monty Mole"),
    (0xdbedc, 3, "Bandit"),
    (0xdbedc, 4, "Pokey"),
    (0xdbedc, 5, "Pokey Mummy"),
    (0xdbedc, 6, "Swooper"),
    (0xdbedc, 7, "Buzzy Beetle"),
    # Tattle Flags 2 (0xdbedd)
    (0xdbedd, 0, "Paragoomba"),
    (0xdbedd, 1, "Spiked Goomba"),
    (0xdbedd, 2, "Fuzzy"),
    (0xdbedd, 3, "Koopa Troopa"),
    (0xdbedd, 4, "Paratroopa"),
    (0xdbedd, 5, "Bob-omb"),
    (0xdbedd, 7, "Bullet Bill"),
    # Tattle Flags 3 (0xdbede)
    (0xdbede, 2, "Gloomba"),
    (0xdbede, 3, "Paragloomba"),
    (0xdbede, 4, "Spiked Gloomba"),
    (0xdbede, 5, "Dark Koopa"),
    (0xdbede, 7, "Goomba"),
    # Tattle Flags 4 (0xdbee0)
    (0xdbee0, 0, "Monty Mole (Green)"),
    (0xdbee0, 1, "Bzzap!"),
    (0xdbee0, 2, "Crazee Dayzee"),
    (0xdbee0, 3, "Amazy Dayzee"),
    (0xdbee0, 4, "Ruff Puff"),
    (0xdbee0, 5, "Spike"),
    (0xdbee0, 6, "Gulpit"),
    # Tattle Flags 5 (0xdbee1)
    (0xdbee1, 1, "Jungle Fuzzy"),
    (0xdbee1, 2, "Spear Guy"),
    (0xdbee1, 3, "Lava Bubble"),
    (0xdbee1, 4, "Spike Top"),
    (0xdbee1, 5, "Putrid Piranha"),
    (0xdbee1, 6, "Lakitu"),
    (0xdbee1, 7, "Spiny"),
    # Tattle Flags 6 (0xdbee2)
    (0xdbee2, 0, "Groove Guy"),
    (0xdbee2, 1, "Sky Guy"),
    (0xdbee2, 2, "Medi Guy"),
    (0xdbee2, 3, "Pyro Guy"),
    (0xdbee2, 4, "Spy Guy"),
    (0xdbee2, 6, "Hurt Plant"),
    (0xdbee2, 7, "M. Bush"),
    # Tattle Flags 7 (0xdbee3)
    (0xdbee3, 0, "Stone Chomp"),
    (0xdbee3, 1, "Piranha Plant"),
    (0xdbee3, 2, "Forest Fuzzy"),
    (0xdbee3, 3, "Hyper Goomba"),
    (0xdbee3, 4, "Hyper Paragoomba"),
    (0xdbee3, 5, "Hyper Cleft"),
    (0xdbee3, 6, "Clubba"),
    (0xdbee3, 7, "Shy Guy"),
    # Tattle Flags 8 (0xdbee4)
    (0xdbee4, 0, "Magikoopa (Bowser's Castle)"),
    (0xdbee4, 2, "Red Magikoopa"),
    (0xdbee4, 3, "Green Magikoopa"),
    (0xdbee4, 5, "Yellow Magikoopa"),
    (0xdbee4, 7, "Gray Magikoopa"),
    # Tattle Flags 9 (0xdbee5)
    (0xdbee5, 1, "Bombshell Bill Blaster"),
    (0xdbee5, 2, "Bombshell Bill"),
    (0xdbee5, 3, "Hammer Bros."),
    (0xdbee5, 4, "Koopatrol"),
    # Tattle Flags 10 (0xdbee6)
    (0xdbee6, 5, "Ember"),
    (0xdbee6, 6, "Bony Beetle"),
    (0xdbee6, 7, "Dry Bones"),
    # Tattle Flags 11 (0xdbee7)
    (0xdbee7, 0, "White Clubba"),
    (0xdbee7, 1, "Frost Piranha"),
    (0xdbee7, 2, "Swoopula"),
    (0xdbee7, 3, "Duplighost"),
    # Tattle Flags 12 (0xdbeeb)
    (0xdbeeb, 2, "White Magikoopa"),
    # Tattle Flags 13 (0xdbeec)
    (0xdbeec, 0, "Blue Goomba"),
    (0xdbeec, 1, "Red Goomba"),
    (0xdbeec, 2, "Goomba King"),
    # Tattle Flags 14 (0xdbeed)
    (0xdbeed, 1, "Jr. Troopa (2)"),
    (0xdbeed, 2, "Jr. Troopa (3)"),
    (0xdbeed, 3, "Jr. Troopa (4)"),
    (0xdbeed, 4, "Jr. Troopa (5)"),
    (0xdbeed, 5, "Jr. Troopa (6)"),
    # Tattle Flags 15 (0xdbeef)
    (0xdbeef, 2, "The Master (1)"),
    (0xdbeef, 3, "The Master (2)"),
    (0xdbeef, 4, "The Master (3)"),
    (0xdbeef, 5, "Chan"),
    (0xdbeef, 6, "Lee"),
    # Tattle Flags 16 (0xdbef0)
    (0xdbef0, 1, "Big Lantern Ghost"),
    (0xdbef0, 3, "Lava Piranha (Phase 1)"),
    (0xdbef0, 4, "Lava Piranha (Phase 2)"),
    (0xdbef0, 5, "Lava Bud (Phase 1)"),
    (0xdbef0, 6, "Lava Bud (Phase 2)"),
    (0xdbef0, 7, "Petit Piranha"),
    # Tattle Flags 17 (0xdbef1)
    (0xdbef1, 0, "Shy Squad"),
    (0xdbef1, 2, "General Guy"),
    (0xdbef1, 7, "Anti Guy"),
    # Tattle Flags 18 (0xdbef2)
    (0xdbef2, 0, "Buzzar"),
    (0xdbef2, 1, "Tutankoopa"),
    (0xdbef2, 2, "Chain Chomp (Tutankoopa)"),
    (0xdbef2, 3, "Tubba Blubba (Windmill)"),
    (0xdbef2, 5, "Tubba's Heart"),
    (0xdbef2, 6, "Stilt Guy"),
    (0xdbef2, 7, "Shy Stack"),
    # Tattle Flags 19 (0xdbef3)
    (0xdbef3, 1, "Bowser (Ch. 1 fake)"),
    (0xdbef3, 3, "Green Ninjakoopa"),
    (0xdbef3, 4, "Red Ninjakoopa"),
    (0xdbef3, 5, "Blue Ninjakoopa"),
    (0xdbef3, 6, "Yellow Ninjakoopa"),
    # Tattle Flags 20 (0xdbef5)
    (0xdbef5, 0, "Electro Blooper"),
    (0xdbef5, 2, "Super Blooper"),
    (0xdbef5, 4, "Blooper Baby"),
    # Tattle Flags 21 (0xdbef6)
    (0xdbef6, 1, "Bowser (Ch. 3 fake)"),
    (0xdbef6, 3, "Bowser (Final)"),
    (0xdbef6, 7, "Blooper"),
    # Tattle Flags 22 (0xdbef7)
    (0xdbef7, 1, "Kent C. Koopa"),
    (0xdbef7, 2, "Huff N. Puff"),
    (0xdbef7, 3, "Tuff Puff"),
    (0xdbef7, 4, "Monstar"),
    (0xdbef7, 5, "Crystal King"),
    (0xdbef7, 7, "Crystal Bit"),
]

CHAPTERS = [
    ("Tattle Flags 1  (0xdbedc)", ["Bill Blaster","Cleft","Monty Mole","Bandit","Pokey","Pokey Mummy","Swooper","Buzzy Beetle"]),
    ("Tattle Flags 2  (0xdbedd)", ["Paragoomba","Spiked Goomba","Fuzzy","Koopa Troopa","Paratroopa","Bob-omb","Bullet Bill"]),
    ("Tattle Flags 3  (0xdbede)", ["Gloomba","Paragloomba","Spiked Gloomba","Dark Koopa","Goomba"]),
    ("Tattle Flags 4  (0xdbee0)", ["Monty Mole (Green)","Bzzap!","Crazee Dayzee","Amazy Dayzee","Ruff Puff","Spike","Gulpit"]),
    ("Tattle Flags 5  (0xdbee1)", ["Jungle Fuzzy","Spear Guy","Lava Bubble","Spike Top","Putrid Piranha","Lakitu","Spiny"]),
    ("Tattle Flags 6  (0xdbee2)", ["Groove Guy","Sky Guy","Medi Guy","Pyro Guy","Spy Guy","Hurt Plant","M. Bush"]),
    ("Tattle Flags 7  (0xdbee3)", ["Stone Chomp","Piranha Plant","Forest Fuzzy","Hyper Goomba","Hyper Paragoomba","Hyper Cleft","Clubba","Shy Guy"]),
    ("Tattle Flags 8  (0xdbee4)", ["Magikoopa (Bowser's Castle)","Red Magikoopa","Green Magikoopa","Yellow Magikoopa","Gray Magikoopa"]),
    ("Tattle Flags 9  (0xdbee5)", ["Bombshell Bill Blaster","Bombshell Bill","Hammer Bros.","Koopatrol"]),
    ("Tattle Flags 10 (0xdbee6)", ["Ember","Bony Beetle","Dry Bones"]),
    ("Tattle Flags 11 (0xdbee7)", ["White Clubba","Frost Piranha","Swoopula","Duplighost"]),
    ("Tattle Flags 12 (0xdbeeb)", ["White Magikoopa"]),
    ("Tattle Flags 13 (0xdbeec)", ["Blue Goomba","Red Goomba","Goomba King"]),
    ("Tattle Flags 14 (0xdbeed)", ["Jr. Troopa (2)","Jr. Troopa (3)","Jr. Troopa (4)","Jr. Troopa (5)","Jr. Troopa (6)"]),
    ("Tattle Flags 15 (0xdbeef)", ["The Master (1)","The Master (2)","The Master (3)","Chan","Lee"]),
    ("Tattle Flags 16 (0xdbef0)", ["Big Lantern Ghost","Lava Piranha (Phase 1)","Lava Piranha (Phase 2)","Lava Bud (Phase 1)","Lava Bud (Phase 2)","Petit Piranha"]),
    ("Tattle Flags 17 (0xdbef1)", ["Shy Squad","General Guy","Anti Guy"]),
    ("Tattle Flags 18 (0xdbef2)", ["Buzzar","Tutankoopa","Chain Chomp (Tutankoopa)","Tubba Blubba (Windmill)","Tubba's Heart","Stilt Guy","Shy Stack"]),
    ("Tattle Flags 19 (0xdbef3)", ["Bowser (Ch. 1 fake)","Green Ninjakoopa","Red Ninjakoopa","Blue Ninjakoopa","Yellow Ninjakoopa"]),
    ("Tattle Flags 20 (0xdbef5)", ["Electro Blooper","Super Blooper","Blooper Baby"]),
    ("Tattle Flags 21 (0xdbef6)", ["Bowser (Ch. 3 fake)","Bowser (Final)","Blooper"]),
    ("Tattle Flags 22 (0xdbef7)", ["Kent C. Koopa","Huff N. Puff","Tuff Puff","Monstar","Crystal King","Crystal Bit"]),
]


def decompress_state(path: str) -> bytes:
    with open(path, 'rb') as f:
        data = f.read()

    if not data.startswith(b'#RZIPv'):
        raise ValueError("Not a RetroArch RZIP save state. Expected #RZIPv header.")

    pos = 0x14  # skip 8-byte magic + 4-byte chunk_size + 4-byte unknown
    chunks = []
    while pos < len(data) - 4:
        comp_len = struct.unpack_from('<I', data, pos)[0]
        if comp_len == 0 or comp_len > 0x200000:
            break
        pos += 4
        if pos + comp_len > len(data):
            break
        try:
            chunks.append(zlib.decompress(data[pos:pos+comp_len]))
        except zlib.error:
            break
        pos += comp_len

    if not chunks:
        raise ValueError("Could not decompress save state.")
    return b''.join(chunks)


def read_rdram_byte(full: bytes, ra_addr: int) -> int:
    offset = RDRAM_BASE + ra_addr
    if offset >= len(full):
        raise ValueError(f"State too small to read RA address 0x{ra_addr:x}")
    return full[offset]


def check_tattles(full: bytes) -> dict:
    return {
        name: bool(read_rdram_byte(full, addr) & (1 << bit))
        for addr, bit, name in TATTLE_FLAGS
    }


def print_report(results: dict, missing_only: bool = False):
    tattled = sum(1 for v in results.values() if v)
    missing_names = sorted(k for k, v in results.items() if not v)
    total = len(TATTLE_FLAGS)

    print(f"\n{'='*60}")
    print(f"  GOOMBARIO TATTLE REPORT")
    print(f"{'='*60}")
    print(f"  Tattled:  {tattled} / {total}")
    print(f"  Missing:  {len(missing_names)}")
    print(f"{'='*60}\n")

    for chapter, names in CHAPTERS:
        ch_missing = [n for n in names if not results.get(n)]
        ch_tattled = [n for n in names if results.get(n)]

        if missing_only and not ch_missing:
            continue

        print(f"  [{chapter}]")
        for name in names:
            if missing_only:
                if not results.get(name):
                    print(f"    ✗ {name}")
            else:
                print(f"    {'✓' if results.get(name) else '✗'} {name}")
        if not missing_only:
            print(f"    → {len(ch_tattled)}/{len(names)}")
        print()

    if missing_names:
        print(f"{'='*60}")
        print(f"  STILL MISSING ({len(missing_names)}):")
        print(f"{'='*60}")
        for name in missing_names:
            print(f"    ✗ {name}")


def main():
    parser = argparse.ArgumentParser(
        description="Check Goombario tattle progress from a RetroArch Mupen64Plus GLES3 save state"
    )
    parser.add_argument('state', help='Path to your .stateN file')
    parser.add_argument('--missing-only', action='store_true',
                        help='Only show enemies not yet tattled')
    args = parser.parse_args()

    try:
        full = decompress_state(args.state)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Quick sanity check
    area = read_rdram_byte(full, 0x740a8)
    stars = read_rdram_byte(full, 0x779cb)
    hp = read_rdram_byte(full, 0x10f291)
    print(f"[State info: area=0x{area:02x}, stars={stars}, Mario HP={hp}]")

    results = check_tattles(full)
    print_report(results, missing_only=args.missing_only)


if __name__ == '__main__':
    main()
