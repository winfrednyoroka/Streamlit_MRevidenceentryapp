#handy sql commands

#Initialise the database
sqlite3 Mr_evidenceDB

#check the schema the commands used to establish
.schema

#check the names of tables in the database
.table or .tables

#Check the contents of the table (just the attribute names and their data types)
PRAGMA table_info(tablename)

#alter the table to add a new column
ALTER TABLE results ADD standard_error REAL;
#insert values on the fly just for a given column meeting certain conditions on other attributes

UPDATE results standarderror=0.4 WHERE results_id=="R22";Updating an entry with two where clauses
UPDATE results SET effectsize=1.25 WHERE id=123 AND outcomeid=O7
