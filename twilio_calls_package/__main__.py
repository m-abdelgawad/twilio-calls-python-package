import os
import yaml
import traceback
from packages.file import file
from packages.logger import logger
from packages.twiliotools import twiliotools
import time

# Initiate logger
log = logger.get(app_name='twilio_calls', enable_logs_file=True)


def main():

    log.info('Start program execution')

    project_abs_path = file.caller_dir_path()

    # Import configurations
    config_path = os.path.join(project_abs_path, 'config.yaml')
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    twilio_connection = twiliotools.TwilioTools(
        account_sid=config['twilio']['account_sid'],
        auth_token=config['twilio']['auth_token']
    )

    # Initiate a call
    call_sid = twilio_connection.call(
        from_num=config['twilio']['from_num'],
        to_num=config['twilio']['to_num'],
        msg='Hello Automation'
    )
    log.info('Initiated the call successfully')
    log.info('The call SID is: {0}'.format(call_sid))

    # Loop every one second to check the status of the call, until the call status
    # matches a Final Call Status
    seconds_passed = 0
    watchdog_counter = 0  # Safe counter
    max_watchdog_counter = 60
    final_call_statuses = ['completed', 'busy', 'no-answer', 'canceled', 'failed']

    while True:

        call_status = twilio_connection.get_call_status(sid=call_sid)

        if call_status in final_call_statuses:
            log.info('Final call status is: {0}, after {1} seconds.'.format(
                call_status, seconds_passed
            ))
            break

        else:
            log.debug('Current call status is {0}'.format(call_status))
            time.sleep(1)
            seconds_passed += 1
            watchdog_counter += 1
            if watchdog_counter == max_watchdog_counter:
                log.error('Waited 60 seconds without reaching a final call status')
                log.error('Last call status is {0}'.format(call_status))
                exit()

    # Get the logs of the call
    call_logs = twilio_connection.get_call_logs(
        sid=call_sid
    )
    log.info('The logs of the call SID {0} is:\n{1}'.format(call_sid, call_logs))

    log.info('Finished program execution')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log.error(e)
        log.error('Error Traceback: \n {0}'.format(traceback.format_exc()))
