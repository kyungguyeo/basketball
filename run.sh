#!/usr/bin/env bash
mkdir gamescores
mkdir seasonstandings
mkdir playergamelogs
mkdir playerseasonlogs

$SPARK_HOME/bin/spark-submit scraper.py

hdfs dfs -mkdir /data
hdfs dfs -mkdir /data/gamescores
hdfs dfs -mkdir /data/seasonstandings
hdfs dfs -mkdir /data/playergamelogs
hdfs dfs -mkdir /data/playerseasonlogs

hdfs dfs -put gamescore /data/gamescores
hdfs dfs -put seasonstandings /data/seasonstandings
hdfs dfs -put playergamelogs /data/playergamelogs
hdfs dfs -put playerseasonlogs /data/playerseasonlogs

##HIVE STUFF


