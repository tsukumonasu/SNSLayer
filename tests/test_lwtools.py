import json
from unittest import TestCase
from lwtools.lwtools import post_lw_user, push_lw_calendar, post_lw_room, post_lw_payload, get_lw_headers, \
    create_room_with_bot


class Test(TestCase):

    def setUp(self):
        with open('lineworks.json', 'r') as f:
            self.secret_dic = json.load(f)
        with open('env.json', 'r') as f:
            self.env = json.load(f)
        self.lw_header = get_lw_headers(self.secret_dic)

    def test_post_lw_room(self):
        expected = post_lw_room(self.secret_dic, self.lw_header, self.env['BotId'], 'ルームに対して送信のテストです1',
                                self.env['RoomId'])
        self.assertEqual(expected, 200)

        expected = post_lw_room(self.secret_dic, self.lw_header, self.env['BotId'], 'ルームに対して送信のテストです2',
                                self.env['RoomId'])
        self.assertEqual(expected, 200)

    def test_post_lw_user(self):
        expected = post_lw_user(self.secret_dic, self.lw_header, self.env['BotId'], 'ユーザに対して送信のテストです',
                                self.env['AccountId'])
        self.assertEqual(expected, 200)

    def test_post_lw_payload(self):
        payload = {
            "accountId": self.env['AccountId'],
            "content": {
                "type": "button_template",
                "contentText": "What do you want?",
                "actions": [{
                    "type": "uri",
                    "label": "WorksMobile Homepage",
                    "uri": "https://line.worksmobile.com"
                }, {
                    "type": "message",
                    "label": "FAQ",
                    "postback": "ButtonTemplate_FAQ"
                }]
            }
        }
        expected = post_lw_payload(self.secret_dic, self.lw_header, self.env['BotId'], payload)
        self.assertEqual(expected, 200)

    def test_push_lw_calendar(self):
        ical = 'BEGIN:VCALENDAR\n' \
               'VERSION:2.0\n' \
               'CALSCALE:GREGORIAN\n' \
               'BEGIN:VTIMEZONE\n' \
               'TZID:Asia/Tokyo\n' \
               'BEGIN:STANDARD\n' \
               'DTSTART:19700101T000000\n' \
               'TZNAME:GMT+09:00\n' \
               'TZOFFSETFROM:+0900\n' \
               'TZOFFSETTO:+0900\n' \
               'END:STANDARD\n' \
               'END:VTIMEZONE\n' \
               'BEGIN:VEVENT\n' \
               'SEQUENCE:0\n' \
               'CLASS:PUBLIC\n' \
               'TRANSP:OPAQUE\n' \
               'DTSTART;VALUE=DATE:20211025\n' \
               'DTEND;VALUE=DATE:20211026\n' \
               'SUMMARY:サンプル予定\n' \
               'DTSTAMP:20211026T015409Z\n' \
               'END:VEVENT\n' \
               'END:VCALENDAR\n'
        expected = push_lw_calendar(self.secret_dic, self.lw_header, self.env['AccountId'], 'defaultCalendarId', ical)
        self.assertEqual(expected, 200)

    def test_create_room_with_bot(self):
        expected = create_room_with_bot(self.secret_dic, self.lw_header, self.env['BotId'], 'hoge_room',
                                        [self.env['AccountId'], self.env['AccountId2']], 'トークルームを作成いたしました！')
        self.assertEqual(expected, 200)
