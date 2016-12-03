#!/usr/bin/env bash
##Script for setting up hive on hdfs

wget http://apache.claz.org/hive/stable/apache-hive-1.2.1-bin.tar.gz
mkdir /usr/local/hive
tar -zvf apache-hive-1.2.1-bin.tar.gz /root/hive

# Set HIVE_HOME
export HIVE_HOME="/usr/local/apache-hive-1.2.1-bin"
PATH=$PATH:$HIVE_HOME/bin
export PATH

# Set Hadoop path in Hive
echo "export HADOOP_HOME=/usr/local/Cellar/hadoop/2.7.3/" >> /usr/local/hive/apache-hive-1.2.1-bin/bin/hive-config.sh

# Set up Hive warehouse in HDFS
 hdfs dfs -mkdir /hive
 hdfs dfs -mkdir /hive/warehouse
 hdfs dfs -chmod g+w /hive/warehouse

