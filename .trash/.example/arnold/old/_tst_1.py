# coding:utf-8
import lxarnold.startup as and_startup

and_startup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019').set_run()

f1 = '/l/temp/jerry/bifrost/my_grass.ass'

f2 = '/l/temp/jerry/bifrost/my_grass_1.ass'

import arnold as ai

from arnold import ai_dotass

ai.AiBegin()
universe = ai.AiUniverse()
ai_dotass._AiASSLoad(universe, filename=f1, mask=ai.AI_NODE_ALL)
ai_dotass._AiASSWrite(universe, filename=f2, mask=ai.AI_NODE_ALL, binary=False)
ai.AiEnd()
