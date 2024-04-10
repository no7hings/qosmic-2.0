# coding:utf-8
import lxbasic.log as bsc_log


class MsgBaseMtd(object):
    class ArkServer(object):
        Url = 'http://cg-ark.papegames.com'
        Port = 61112

    class MessageServer(object):
        AutherUrl = 'https://paas.diezhi.net/o/user-center/api/login/adagent/user_auth/'
        MailUrl = (
            'https://pops-tianmen.diezhi.net/api/noc/v1/alert/pro?'
            'type=emailx&tpl=dzdh-dev&index={sender}&bind=form-data&email={addresses}'
        )
        FeishuUrl = (
            'https://pops-tianmen.diezhi.net/api/noc/v1/alert/pro?'
            'type=fsappx&tpl=dzdh-dev&index={sender}&bind=form-data&at={receivers}'
        )

    class Verifier(object):
        Login = 'ple'
        Password = 'abcd1234,'

    FIX = {
        'fangxiaodong': 'xiaoche',
        'huangxin': 'mofei'
    }

    @classmethod
    def get_session(cls):
        import requests

        session = requests.Session()
        session.verify = False
        session.post(
            cls.MessageServer.AutherUrl,
            data=dict(
                user_name=cls.Verifier.Login,
                password=cls.Verifier.Password,
                bk_login=False
            ),
            verify=False,
            allow_redirects=False
        )
        return session

    # new api
    # noinspection PyUnusedLocal
    @classmethod
    def send_mail_(cls, sender='ple', addresses=None, subject=None, content=None, attachments=None):
        url = cls.MessageServer.MailUrl.format(
            sender=sender,
            addresses=','.join(addresses or [])
        )
        message_data = {'hi_title': subject, 'message': content}
        session = cls.get_session()
        response = session.post(url, data=message_data, files=None)
        result = response.json()
        bsc_log.Log.trace_method_result(
            'send mail',
            'result is "{}"'.format(result.get('message') or 'fail')
        )
        return result

    # noinspection PyUnusedLocal
    @classmethod
    def send_feishu_(cls, sender='shotgun', receivers=None, subject=None, content=None, attachments=None):
        def to_receives_fnc_(receivers_):
            if receivers_:
                for _seq, _i in enumerate(receivers_):
                    if _i in cls.FIX:
                        receivers_[_seq] = cls.FIX[_i]
                return ','.join(receivers_)
            else:
                raise RuntimeError()

        #
        url = cls.MessageServer.FeishuUrl.format(
            sender=sender,
            receivers=to_receives_fnc_(receivers)
        )
        message_data = {'hi_title': subject, 'message': content}
        session = cls.get_session()
        response = session.post(url, data=message_data, files=None)
        result = response.json()
        bsc_log.Log.trace_method_result(
            'send mail',
            'result is "{}"'.format(result.get('message') or 'fail')
        )
        return result

    @classmethod
    def send_chat_(cls, sender, receivers, subject, content):
        pass
