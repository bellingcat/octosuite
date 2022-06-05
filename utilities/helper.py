from utilities.colors import Color

class Help:
    usageText = 'Use {} to get started'
    def updateCommand():
        print(f'''
{Color.white}Update subcommands{Color.reset}
{'='*18}
{Help.usageText.format('update:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    check              Check for updates
    install            Download and install updates''')
        
        
    def searchCommand():
        print(f'''
{Color.white}Search subcommands{Color.reset}
{'='*18}
{Help.usageText.format('search:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    users              Search user(s)
    repos              Search repositor[yies]
    topics             Search topic(s)
    issues             Search issue(s)
    commits            Search commit(s)''')
            
            
    def userCommand():
        print(f'''
{Color.white}User subcommands{Color.reset}
{'='*17}
{Help.usageText.format('user:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    profile            Get a user's profile info
    gists              Return a users's gists
    orgs               Return organizations that a user belongs to/owns
    repos              Return a user's repositories
    events             Return a user's events
    followers          Return a user's followers
    following          Check if user[A] follows user[B]
    subscriptions      Return a user's subscriptions''')
        
        
    def orgCommand():
        print(f'''
{Color.white}Org subcommands{Color.reset}
{'='*16}
{Help.usageText.format('org:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    profile            Get an organization's info
    repos              Return an organization's repositories
    events             Return an organization's events
    member             Check if a specified user is a public member of the target organization''')
            
            
    def repoCommand():
        print(f'''
{Color.white}Repo subcommands{Color.reset}
{'='*17}
{Help.usageText.format('repo:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    profile            Get a repository's info
    forks              Return a repository's forks
    releases           Return a repository's releases
    languages          Return a repository's languages
    stargazers         Return a repository's stargazers
    pathcontents       List contents in a path of a repository''')
             
        
    def logsCommand():
        print(f'''
{Color.white}Logs subcommands{Color.reset}
{'='*17}
{Help.usageText.format('logs:<subcommand>')}

    {Color.white}Command            Description{Color.reset}
    -------            -----------
    view               View logs
    read               Read log
    delete             Delete log''')
                
            
    def helpCommand():      
        print(f'''
{Color.white}Core commands{Color.reset}
{'='*13}

    {Color.white}Command               Description{Color.reset}
    -------               -----------
    help                  Help menu
    exit                  Close session
    clear                 Clear screen
    about                 Program's info
    author                Developer's info
    version               Version info
 
       
{Color.white}Help subcommands{Color.reset}
{'='*16}
{Help.usageText.format('help:<subcommand>')}

    {Color.white}Command               Description{Color.reset}
    -------               -----------
    logs                  List all logs management commands
    repo                  List all repository investigation commands
    user                  List all users investigation commands
    search                List all target discovery commands
    update                List all program updates managememt commands''')
