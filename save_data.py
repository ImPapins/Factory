from dataclasses import dataclass
import json
from pathlib import Path


SAVE_DIR = Path("saves")
SAVE_SLOT_COUNT = 3


@dataclass(frozen=True)
class SaveSlot:
    index: int
    name: str
    path: Path

    @property
    def exists(self):
        return self.path.exists()


def create_default_save(slot: SaveSlot):
    SAVE_DIR.mkdir(exist_ok=True)

    data = {
        "slot": slot.index,
        "name": slot.name,
        "factory": {
            "money": 0,
            "machines": [],
            "items": {},
        },
    }

    slot.path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_save(slot: SaveSlot):
    ensure_save(slot)
    return json.loads(slot.path.read_text(encoding="utf-8"))


def save_game(slot: SaveSlot, data):
    SAVE_DIR.mkdir(exist_ok=True)
    slot.path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def delete_save(slot: SaveSlot):
    if slot.exists:
        slot.path.unlink()


def ensure_save(slot: SaveSlot):
    if not slot.exists:
        create_default_save(slot)


def get_save_slots():
    return [
        SaveSlot(
            index=slot_index,
            name=f"Save Slot {slot_index}",
            path=SAVE_DIR / f"slot_{slot_index}.json"
        )
        for slot_index in range(1, SAVE_SLOT_COUNT + 1)
    ]
