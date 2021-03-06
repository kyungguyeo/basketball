from subprocess import call

def interacter():
    """
    The 'frontend' for the project. Series of commandline prompts that allows the user to download the desired data.
    Can be used to download 1 file at a time, or give ranges to download multiple.
    """
    print """


                !!!!WELCOME TO BALLGEEK!!!!

                        ..ee$$$$$ee..
                   .e$*      $      *$e.
                 z$ *.       $         $$c
               z$    *.      $       .P  ^$c
              d       *      $      z       b
             $         b     $     4%       ^$
            d%         *     $     P          $
           .$           F    $    J          $r
           4L           b    $    $           J$
           $F$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
           4F          4F    $    4r          4P
           ^$          $     $     b          $%
            3L        .F     $      r        JP
             *c       $      $      3.      z$
              *b     J      $       3r    dP
               ^$c  z%       $        c z$
                 *$L        $        .d$
                    *$ee..  $  ..ze$P
                        *******

    Make sure the local Hadoop configuration files are the same as the configuration files of the spark application.
    """
    mode_resp = mode()
    retriever(mode_resp)


def mode():
    mode_resp = raw_input("What kind of data do you want? "
                          "(gamescore[g]/seasonstandings[s]/playergamelogs[pg]/playerseasonlogs[ps]): ")
    if mode_resp in ['g','s','pg','ps']:
        return mode_resp
    else:
        print "I didn't understand your input."
        mode()


def retriever(m):
    if m == 'g':
        w = raw_input("You entered gamescore. Please input the desired date range, "
                      "in mmddyyyy format for one day, and mmddyyyy;mmddyyyy;... format for multiple days: ")
        dates = w.split(';')
        for date in dates:
            hdfs_path = '/data/gamescore/' + date + '_boxscore.csv'
            command = "hdfs dfs -get " + hdfs_path
            commands = command.split(" ")
            call(commands)
        print "data downloaded from hdfs."
    elif m == 's':
        w = raw_input("You entered seasonstandings. Please input the desired year range, "
                      "in yyyy format for 1 year, and yyyy;yyyy;... format for multiple years: ")
        years = w.split(';')
        for year in years:
            hdfs_path = '/data/seasonstandings/' + year + 'seasonstandings.csv'
            command = "hdfs dfs -get " + hdfs_path
            commands = command.split(" ")
            call(commands)
        print "data downloaded from hdfs."
    elif m == 'pg':
        w = raw_input("You entered playergamelogs. Please input the desired player ids and desired year, "
                      "in player_id-yyyy format (player_id found under http://www.basketball-reference.com/players/)."
                      " For multiple, separate id-yyyy's with semicolons (;). If you want all gamelogs of a player,"
                      "add just the names, without any years: ")
        names = w.split(';')
        for name in names:
            player = name.split('-')
            if len(player) == 2:
                hdfs_path = '/data/playergamelogs/' + player[0] + 'gamelog' + player[1] + '.csv'
                command = "hdfs dfs -get " + hdfs_path
            else:
                hdfs_path = '/data/playergamelogs/' + player[0] + '*'
                command = "hdfs dfs -get " + hdfs_path
            commands = command.split(" ")
            call(commands)
        print "data downloaded from hdfs."
    elif m == 'ps':
        w = raw_input("You entered playerseasonlogs. Please input the desired player ids (found under "
                      "http://www.basketball-reference.com/players/). For multiple, separate ids with semicolons (;): ")
        names = w.split(';')
        for name in names:
            hdfs_path = '/data/playerseasonlogs/' + name + '_seasonlogs.csv'
            command = "hdfs dfs -get " + hdfs_path
            commands = command.split(" ")
            call(commands)
        print "data downloaded from hdfs."
    else:
        print "I didn't understand your input."
        retriever(m)

if __name__ == "__main__":
    interacter()
