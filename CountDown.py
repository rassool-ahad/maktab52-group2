#Rasool Ahadi - Reza Gholami - Sepehr Bazyar
import datetime, time, argparse

parser = argparse.ArgumentParser(description = "It's Countdown App")
parser.add_argument("time", type = str, action = "store", default = None , nargs = "?")
parser.add_argument("-ss", "--sec", type = int, action = "store", metavar = "SECONDS", default = 0)
parser.add_argument("-mm", "--min", type = int, action = "store", metavar = "MINUTE", default = 0)
parser.add_argument("-hh", "--hour", type = int, action = "store", metavar = "HOUR", default = 0)
args = parser.parse_args()

if args.time:
    date = str(datetime.datetime.now().date())
    countdown_start = datetime.datetime.fromisoformat(date + " "+ args.time) - datetime.datetime.now()
    while True:
        try:
            print(countdown_start)
            time.sleep(1)
            countdown_start -= datetime.timedelta(seconds = 1)
            if countdown_start.total_seconds() < 1:
                print("Timeps UP!!")
                break
        except KeyboardInterrupt:
            print("Fineshed!!")
            break

else:
    date = str(datetime.datetime.now().date())
    ti = datetime.datetime.fromisoformat(date +f" {args.hour:02}:{args.min:02}:{args.sec:02}")
    while True:
        try:
            print(ti)
            ti -= datetime.timedelta(seconds = 1)
            time.sleep(1)
            if ti.time().second == 0 and ti.time().minute == 0 and ti.time().hour == 0:
                print("Times UP!!")
                break
        except KeyboardInterrupt:
            print("Fineshed!!")
            break
