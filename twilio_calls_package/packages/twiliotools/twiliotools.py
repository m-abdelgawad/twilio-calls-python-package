import logging
from twilio.rest import Client


# Import logger
logging.getLogger('twilio.http_client').setLevel(level=logging.WARN)
logging.getLogger('urllib3.connectionpool').setLevel(level=logging.WARN)


class TwilioTools:
    def __init__(self, account_sid, auth_token):
        self.twilio_client = Client(account_sid, auth_token)

    def call(self, from_num, to_num, msg):
        twiml_msg = "<Response><Say>{0}</Say></Response>".format(msg)
        call = self.twilio_client.calls.create(
            twiml=twiml_msg,
            to=to_num,
            from_=from_num
        )

        return call.sid

    def _fetch_call(self, sid):
        return self.twilio_client.calls(sid).fetch()

    def get_call_status(self, sid):
        call = self._fetch_call(sid=sid)
        return call.status

    def get_call_logs(self, sid):
        call = self._fetch_call(sid=sid)
        return {
            'sid': call.sid,
            'from': call.from_,
            'from_formatted': call.from_formatted,
            'to': call.to,
            'to_formatted': call.to_formatted,
            'price': call.price,
            'price_unit': call.price_unit,
            'duration': call.duration,
            'date_created': call.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'date_updated': call.date_updated.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': call.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'direction': call.direction,
            'status': call.status,
            'queue_time': call.queue_time,
            'forwarded_from': call.forwarded_from,
        }
