import unittest
from datetime import datetime
from race.race import Driver, Lap, Result, Racing


class TestDriverClass(unittest.TestCase):

    def setUp(self):
        self.code = "026"
        self.name = "Lucas"

    def test_init(self):
        obj = Driver(self.code, self.name)
        self.assertEqual(obj.code, self.code)
        self.assertEqual(obj.name, self.name)

    def test_representation(self):
        obj = Driver(self.code, self.name)
        expected = "{} - {}".format(self.code, self.name)
        self.assertEqual(str(obj), expected)


class TestLapClass(unittest.TestCase):

    def setUp(self):
        self.hour = "23:49:08.277"
        self.number = "1"
        self.time_lap = "1:02.852"
        self.average_speed = "44,275"

    def test_init(self):
        obj = Lap(self.hour, self.number, self.time_lap, self.average_speed)
        self.assertEqual(obj.hour, datetime.strptime(self.hour, "%H:%M:%S.%f"))
        self.assertEqual(obj.number, self.number)
        self.assertEqual(obj.time_lap,
                         datetime.strptime(self.time_lap, "%M:%S.%f"))
        self.assertEqual(obj.average_speed,
                         float(self.average_speed.replace(",", ".")))

    def test_hour_value_error(self):
        with self.assertRaises(ValueError) as context:
            obj = Lap("Error", self.number, self.time_lap,
                      self.average_speed)
        self.assertTrue('does not match format' in str(context.exception))

    def test_time_lap_value_error(self):
        with self.assertRaises(ValueError) as context:
            obj = Lap(self.hour, self.number, "Error",
                      self.average_speed)
        self.assertTrue('does not match format' in str(context.exception))

    def test_average_speed_value_error(self):
        with self.assertRaises(ValueError) as context:
            obj = Lap(self.hour, self.number, self.time_lap,
                      "Error")
        self.assertTrue('could not convert string to float' in str(context.exception))


class TestResultClass(unittest.TestCase):

    def setUp(self):
        self.result = Result()
        self.position = 1
        self.completed_laps = 5
        self.total_time = datetime(1, 1, 1, 0, 5, 5, 5)

    def test_init(self):
        self.assertEqual(self.result.position, 0)
        self.assertEqual(self.result.completed_laps, 0)
        self.assertEqual(self.result.total_time, datetime(1, 1, 1, 0, 0, 0))

    def test_attribution(self):
        self.result.position = self.position
        self.result.completed_laps = self.completed_laps
        self.result.total_time = self.total_time

        self.assertEqual(self.result.position, self.position)
        self.assertEqual(self.result.completed_laps, self.completed_laps)
        self.assertEqual(self.result.total_time, self.total_time)

    def test_representation(self):
        expected = """
            Posição de Chegada: {}
            Quantidade de Voltas Completas: {}
            Tempo Total de Prova: {}
        """.format(self.result.position,
                   self.result.completed_laps,
                   self.result.total_time.strftime("%M:%S.%f"))
        self.assertEqual(str(self.result), expected)


class TestRacingClass(unittest.TestCase):

    def setUp(self):
        self.racing = Racing()
        self.driver_code = "1"
        self.laps = {
            self.driver_code: [
                Lap("01:01:01.1", "1", "1:01.1", "1"),
                Lap("01:03:01.1", "3", "1:01.1", "1"),
                Lap("01:02:01.1", "2", "1:01.1", "1")
            ]
        }
        self.result = {
            self.driver_code: Result()
        }

    def test_init(self):
        self.assertEqual(self.racing.drivers, {})
        self.assertEqual(self.racing.laps, {})
        self.assertEqual(self.racing.result, {})

    def test_last_lap_driver(self):
        self.racing.laps = self.laps
        self.assertEqual(self.racing.last_lap_driver(self.driver_code),
                         self.laps[self.driver_code][1])

    def test_sum_time_lap_driver(self):
        self.racing.laps = self.laps
        self.assertEqual(self.racing.sum_time_lap_driver(self.driver_code),
                         datetime(1, 1, 1, 0, 3, 3, 300000))

    def test_get_or_create_result(self):
        self.racing.result = self.result
        self.assertEqual(self.racing.get_or_create_result(self.driver_code),
                         self.result[self.driver_code])
