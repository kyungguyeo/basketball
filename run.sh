#!/usr/bin/env bash
echo -n "IP of master > "
read ip

ssh root@$ip
cd
git clone https://github.com/kyungguyeo/basketball.git

hdfs dfs -mkdir /gamescores_raw
hdfs dfs -mkdir /playerseasonlogs_raw
hdfs dfs -mkdir /playergamelogs_raw
hdfs dfs -mkdir /seasonstandings_raw

python url_scraper.py

hdfs dfs -mkdir /data
hdfs dfs -mkdir /data/gamescores
hdfs dfs -mkdir /data/seasonstandings
hdfs dfs -mkdir /data/playergamelogs
hdfs dfs -mkdir /data/playerseasonlogs

$SPARK_HOME/bin/spark-submit --master yarn --deploy-mode cluster scraper.py

ssh root@$ip
chmod a+x basketball/hive.sh
basketball/hive.sh

hive basketball/hive_db_setup.sh

python url_aggregator.py
hdfs dfs -mkdir /urls
hdfs dfs -put player_urls.txt /urls
hdfs dfs -put seasonstanding_urls.txt /urls
hdfs dfs -put boxscore_urls.txt /urls


/urls

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar \
    -file mapper.py -mapper mapper.py \
    -file reducer.py -reducer reducer.py \
    -input hdfs://23.246.218.75/urls/seasonstanding_urls.txt -output hdfs://23.246.218.75/test/