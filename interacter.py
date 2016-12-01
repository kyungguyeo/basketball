import csv

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

    Alright, it looks like the database has finished downloading.
    """
    mode_resp = mode()
    retriever(mode_resp)



def mode():
    mode = raw_input("What kind of data do you want? (gamescore[g]/seasonstandings[s]/playergamelogs[pg]\
    /playerseasonlogs[ps]): ")
    if mode == ('g' or 's' or 'pg' or 'ps'):
        return mode
    else:
        print "I didn't understand your input."
        mode()

def retriever(m):
    if m == 'g':
        w = raw_input("You entered gamescore. Please input the desired date range, in mmddyyyy format for one day, and \
        mmddyyyy-mmddyyyy format for multiple days: ")
        dates = w.split('-')
        for date in dates:
            path = 'hdfs://gamescore/' + date + '.csv'
            pass
    elif m == 's':
        w = raw_input("You entered seasonstandings. Please input the desired year range, in yyyy format for 1 year, and\
                      yyyy-yyyy format for multiple years: ")
        dates = w.split('-')
        for date in dates:
            path = 'hdfs://seasonstandings/' + date + '.csv'
            pass
    elif m == 'pg':
        w = raw_input("You entered playergamelogs. Please input the desired player ids (found under \
        http://www.basketball-reference.com/players/). For multiple, separate ids with semicolons (;): ")
        names = w.split(';')
        for name in names:
            path = 'hdfs://playergamelogs/' + name + '.csv'
            pass
    elif m == 'ps':
        w = raw_input("You entered playerseasonlogs. Please input the desired player ids (found under \
        http://www.basketball-reference.com/players/). For multiple, separate ids with semicolons (;): ")
        names = w.split(';')
        for name in names:
            path = 'hdfs://playerseasonlogs/' + name + '.csv'
            pass
    else:
        print "I didn't understand your input."
        window(m)