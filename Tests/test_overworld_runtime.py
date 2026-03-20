import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [
    str(ROOT / "Sources" / "SootCore"),
]

from sootcore.world.overworld import make_demo_overworld


class OverworldRuntimeTests(unittest.TestCase):
    def test_player_moves_on_walkable_tiles(self) -> None:
        runtime = make_demo_overworld()

        moved = runtime.move("left")

        self.assertTrue(moved)
        self.assertEqual((runtime.player.x, runtime.player.y), (6, 6))
        self.assertEqual(runtime.player.facing, "left")

    def test_player_stops_on_collision(self) -> None:
        runtime = make_demo_overworld()

        runtime.player.x = 1
        runtime.player.y = 1
        moved = runtime.move("up")

        self.assertFalse(moved)
        self.assertEqual((runtime.player.x, runtime.player.y), (1, 1))
        self.assertEqual(runtime.player.facing, "up")

    def test_player_can_walk_through_door_tile(self) -> None:
        runtime = make_demo_overworld()

        runtime.player.x = 7
        runtime.player.y = 6
        moved = runtime.move("down")

        self.assertTrue(moved)
        self.assertEqual((runtime.player.x, runtime.player.y), (7, 7))

    def test_runtime_from_manifest_supports_map_warps(self) -> None:
        from sootcore.world.overworld import runtime_from_manifest

        runtime = runtime_from_manifest(
            {
                "entry_overworld": {
                    "map_id": "room.upstairs",
                    "spawn": {"x": 1, "y": 1, "facing": "down"},
                },
                "maps": [
                    {
                        "id": "room.upstairs",
                        "location_name": "LITTLEROOT",
                        "area_subtitle": "UPSTAIRS",
                        "rows": [
                            "###",
                            "#s#",
                            "###",
                        ],
                        "warps": [
                            {"x": 1, "y": 1, "target_map_id": "room.downstairs", "target_x": 1, "target_y": 1, "target_facing": "up"},
                        ],
                    },
                    {
                        "id": "room.downstairs",
                        "location_name": "LITTLEROOT",
                        "area_subtitle": "DOWNSTAIRS",
                        "rows": [
                            "###",
                            "#.#",
                            "###",
                        ],
                    },
                ],
            }
        )

        moved = runtime.move("down")

        self.assertFalse(moved)
        runtime.player.y = 0
        moved = runtime.move("down")
        self.assertTrue(moved)
        self.assertEqual(runtime.current_map_id, "room.downstairs")
        self.assertEqual(runtime.map_data.area_subtitle, "DOWNSTAIRS")

    def test_runtime_from_manifest_supports_block_collision_maps(self) -> None:
        from sootcore.world.overworld import runtime_from_manifest

        runtime = runtime_from_manifest(
            {
                "entry_overworld": {
                    "map_id": "room.blocks",
                    "spawn": {"x": 1, "y": 1, "facing": "right"},
                },
                "maps": [
                    {
                        "id": "room.blocks",
                        "location_name": "LITTLEROOT",
                        "area_subtitle": "ROOM",
                        "width": 3,
                        "height": 3,
                        "blocks": [
                            0x0400, 0x0400, 0x0400,
                            0x0400, 0x0000, 0x0400,
                            0x0400, 0x0400, 0x0400,
                        ],
                    },
                ],
            }
        )

        self.assertFalse(runtime.move("right"))
        self.assertEqual((runtime.player.x, runtime.player.y), (1, 1))

    def test_blocked_warp_tiles_are_still_enterable(self) -> None:
        from sootcore.world.overworld import runtime_from_manifest

        runtime = runtime_from_manifest(
            {
                "entry_overworld": {
                    "map_id": "outside",
                    "spawn": {"x": 1, "y": 2, "facing": "up"},
                },
                "maps": [
                    {
                        "id": "outside",
                        "location_name": "LITTLEROOT",
                        "area_subtitle": "TOWN",
                        "width": 3,
                        "height": 3,
                        "blocks": [
                            0x0400, 0x0400, 0x0400,
                            0x0400, 0x0400, 0x0400,
                            0x0400, 0x0000, 0x0400,
                        ],
                        "warps": [
                            {"x": 1, "y": 1, "target_map_id": "inside", "target_x": 1, "target_y": 1, "target_facing": "up"},
                        ],
                    },
                    {
                        "id": "inside",
                        "location_name": "LITTLEROOT",
                        "area_subtitle": "HOUSE",
                        "width": 3,
                        "height": 3,
                        "blocks": [
                            0x0400, 0x0400, 0x0400,
                            0x0400, 0x0000, 0x0400,
                            0x0400, 0x0400, 0x0400,
                        ],
                    },
                ],
            }
        )

        self.assertTrue(runtime.move("up"))
        self.assertEqual(runtime.current_map_id, "inside")
        self.assertEqual((runtime.player.x, runtime.player.y), (1, 1))
