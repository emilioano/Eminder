from eminder.main import run
from eminder.utils.logger import log,debug,info,warning,error,critical

if __name__ == '__main__':
    try:
        run()

    except Exception as err:
        error(f'Application stopped with following: {err}')

    except KeyboardInterrupt:
        log(f'Application was stopped with keyboard interrupt.')

    