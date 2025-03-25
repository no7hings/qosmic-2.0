# coding:utf-8
import lnx_scene.stage.model as m


stage = m.StageRoot.new_from_json(
'''
{
    "nodes": {
        "/root/premiere/xml/main": {
            "type": "PremiereXml",
            "attrs": {
                "videos": {
                    "value": {
                        "data": [
                            "X:/QSM_TST/A001/A001_001/\u52a8\u753b/\u901a\u8fc7\u6587\u4ef6/A001_001_002.mov",
                            "X:/QSM_TST/A001/A001_001/\u52a8\u753b/\u901a\u8fc7\u6587\u4ef6/A001_001_001.mov",
                            "X:/QSM_TST/A001/A001_001/\u52a8\u753b/\u901a\u8fc7\u6587\u4ef6/A001_001_003.mov"
                        ],
                        "type": "StringArray"
                    }
                }
            }
        },
        "/root/maya/scene/A001_001_001": {
            "type": "MaysScene",
            "attrs": {
                "references": {
                    "value": {
                        "data": [
                            "X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma"
                        ],
                        "type": "StringArray"
                    }
                }
            }
        },
        "/root/maya/scene/A001_001_003": {
            "type": "MaysScene",
            "attrs": {
                "references": {
                    "value": {
                        "data": [
                            "X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma"
                        ],
                        "type": "StringArray"
                    }
                }
            }
        }
    }
}
'''
)

other_stage = m.StageRoot.new_from_json(
'''
{
    "nodes": {
        "/root/maya/scene/A001_001_001": {
            "type": "MaysScene",
            "attrs": {
                "references": {
                    "value": {
                        "data": [
                            "X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma"
                        ],
                        "type": "StringArray"
                    }
                },
                "reference_replace_map": {
                    "value": {
                        "data": {},
                        "type": "Dict"
                    }
                }
            }
        },
        "/root/maya/scene/A001_001_002": {
            "type": "MaysScene",
            "attrs": {
                "references": {
                    "value": {
                        "data": [
                            "X:/QSM_TST/Assets/chr/lily/Rig/Final/scenes/lily_Skin.ma",
                            "X:/QSM_TST/A001/A001_001/\u52a8\u753b/\u901a\u8fc7\u6587\u4ef6/A001_001_001.ma"
                        ],
                        "type": "StringArray"
                    }
                }
            }
        }
    }
}
'''
)

stage.update(other_stage)
print(stage)

# print(stage.get_nodes())

# print(stage.find_nodes('/root/maya/scene//*{attr("type")=="MaysScene"}'))

