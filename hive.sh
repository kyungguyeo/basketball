#!/usr/bin/env bash
##Script for setting up hive
cd
wget http://apache.claz.org/hive/stable/apache-hive-1.2.1-bin.tar.gz
mkdir /usr/local/hive
tar -xf apache-hive-1.2.1-bin.tar.gz
mv apache-hive-1.2.1-bin /usr/local/hive

# Set HIVE_HOME
export HIVE_HOME="/usr/local/hive/apache-hive-1.2.1-bin"
PATH=$PATH:$HIVE_HOME/bin
export PATH

# Set Hadoop path in Hive
echo "export HADOOP_HOME=/usr/local/hadoop/" >> /usr/local/hive/apache-hive-1.2.1-bin/bin/hive-config.sh