import configparser
import os
from dps_meter import DPSMeter

def main():
    config = configparser.ConfigParser()
    ini_path = os.path.join(os.getcwd(),'config.ini')
    config.read(ini_path)

    dps_meter = DPSMeter(config)
    dps_meter.run()


if __name__ == '__main__':
    main()