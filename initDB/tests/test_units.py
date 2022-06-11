import unittest
from initDB import Atlas

class TestScheduleGeneration(unittest.TestCase):
    """Some simple unit tests"""
    def setUp(self):
        self.atlas = Atlas('test', 'test', 1000, 250, 1000000, 1)

        fake_driver_ids = []
        for d in range(1000):
            fake_driver_ids.append(f'Object({str(d).zfill(9)})')
        self.fake_driver_ids = fake_driver_ids

        fake_bus_ids = []
        for b in range(250):
            fake_bus_ids.append(f'Object({str(d).zfill(9)})')
        self.fake_bus_ids = fake_bus_ids

    def test_generate_drivers(self):
        """Test driver generation"""
        drivers = self.atlas.populate_drivers()
        self.assertEqual(len(drivers), 1000)

    def test_generate_schedules(self):
        """Test schedules generation"""
        schedules = self.atlas.populate_shcedules(self.fake_bus_ids)
        self.assertEqual(len(schedules), 1000000)
        


if __name__ == '__main__':
    unittest.main()