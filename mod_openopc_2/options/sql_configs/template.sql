# -------------------------------------------------------------------
# mod_openopc	
# -------------------------------------------------------------------
# ... integrating the Python OpenOPC project to run HMI
#     over Linux, BSD, any Unix, and now Shitty Windows
#     in an unfettered manner.
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# COPYRIGHT
#
# SEE README FILE FOR COPYRIGHT INFORMATION
# -------------------------------------------------------------------
# -------------------------------------------------------------------
#
# --------------------- QUICK INFO ----------------------------------
# Each SQL server must have its own configuration file.
# To make a new file, simply copy this file, and edit the parameters
#   to suit your needs.
#
#          path/options/sql_configs/cheese_table1.sql 
#
#		... should contain info about the database which
#		    is named 'cheese' in your server.
#		... should only be configured for table1
#
# You will have one config file per db.
#
# --------------------- DECLARATIONS --------------------------------
#
[sql_server_configs]
MYSQLDB:modopenopc		
# DATABASE NAME
MYSQLIP:localhost
# IPADDRESS, should be "localhost" or actual IP address
# -- USE "QUOTES" FOR IF RUNNING THIS PROGRAM UNDER UNIX
# -- DO NOT USE QUOTES IF RUNNING UNDER WIN
MYSQLFAULT:modopenopc		
# DATABASE THAT HOLDS FAULT TABLE
FAULTTABLENAME:system_faults	
# FAULT TABLE NAME
MYSQLUSER:yourmysqlusername
# YOUR MYSQL USERNAME
MYSQLPASS:yourmysqluserpassword		
# YOUR MYSQL PASSWORD
COMMITTRANSACTIONS:YES
# COMMIT DATABASE TRANSACTIONS AFTER EXECUTION
# -- YES or NO
# -- TRANSACTIONAL DATABASES SUCH AS INNODB REQUIRE
#    THIS FUNCTIONALITY, FUTURE MYISAM WILL ALSO
MYSQLRETENTION:3		
# DB RETENTION TIME FOR RECORDS IN YEARS
FIELDRETENTION:DATESTAMP	
# FIELD TO CARRY OUT RETENTION QUERY ON
MYSQLMAINTTABLES:TABLE1,TABLE2,system_faults
# TABLE NAMES (CASE SENSITIVE) TO PERFORM PERIODIC 
# MAINTENANCE ON WHEN CALLING 'MAINT_DB' FUNCTION
# -- DO NOT INCLUDE ANY TABLES THAT ARE SUPPOSED
#    BE STATIC
# -- DO NOT INCLUDE TRAILING PIPE!
# -- FORM IS TABLE1,TABLE2,TABLE3   
# -- -- NO QUOTES, NO SPACES
# -- -- SHOULD ALWAYS INCLUDE system_faults 
#       UNLESS YOU ARE RUNNING A CUSTOM SCHEME
# -------------------------------------------------------------------

