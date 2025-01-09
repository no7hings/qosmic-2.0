# coding:utf-8
import parse

r = parse.parse(
    '{root.storage.path}/prod/{project.storage.name}/{stage.storage.name}/assets/{role.storage.name}/{asset.storage.name}/{extra}', '/l/prod/cg7/work/assets/chr/dad/mod/modeling/maya'
)


if r:
    result = r.named
    for k, v in result.items():
        print '{} = {}'.format(k, v)


print "{test-test}".format(**{'test-test': "A"})

