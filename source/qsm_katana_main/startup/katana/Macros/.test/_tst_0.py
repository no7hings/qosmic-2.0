'\n'.join(
                    [       i
                        for i in [
                            '\n'.join(
                                [
                                    "{}={}".format(
                                        str(getParam("<...variant_resolve.name>.parameters.variant.key_{}".format(i.split("_")[-1] if i != "None" else 0))),
                                        str(getParam("<...variant_resolve.name>.parameters.variant.value_{}".format(i.split("_")[-1] if i != "None" else 0)))
                                    )
                                    for i in str(getNode("<...variant_resolve.name>").parameters.keys).split(", ")
                                    if i != "None"
                                ]
                            ),
                            '\n'.join(
                                [
                                    '{}={}'.format(
                                        self.getNode().getParent().getParameter('parameters.variant_customize.{}.i0'.format(i)).getValue(0),
                                        self.getNode().getParent().getParameter('parameters.variant_customize.{}.i1'.format(i)).getValue(0),
                                    )
                                    for i in ['tag_0', 'tag_1', 'tag_2']
                                    if self.getNode().getParent().getParameter('parameters.variant_customize.{}.i0'.format(i)).getValue(0)
                                ]
                            )
                        ] if i
                    ]
                )