In forensic accounting, identifying the cause of account imbalances is a tedious process that requires an archaeic methodology of analyzing individual transactions one-by-one.
To streamline the process, this program reads csv files with 3 attributes including "Document Number", "Date", and "Amount". It iterates through each row of the general ledger data 
to match and filter out pairs of values that offset eachother (ie. debits and their corresponding credits). It then outputs remaining values that have no offsetting counterpart (in other words, the transactions
that are causing the account imbalance) into a new csv file, along with their unique identifier and date. This eliminates dozens of labor hours, simplifying the process into exporting a 
general ledger to a csv file, and typing in the file path into the program. The only external work involved is ensuring the input csv file only includes the 3 aforementioned attributes, 
the date is in year/month format, and the amount column values are integer data types. Happy reconciling!
