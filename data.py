import random
import os

class dataset:

    # Read a dataset from an input file
    def __init__(self, filename):

        if filename.endswith(".csv"):
            self.load_from_csv(filename)
        else:
            raise Exception("Unkown filetype "+filename)

    # Load the dataset from a csv file
    def load_from_csv(self, filename):
        
        names = None
        rows  = []
        with open(filename) as csv:
            for line in csv:
                
                # If this is the first line, see if it contains
                # names, or data
                if names is None:
                    names = [w for w in line.split(",")]
                    try:
                        # If this is a data row, name by column number
                        row   = [float(n) for n in names]
                        names = [i+1 for i in range(len(names))]
                    except:
                        # This was a names row, skip to next line
                        continue

                # Parse a data row
                try:
                    parse_float = lambda w : None if len(w.strip()) == 0 else float(w) 
                    row = [parse_float(w) for w in line.split(",")]
                except:
                    raise Exception("Could not parse csv line:\n"+line)

                # Check all the rows have the same length
                if len(rows) > 0:
                    if len(rows[0]) != len(row):
                        raise Exception("Row length mismatch in csv!")

                # Add the row
                rows.append(row)

        self.column_names = names
        self.rows = rows

    # Convert this object to a descriptive string
    def __str__(self):
        
        fs = "Dataset containing {0} columns and {1} rows"
        return fs.format(len(self.rows[0]), len(self.rows))

    # Set the column with the given name as the last column
    def set_last_column(self, column_name):

        name = column_name
        if not name in self.column_names:
            raise Exception("Could not find the column "+name+"!")

        # Swap the column names
        i = self.column_names.index(name)
        tmp                   = self.column_names[-1]
        self.column_names[-1] = name
        self.column_names[i]  = tmp

        # Swap the data columns
        for row in self.rows:
            tmp     = row[-1]
            row[-1] = row[i]
            row[i]  = tmp

    # Generate an input_train.csv and input_validate.csv from this dataset
    def gen_train_validate(self, train_percent):
        
        if train_percent > 100 or train_percent < 0:
            raise Exception("{0} is not a valid percentage!".format(train_percent))

        train_rows = int(len(self.rows) * train_percent / 100.0)
        random.shuffle(self.rows)
        
        to_string = lambda f : "" if f is None else str(f)
    
        with open("input.csv", "w") as f:
            for row in self.rows[0: train_rows]:
                f.write(",".join([to_string(w) for w in row])+"\n")

        with open("input_validate.csv", "w") as f:
            for row in self.rows[train_rows:]:
                f.write(",".join([to_string(w) for w in row])+"\n")

# Get the hydrides dataset from google docs
def hydrides_dataset():
    url  = "https://docs.google.com/spreadsheets/d/"
    url += "14EAJUxTejpKxMGd4b5i8BPBmLOzL8sOIpRYkcn2C1Kc/"
    url += "export?format=csv&id=14EAJUxTejpKxMGd4b5i8BPB"
    url += "mLOzL8sOIpRYkcn2C1Kc&gid=1868430126"
    os.system('wget "{0}" -O tmp.csv'.format(url))
    d = dataset("tmp.csv")
    os.system("rm tmp.csv")
    return d
