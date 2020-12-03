from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
import bs4
import re

print('项目地址：https://github.com/TkzcM/pandownload-login/')


class AddHeader:
    def response(self, flow):
        print(flow.response.text)
        if "pan.baidu.com/disk/home" in flow.request.pretty_url:
            orig_body = flow.response.text
            parsed_body = bs4.BeautifulSoup(orig_body, features="html.parser")
            script = str(parsed_body)
            regex_token = ",\"bdstoken\":\"(\w{32})\""
            regex_name = "username\"\:\"(.+?)\""
            print(script)
            if re.search(regex_token, script) == None:
                regex_token = "locals\.set\(\'bdstoken\', \'(\w{32})\'"
                bdstoken = re.search(regex_token, script)
            else:
                bdstoken = re.search(regex_token, script)
            finalbds = bdstoken[1]
            body = '<script type=\"text/javascript\">\ntypeof initPrefetch === \'function\' && ' \
                   'initPrefetch(' \
                   '\'' + finalbds + '\', \'''\');\n</script>'
            flow.response.text = body
            flow.response.status_code = 200
            print('修改成功')


def start():
    myaddon = AddHeader()
    opts = options.Options(listen_host='127.0.0.1', listen_port=8888)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()


print('\n启动代理成功，请将 PanData/config.ini 中的 proxy 修改为下面显示的地址（已修改请忽略）')
start()
