--Create NBA Data DB
create database nba_db;
use nba_db;

--Map Game Scores (Box Scores)

DROP TABLE IF EXISTS gamescores;
CREATE EXTERNAL TABLE gamescores(
    winner_team VARCHAR(500),
    loser_team VARCHAR(500),
    winner_score INT,
    loser_score INT,
    game_date DATE
    )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar" = ",")
stored as textfile
location '/data/gamescores'
tblproperties ("skip.header.line.count"="1");


-- Season Standings Data

DROP TABLE IF EXISTS seasonstandings;
CREATE EXTERNAL TABLE seasonstandings (
    team VARCHAR(500),
    wins INT,
    losses INT,
    season_year INT
    )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar" = ",")
stored as textfile
location '/data/seasonstandings'
tblproperties ("skip.header.line.count"="1");


--Player Season Data

DROP TABLE IF EXISTS playerseasondata;
CREATE EXTERNAL TABLE playerseasondata (
    league_id VARCHAR(500),
    games_started INT,
    fg_pct FLOAT,
    stl_per_g FLOAT,
    pos VARCHAR(500),
    pts_per_g FLOAT,
    team_id VARCHAR(500),
    fg2a_per_g FLOAT,
    pf_per_g FLOAT,
    efg_pct FLOAT,
    fta_per_g FLOAT,
    blk_per_g FLOAT,
    fg2_per_g FLOAT,
    fg3a_per_g FLOAT,
    ast_per_g FLOAT,
    fga_per_g FLOAT,
    ft_pct FLOAT,
    fg_per_g FLOAT,
    season VARCHAR(500),
    orb_per_g FLOAT,
    fg3_pct FLOAT,
    ft_per_g FLOAT,
    trb_per_g FLOAT,
    tov_per_g FLOAT,
    g INT,
    age INT,
    drb_per_g FLOAT,
    fg2_pct FLOAT,
    fg3_per_g FLOAT,
    mp_per_g FLOAT,
    player_name VARCHAR(500)
    )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar" = ",")
stored as textfile
location '/data/playerseasonlogs'
tblproperties ("skip.header.line.count"="1");


--Player Game Data (Box Scores)

DROP TABLE IF EXISTS playergamedata;
CREATE EXTERNAL TABLE playergamedata (
    gs INT,
    opp_id  VARCHAR(500),
    fg_pct FLOAT,
    fg3 FLOAT,
    game_result  VARCHAR(500),
    team_id  VARCHAR(500),
    pts INT,
    game_location  VARCHAR(500),
    tov INT,
    fta INT,
    game_score FLOAT,
    pf INT,
    blk INT,
    ft_pct FLOAT,
    fg3a INT,
    ft INT,
    ranker INT,
    ast INT,
    game_season INT,
    fg3_pct FLOAT,
    fg INT,
    orb INT,
    fga INT,
    stl INT,
    age  VARCHAR(500),
    trb INT,
    date_game DATE,
    mp  VARCHAR(500),
    drb INT,
    player_name VARCHAR(500)
    )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar" = ",")
stored as textfile
location '/data/playergamelogs'
tblproperties ("skip.header.line.count"="1");