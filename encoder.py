import RPi.GPIO as GPIO
import time

def sensor_setup(pin):
    GPIO.setup(7, GPIO.IN)

def calc_raw_rpm(milliseconds, count):
    """
    Get rotations per minute for encoder values.
    :param milliseconds: The number of milliseconds data was taken for.
    :param count: The number of HIGH signals read from the encoder.
                  This is equivalent to the amount of times the light sensor detected a hole.
    :return: The speed of the encoder in rotations per minute.
    """
    rps = count / (1000 * milliseconds)
    return rps * 60

def current_milli_time():
    return round(time.time() * 1000)

def get_rpm(pin):
    """
    Reads the rpm from the encoder. Gear ratio calculations will have to be done for the rpm of the wheel.
    NOTE: THIS IS BLOCKING CODE!!! DO NOT RUN OFTEN
    :param pin: Pin of the encoder to read.
    :return: The current RPM of the encoder.
    """
    # CONSTANT: The minimum number of readings of data
    min_count = 20
    # CONSTANT:The maximum amount of time for this reading
    max_time_ms = 20
    start_time = current_milli_time()
    count = 0
    last_state = False
    while count < min_count and current_milli_time() - start_time < max_time_ms:
        curr_state = GPIO.input(pin)
        if curr_state != last_state:
            last_state = curr_state
            count = count + 1
    return calc_raw_rpm(current_milli_time() - start_time, count)

def get_wheel_speed(pin):
    """
    Reads the rpm from the encoder and converts it to the rpm of the wheel
    NOTE: THIS IS BLOCKING CODE!!! DO NOT RUN OFTEN
    :param pin: Pin of the encoder to read.
    :return: The current RPM of the wheelchair wheel.
    """
    # The current gear ratio from the encoder to the wheel is 2:1
    encoder_rpm = get_rpm(pin)
    return encoder_rpm / 2
