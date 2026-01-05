from modules import recipientmanager,taskmanager,schedulemanager
import schedulerservice

def menuoptions():
    print('='*60)
    print('Eminder main menu!')
    print('='*60)
    print('Make a selection.')
    print('1. Receipient manager (View, Enter, Delete Recipients).')
    print('2. Task manager (View, Enter, Delete Tasks).')
    print('3. Schedule manager (Run the task scheduler once, responsible for sending messages according to the tasks stored in DB).')
    print('4. Scheduler as service (Run the task scheduler as service, responsible for sending messages according to the tasks stored in DB).')
    print('0. Exit')
    print('='*60)


def run(): 

    selection = 0

    while True:
        try:
            menuoptions()
            selection = int(input())


            if selection < 0 or selection > 4:
                print('='*60)
                print('Invalid selection, try again!')
                print('='*60)
                continue

            elif selection == 1:
                recipientmanager.run_recipient_program()
                selection = 0

            elif selection == 2:
                taskmanager.run_task_manager()
                selection = 0

            elif selection == 3:
                schedulemanager.TaskManager().run()
                selection = 0

            elif selection == 4:
                schedulerservice.job()
                selection = 0

            elif selection == 0:
                break


        except ValueError:
            print('='*60)
            print('Invalid selection, try again!')
            print('='*60)
            continue


if __name__ == '__main__':
    run()