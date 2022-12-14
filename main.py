import datetime, os, csv, traceback, pygal
from prettytable import PrettyTable

FILENAME = "mood_tracker.csv"
DATE_FORMAT = "%m-%d-%Y"
debug = True
def inputData():
  while True:
    try:
      mood = int(input("Please enter your current mood on a scale of 1-10: "))
      if mood > 10 or mood < 1:
        print("Please enter a number between 1 and 10")
        raise ValueError
      stress = int(input("Please enter your current stress level on a scale of 1-10: "))
      if stress > 10 or stress < 1:
        print("Please enter a number between 1 and 10")
        raise ValueError
      sleep = int(input("Please enter your current sleep quality on a scale of 1-10: "))
      if sleep > 10 or sleep < 1:
        print("Please enter a number between 1 and 10")
        raise ValueError
      date = datetime.datetime.now()
      date = date.strftime("%m-%d-%Y")
      data = [date, mood, stress, sleep]
      return data
    except (ValueError):
      continue
    except (KeyboardInterrupt):
      break
    except:
      if debug:
        print(f"Error: {traceback.print_exc()}")
      break
def outputData(data):  
  if os.path.exists(FILENAME):
      with open(FILENAME, "a", newline="") as file:
          writer = csv.writer(file)
          writer.writerow(data)
  else:
      with open(FILENAME, "w", newline="") as file:
          writer = csv.writer(file)
          writer.writerow(["Date", "Mood", "Stress Level", "Sleep Quality"])
          writer.writerow(data)

def csvToPrettyTable():
  table = PrettyTable()
  table.field_names = ["Date", "Mood", "Stress Level", "Sleep Quality"]
  with open(FILENAME, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
      table.add_row(row)
  print(table)
    
def csvToGraph():
  if os.path.exists(FILENAME):
    data = list(csv.reader(open(FILENAME)))
    data.remove(data[0])
    line_chart = pygal.Line()
    date = []
    for row in data:
      dates = datetime.datetime.strptime(row[0],DATE_FORMAT)
      dates = dates.date()
      date.append(dates)
    line_chart.x_labels = date
    line_chart.add("Mood Level", [int(row[1]) for row in data])
    line_chart.add("Stress Level", [int(row[2]) for row in data])
    line_chart.add("Sleep Quality", [int(row[3]) for row in data]) 
    line_chart.title = "Mood, Stress, and Sleep Tracker"
    line_chart.render_to_file("mood_data.svg")
  else:
    print("No data found")  
  
def main():
  while True:
    try:
      data = inputData()
      outputData(data)
      csvToPrettyTable()
      csvToGraph()
      break
    except:
      if debug:
        print(f"Error: {traceback.print_exc()}")
      print("\nExiting...")
      break  
if __name__ == "__main__":
  main()