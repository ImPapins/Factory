from dataclasses import dataclass
import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SAVE_DIR = BASE_DIR / "saves"
SAVE_SLOT_COUNT = 3


@dataclass(frozen=True)
class SaveSlot:
    index: int
    name: str
    path: Path

    @property
    def exists(self):
        return self.path.exists()


def _write_json_atomic(path: Path, data):
    SAVE_DIR.mkdir(exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(tmp_path, path)


def create_default_save(slot: SaveSlot):
    data = {
        "slot": slot.index,
        "name": slot.name,
        "factory": {
            "money": 0,
            "machines": [],
            "items": {},
        },
    }

    _write_json_atomic(slot.path, data)


def load_save(slot: SaveSlot):
    ensure_save(slot)
    return json.loads(slot.path.read_text(encoding="utf-8"))


def save_game(slot: SaveSlot, data):
    _write_json_atomic(slot.path, data)


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
