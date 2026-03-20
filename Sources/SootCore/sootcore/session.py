from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GameplayShellContent:
    location_name: str
    area_subtitle: str
    dialogue_speaker: str
    dialogue_text: str
    trainer_name: str
    pokedex_summary: str
    party_summary: str
    bag_summary: str
    player_summary: str
    save_summary: str
    clock_summary: str
    options_summary: str

def make_gameplay_shell_content() -> GameplayShellContent:
    return GameplayShellContent(
        location_name="LITTLEROOT",
        area_subtitle="POKECENTER",
        dialogue_speaker="MOM",
        dialogue_text="",
        trainer_name="BRENDAN",
        pokedex_summary="0/202",
        party_summary="1/6",
        bag_summary="8",
        player_summary="PLAYER BRENDAN",
        save_summary="1 FILE",
        clock_summary="PLAY TIME 00:12",
        options_summary="TINTED",
    )
