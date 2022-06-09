import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:

        def parseMonth(month):
            if month=='Jan':
                return 0
            elif month=='Feb':
                return 1
            elif month=='Mar':
                return 2
            elif month=='Apr':
                return 3
            elif month=='May':
                return 4
            elif month=='June':
                return 5
            elif month=='Jul':
                return 6
            elif month=='Aug':
                return 7
            elif month=='Sep':
                return 8
            elif month=='Oct':
                return 9
            elif month=='Nov':
                return 10
            elif month=='Dec':
                return 11
            

        reader = csv.reader(f)
        # Header row
        next(reader)

        (evidence, labels) = ([], [])

        for row in reader:
            # Adding to label
            labels.append(1 if row[17]!='FALSE' else 0)

            # Adding to Evidence
            evidence.append(
                [
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                    row[9],
                    parseMonth(row[10]),
                    row[11],
                    row[12],
                    row[13],
                    row[14],
                    1 if row[15]=='Returning_Visitor' else 0,
                    1 if row[16]!='FALSE' else 0
                ]
            ) 

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    trues_count = 0
    specificity = 0
    falses_count = 0

    for i in range(len(labels)):
        if labels[i] ==1:
            trues_count += 1
            sensitivity += 1 if predictions[i]==1 else 0
        else:
            falses_count += 1 
            specificity += 1 if predictions[i]==0 else 0

    sensitivity /= trues_count
    specificity /= falses_count

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
