# arnold node abstract

## basic
- Scene
    - Universe
        - Category
            - Type
            - ...
        - ...
        - ObjCategory
            - ObjType
            - ...
        - ...
        - Node
            - Input
                - Channel
                - ...
                - Element
                    - Channel
                    - ...
             - ...
            - Output
                - Channel
                - ...
        - ...
        - Connection
        - ...

## graphic

```mermaid
graph TD

scene["Scene"]

universe["Universe"]

category["Category"]

type["Type"]

node_category["ObjCategory"]

node_type["ObjType"]

node["Node"]

connection["Connection"]

scene --- universe

universe --- category
category --- type

universe --- node_category
node_category --- node_type

universe --- node
universe --- connection
```