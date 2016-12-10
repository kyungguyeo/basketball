# BallGeek
### A basketball-reference.com web scraper that uses Spark, Hadoop, and Hive to build a database designed for analysts.

## Set Up

1. Set up Hadoop/HDFS on Softlayer (or any other remote set of vms)

- Refer to Hadoop/HDFS homework ([link](https://github.com/MIDS-scaling-up/coursework/tree/master/week5/hw/hadoop_yarn_sort))
- Set up 10 machines at 100G of disk space each
- Be sure to remember the ip address of the master, as it will be needed for Spark setup

2. Set up Spark on local computer

- Refer to Intro to Spark homework ([link](https://github.com/MIDS-scaling-up/coursework/tree/master/week6/hw/apache_spark_introduction))

- No need to set this up remotely, just set it up locally on personal computer
- In running Spark with Yarn cluster, no need to have Spark on remote vms

4. Set up python on all machines (including remote vms)

- Python libraries required to run job:
    - BeautifulSoup (bs4)
    - pandas
    - requests
    - datetime

## Run the App

From local machine, run the shell script "run.sh", and input the public ip address of the master node of the remote vms.
This should:
 - Scrape data from basketball-reference.com
 - Set up hive
 - Put all data into HDFS
 - Create hive tables from data

After this is done, try logging in and testing the database:
```shell

ssh root@<ip_address>
hive
use nba_db;
show tables;
```

This should display all the tables and their descriptions.

## Downloading Data for Local Analysis

Data can also be downloaded in smaller chunks as csv files, and used for separate in-depth analysis.
Run python ```interacter.py``` and follow the prompts to download the files needed. They will downloand onto the local path.
