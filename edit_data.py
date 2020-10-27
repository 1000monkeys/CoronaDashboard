import csv

from abbreviations import us_state_abbrev

states = {}
with open('covid-19-dataset-1.csv') as f:
    reader = csv.reader(f)
    next(reader)  # skip the first line with the column heads

    for row in reader:
        state_name = row[2]
        confirmed = int(row[7])

        if state_name in us_state_abbrev.keys():
            if state_name in states:
                states[us_state_abbrev[state_name]] += confirmed
            else:
                states[us_state_abbrev[state_name]] = confirmed

        with open('data-edited.csv', mode='w', newline='') as data_edited:
            state_writer = csv.writer(data_edited, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            state_writer.writerow(["StateCode", "Confirmed"])
            for state in states:
                state_writer.writerow([state, states[state]])
