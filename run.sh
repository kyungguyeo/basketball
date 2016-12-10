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

# LOAD DATA INTO HDFS
cd
mkdir urls
python basketball/url_aggregator.py

cat urls/player_urls.txt | python basketball/player_season_logs/mapper_playerseasonlogs.py | \
    python basketball/player_season_logs/reducer_playerdata.py
cat urls/player_urls.txt | python basketball/player_game_logs/mapper_playergamelogs.py | \
    python basketball/player_game_logs/reducer_playerdata.py
cat urls/boxscore_urls.txt | python basketball/boxscores/mapper.py | \
    python basketball/boxscores/reducer_boxscores.py
cat urls/seasonstanding_urls.txt | python basketball/season_standings/mapper.py | \
    python basketball/season_standings/reducer_seasonstandings.py

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