# coding:utf-8
import jinja2

jinja_loader = jinja2.FileSystemLoader('/data/e/myworkspace/td/lynxi/script/python/lxarnold/.data')

env = jinja2.Environment(loader=jinja_loader)

jinjia_template = env.get_template('dot-mtlx-template.j2')

print jinjia_template.render(
    looks={
        'default': {
            'material_assigns': {
                '/default/mesh/material_0': {
                    'material': '/default/mesh/material_0',
                    'geometries': ['/mesh_1Shape', '/mesh_2Shape']
                },
                '/default/mesh/material_1': {
                    'material': '/default/mesh/material_1',
                    'geometries': ['/mesh_1Shape', '/mesh_2Shape']
                }
            },
            'property_set_assigns': {
                '/default/mesh/property_set_0': {
                    'property_set': '/default/mesh/property_set_0',
                    'geometries': ['/mesh1Shape']
                }
            },
            'visibilities': {
                '/default/mesh/visibility_0': {
                    'type': 'camera',
                    'value': 'true',
                    'geometries': ['/mesh1Shape']
                }

            },
            'materials': {
                '/default/mesh/material_0': {
                    'shaders': {
                        '/default/shader_0': {
                            'obj_type': 'standard_surface',
                            'context': 'surfaceshader',
                            'inputs': {
                                'base': {
                                    'type': 'float',
                                    'value': '1.0'
                                }
                            },

                        }
                    },
                    'node_graphs': {
                        '/default/shader_0': {
                            'nodes': {
                                'node_0': {
                                    'obj_type': 'image',
                                    'type': 'color4',
                                    'inputs': {
                                        'base': {
                                            'type': 'float',
                                            'value': '1.0'
                                        }
                                    }
                                }
                            },
                            'outputs': {}
                        }
                    }
                }
            },
            'property_sets': {
                '/default/mesh/property_set_0': {
                    'smoothing': {
                        'type': 'boolean',
                        'value': 'true'
                    }
                }
            },
        }
    },
    option=dict(
        version=1.36,
        hyperlink='materialx/arnold/nodedefs.mtlx',
        indent=4,
        linesep='\n'
    )
)
