import operator
from datetime import datetime, time, timedelta
from race.log_utils import split_log_line


class Driver:
    """
    A class used to represent a race driver

    Attributes
    ----------
    code : str
        the identifier of the driver
    name : str
        the name of the driver
    """

    def __init__(self, code, name):
        """Initializes class attributes

        Parameters
        ----------
        code : str
            the identifier of the driver
        name : str
            The name of the animal
        """
        self.code = code
        self.name = name

    def __str__(self):
        """Prints the driver information formatted"""
        return "{} - {}".format(self.code, self.name)


class Lap:
    """
    A class used to represent one lap in a race

    Attributes
    ----------
    hour : time
        time the lap happened
    number : str
        the number of the lap
    time_lap : time
        time to complete the lap
    average_speed: float
        average lap speed
    """

    def __init__(self, hour, number, time_lap, average_speed):
        """Initializes class attributes

        Parameters
        ----------
        hour : str
            time the lap happened
        number : str
            the number of the lap
        time_lap : str
            time to complete the lap
        average_speed: str
            average lap speed
        """
        self.hour = datetime.strptime(hour, "%H:%M:%S.%f")
        self.number = number
        self.time_lap = datetime.strptime(time_lap, "%M:%S.%f")
        self.average_speed = float(average_speed.replace(",", "."))


class Result:
    """
    A class used to represent final race result of the driver

    Attributes
    ----------
    position : int
        final ranking of the driver
    completed_laps : str
        number of completed laps of the driver
    total_time : time
        time to complete race
    """

    def __init__(self):
        """Initializes class attributes

            All attributes are initialize with zero
        """
        self.position = 0
        self.completed_laps = 0
        self.total_time = datetime(1, 1, 1, 0, 0, 0)

    def __str__(self):
        """Prints the result of the driver formatted"""
        return """
            Posição de Chegada: {}
            Quantidade de Voltas Completas: {}
            Tempo Total de Prova: {}
        """.format(self.position,
                   self.completed_laps,
                   self.total_time.strftime("%M:%S.%f"))


class Racing:
    """
    A class used to represent a race

    Attributes
    ----------
    drivers : dict {driver_code: driver_obj}
       dictionary with all race drivers
    laps : dict {driver_code: [lap_obj]}
       dictionary with all laps per driver
    result : dict {driver_code: result_obj}
       dictionary with final result per driver

    Methods
    -------
    last_lap_driver(driver_code)
        Finds a last lap of a driver
    sum_time_lap_driver(driver_code)
        Adds the times of each turn of a driver
    get_or_create_result(driver_code)
        Gets or creates a result instance for a driver
    calculate_position()
        Calculates the position of all race drivers
    calculate_completed_laps()
        Calculates the number of complete laps of all race drivers
    calculate_total_time()
        Calculates the total time of all race drivers
    calculate_result()
        Calls the methods to calculate the race result
    parser_log_file(file_name)
        Reads a log file with the information to create a race
    """

    def __init__(self):
        """Initializes class attributes

           All attributes are initialize with empty dictionary
        """
        self.drivers = {}
        self.laps = {}
        self.result = {}

    def __str__(self):
        """Prints the result of the driver formatted"""
        for code in self.result.keys():
            print("{} {}".format(self.drivers.get(code, ''),
                                 self.result.get(code, '')))

    def last_lap_driver(self, driver_code):
        """Finds a last lap of a driver
        Parameters
        ----------
        driver_code : str
            the identifier of the driver

        Returns
        -------
        Lap Object
            lap object that represents the driver's last lap
        """
        return sorted(self.laps[driver_code],
                      key=operator.attrgetter('number'))[-1]

    def sum_time_lap_driver(self, driver_code):
        """Adds the times of each turn of a driver
        Parameters
        ----------
        driver_code : str
            the identifier of the driver

        Returns
        -------
        time
            sum of the times of the driver's laps
        """
        sum = datetime(1, 1, 1, 0, 0, 0)
        for lap in self.laps[driver_code]:
            sum = sum + timedelta(minutes=lap.time_lap.minute,
                                  seconds=lap.time_lap.second,
                                  microseconds=lap.time_lap.microsecond)
        return sum

    def get_or_create_result(self, driver_code):
        """Gets or creates a result instance for a driver
        Parameters
        ----------
        driver_code : str
            the identifier of the driver

        Returns
        -------
        Result Object
            the result of the driver's race
        """
        result = self.result.get(driver_code, None)
        if not result:
            result = Result()
            self.result[driver_code] = result
        return result

    def calculate_position(self):
        """Calculates the position of all race drivers"""
        laps = [(code, self.last_lap_driver(code).hour) for code in
                self.drivers.keys()]
        laps.sort(key=lambda tup: tup[1])

        for i in range(len(laps)):
            code, _ = laps[i]
            result = self.get_or_create_result(code)
            result.position = i + 1

    def calculate_completed_laps(self):
        """Calculates the number of complete laps of all race drivers"""
        for code in self.drivers.keys():
            count_laps = len(self.laps[code])
            result = self.get_or_create_result(code)
            result.completed_laps = count_laps

    def calculate_total_time(self):
        """Calculates the total time of all race drivers"""
        for code in self.drivers.keys():
            time_laps = self.sum_time_lap_driver(code)
            result = self.get_or_create_result(code)
            result.total_time = time_laps

    def calculate_result(self):
        """Calls the methods to calculate the race result"""
        self.calculate_position()
        self.calculate_completed_laps()
        self.calculate_total_time()

    def parser_logfile(self, file_name):
        """Reads a log file with the information to create a race
        Parameters
        ----------
        file_name : str
            the path of log file
        """
        with open(file_name) as file_obj:

            # skip header
            next(file_obj)

            # read lines of file
            for line in file_obj:

                # split columns of a line
                columns = split_log_line(line)

                # check if the line has all the information
                if len(columns) != 6:
                    continue

                hour = columns[0]
                code = columns[1]
                name = columns[2]
                number = columns[3]
                time = columns[4]
                average_speed = columns[5]

                # create lap object
                lap = Lap(hour, number, time, average_speed)

                # try get driver using code
                driver = self.drivers.get(code, None)

                # check if driver exist, if not create a new
                if not driver:
                    driver = Driver(code, name)
                    self.drivers[code] = driver

                self.laps[driver.code] = self.laps.get(driver.code, []) + [lap]

        self.calculate_result()