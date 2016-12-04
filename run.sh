#!/usr/bin/env bash
cd
mkdir gamescores
mkdir seasonstandings
mkdir playergamelogs
mkdir playerseasonlogs

$SPARK_HOME/bin/spark-submit scraper.py
./hive.sh

hdfs dfs -mkdir /data
hdfs dfs -mkdir /data/gamescores
hdfs dfs -mkdir /data/seasonstandings
hdfs dfs -mkdir /data/playergamelogs
hdfs dfs -mkdir /data/playerseasonlogs

hdfs dfs -put /root/gamescore /data/gamescores
hdfs dfs -put /root/seasonstandings /data/seasonstandings
hdfs dfs -put /root/playergamelogs /data/playergamelogs
hdfs dfs -put /root/playerseasonlogs /data/playerseasonlogs