from common import TestMetaWearBase
from ctypes import c_float, create_string_buffer
from mbientlab.metawear.sensor import ProximityTsl2671

class TestProximityTsl2671Config(TestMetaWearBase):
    def setUp(self):
        self.boardType= TestMetaWearBase.METAWEAR_DETECT_BOARD

        super().setUp()

    def test_receiver_channel(self):
        tests= [
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0x90],
                'channel': ProximityTsl2671.CHANNEL_0,
                'channel_name': '0'
            },
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0xa0],
                'channel': ProximityTsl2671.CHANNEL_1,
                'channel_name': '1'
            },
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0xb0],
                'channel': ProximityTsl2671.CHANNEL_BOTH,
                'channel_name': 'both'
            }
        ]

        for test in tests:
            with self.subTest(channel= test['channel_name']):
                self.libmetawear.mbl_mw_proximity_tsl2671_set_receiver_channel(self.board, test['channel'])
                self.libmetawear.mbl_mw_proximity_tsl2671_write_config(self.board)
                self.assertEqual(self.command, test['expected'])

    def test_transmitter_current(self):
        tests= [
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0xe0],
                'current': ProximityTsl2671.CURRENT_12_5MA,
                'current_name': '12.5mA'
            },
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0xa0],
                'current': ProximityTsl2671.CURRENT_25MA,
                'current_name': '25mA'
            },
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0x60],
                'current': ProximityTsl2671.CURRENT_50MA,
                'current_name': '50mA'
            },
            {
                'expected': [0x18, 0x02, 0xff, 0x01, 0x20],
                'current': ProximityTsl2671.CURRENT_100MA,
                'current_name': '100mA'
            }
        ]

        for test in tests:
            with self.subTest(channel= test['current_name']):
                self.libmetawear.mbl_mw_proximity_tsl2671_set_transmitter_current(self.board, test['current'])
                self.libmetawear.mbl_mw_proximity_tsl2671_write_config(self.board)
                self.assertEqual(self.command, test['expected'])

    def test_integration_time(self):
        tests= [
            {
                'expected': [0x18, 0x02, 0xfe, 0x01, 0xa0],
                'integration_time': c_float(5.44),
                'time': '5.44ms'
            },
            {
                'expected': [0x18, 0x02, 0x01, 0x01, 0xa0],
                'integration_time': c_float(693.6),
                'time': '693.6ms'
            }
        ]

        for test in tests:
            with self.subTest(channel= test['time']):
                self.libmetawear.mbl_mw_proximity_tsl2671_set_integration_time(self.board, test['integration_time'])
                self.libmetawear.mbl_mw_proximity_tsl2671_write_config(self.board)
                self.assertEqual(self.command, test['expected'])


    def test_n_pulses(self):
        expected= [0x18, 0x02, 0xff, 0x20, 0xa0]

        self.libmetawear.mbl_mw_proximity_tsl2671_set_n_pulses(self.board, 32)
        self.libmetawear.mbl_mw_proximity_tsl2671_write_config(self.board)
        self.assertEqual(self.command, expected)

class TestProximityTsl2671Data(TestMetaWearBase):
    def setUp(self):
        self.boardType= TestMetaWearBase.METAWEAR_DETECT_BOARD

        super().setUp()

    def test_read_adc(self):
        expected= [0x18, 0x81]

        self.libmetawear.mbl_mw_proximity_tsl2671_read_adc(self.board)
        self.assertEqual(self.command, expected)

    def test_proximity_data(self):
        expected= 1522
        response= create_string_buffer(b'\x18\x81\xf2\x05', 4)

        signal= self.libmetawear.mbl_mw_proximity_tsl2671_get_adc_data_signal(self.board)
        self.libmetawear.mbl_mw_datasignal_subscribe(signal, self.sensor_data_handler)
        self.libmetawear.mbl_mw_connection_notify_char_changed(self.board, response.raw, len(response.raw))

        self.assertEqual(self.data_uint32.value, expected)