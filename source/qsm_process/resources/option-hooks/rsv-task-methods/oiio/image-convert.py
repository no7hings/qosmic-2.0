# coding:utf-8


def main(session):
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    hook_option_opt = session.option_opt

    image_file_path = hook_option_opt.get('image_file')
    output_image_path = hook_option_opt.get('output_image_file')

    if bsc_storage.StgFileOpt(
        image_file_path
    ).get_is_file() is True:
        bsc_storage.ImgOiioOptForThumbnail(image_file_path).convert_to(
            output_image_path
        )
    else:
        raise RuntimeError(
            bsc_log.Log.trace_method_error(
                'file="{}" is non-exists'.format(image_file_path)
            )
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
