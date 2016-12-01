mkdir gamescore
mkdir seasonstandings
mkdir playergamelogs
mkdir playerseasonlogs

$SPARK_HOME/bin/spark-submit scraper.py

hdfs dfs -mkdir /data/gamescore
hdfs dfs -mkdir /data/seasonstandings
hdfs dfs -mkdir /data/playergamelogs
hdfs dfs -mkdir /data/playerseasonlogs

hdfs dfs -put gamescore /data/gamescore
hdfs dfs -put seasonstandings /data/seasonstandings
hdfs dfs -put playergamelogs /data/playergamelogs
hdfs dfs -put playerseasonlogs /data/playerseasonlogs

##HIVE STUFF

