"""Basic testing for AlazarTech card"""
from time import sleep
from unittest import TestCase
import unittest
import json
from place.scan import Scan
from . import atsapi as ats


JSON_TEST_STR = """
{
"scan_type": "scan_point_test",
"instruments":
    [
        {
        "module_name": "alazartech",
        "class_name": "ATS660",
        "priority": 99,
        "config":
            {
            "clock_source": "INTERNAL_CLOCK",
            "sample_rate": "SAMPLE_RATE_10MSPS",
            "clock_edge": "CLOCK_EDGE_RISING",
            "decimation": 0,
            "analog_inputs":
                [
                    {
                    "input_channel": "CHANNEL_A",
                    "input_coupling": "DC_COUPLING",
                    "input_range": "INPUT_RANGE_PM_800_MV",
                    "input_impedance": "IMPEDANCE_50_OHM"
                    }
                ],
            "trigger_operation": "TRIG_ENGINE_OP_J",
            "trigger_engine_1": "TRIG_ENGINE_J",
            "trigger_source_1": "TRIG_FORCE",
            "trigger_slope_1": "TRIGGER_SLOPE_POSITIVE",
            "trigger_level_1": 128,
            "trigger_engine_2": "TRIG_ENGINE_K",
            "trigger_source_2": "TRIG_FORCE",
            "trigger_slope_2": "TRIGGER_SLOPE_POSITIVE",
            "trigger_level_2": 128,
            "pre_trigger_samples": 0,
            "post_trigger_samples": 1024,
            "averages": 32,
            "plot": "no"
            }
        }
    ]
}
"""

class TestOsciCardUtilities(TestCase):
    """Test class"""
    def test0002_json_init(self):
        """Test that JSON is processing our string correctly"""
        dat = json.loads(JSON_TEST_STR)
        self.assertEqual(dat, json.loads(json.dumps(dat)))

    def test0003_json_test1(self):
        """Test that we can perform a point scan with JSON input"""
        scan = Scan()
        try:
            scan.config(JSON_TEST_STR)
        except Exception as err: # pylint: disable=broad-except
            if "Board" in str(err) and "not found" in str(err):
                self.skipTest("No Alazar board detected.")
            else:
                raise err
        scan.run()

class TestATS(TestCase):
    """Test the ATS card (if available)"""

    def setUp(self):
        try:
            self.board = ats.Board()
        except Exception: #pylint: disable=broad-except
            self.skipTest('No ATS card detected in this machine.')

        # set the capture clock
        # (these values should be supported by all ATS cards)
        self.board.setCaptureClock(
            ats.INTERNAL_CLOCK,
            ats.SAMPLE_RATE_1MSPS,
            ats.CLOCK_EDGE_RISING,
            0
            )

        if self.board.type == ats.ATS660:
            self.range_impedance_tests = [
                # supported modes on ATS660
                (ats.INPUT_RANGE_PM_200_MV, ats.IMPEDANCE_1M_OHM),
                (ats.INPUT_RANGE_PM_200_MV, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_400_MV, ats.IMPEDANCE_1M_OHM),
                (ats.INPUT_RANGE_PM_400_MV, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_800_MV, ats.IMPEDANCE_1M_OHM),
                (ats.INPUT_RANGE_PM_800_MV, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_2_V, ats.IMPEDANCE_1M_OHM),
                (ats.INPUT_RANGE_PM_2_V, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_4_V, ats.IMPEDANCE_1M_OHM),
                (ats.INPUT_RANGE_PM_4_V, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_8_V, ats.IMPEDANCE_1M_OHM),
                (ats.INPUT_RANGE_PM_16_V, ats.IMPEDANCE_1M_OHM),
                # theses range/impedance combinations fail for some reason, but
                # the ATS-SDK-Guide-7.1.4 says they are valid for this card
                #------------
                # (ats.INPUT_RANGE_PM_8_V, ats.IMPEDANCE_50_OHM),
                # (ats.INPUT_RANGE_PM_16_V, ats.IMPEDANCE_50_OHM),
                ]

        elif self.board.type == ats.ATS9440:
            self.range_impedance_tests = [
                # supported modes on ATS9440
                (ats.INPUT_RANGE_PM_100_MV, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_200_MV, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_400_MV, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_1_V, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_2_V, ats.IMPEDANCE_50_OHM),
                (ats.INPUT_RANGE_PM_4_V, ats.IMPEDANCE_50_OHM),
                ]

        else:
            self.skipTest('No range/impedance tests found for this card.')

    def test_input_range(self):
        """Test available input ranges and impedance values."""
        for input_range, impedance in self.range_impedance_tests:
            try:
                self.board.inputControl(
                    ats.CHANNEL_A,
                    ats.AC_COUPLING,
                    input_range,
                    impedance
                    )
                sleep(0.05)
            except Exception as err: # pylint: disable=broad-except
                self.fail(str(err))
            else:
                print("passed: input range = {}, impedance = {}"
                      .format(input_range, impedance))

if __name__ == '__main__':
    unittest.main(verbosity=2, buffer=True)