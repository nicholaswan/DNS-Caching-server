#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
import sys
from os import system as cmd

conf_dir = '/etc/'
url = 'https://o5obpsd7a.qnssl.com/'
dist = {		
		'Linux64bitcentos':[1,'pdnsd-1.2.9a-par_sl6.x86_64.rpm'],
		'Linux32bitcentos':[1,'pdnsd-1.2.9a-par_sl6.i686.rpm']
}

def get_platform_info():
	system_name = platform.system()
	system_bits = platform.architecture()[0]
	system_Release = platform.dist()[0]

	print system_name + system_bits + system_Release
	return system_name + system_bits + system_Release


def install_pdnsd():

	install_info = dist[get_platform_info()]
	if install_info[0] :
		cmd('wget %s%s'%(url,install_info[1]))
		cmd('yum localinstall %s -y'%install_info[1])
	else :
		print install_info[1]
def get_conf():
	cmd('wget https://raw.githubusercontent.com/zyqf/DNS-Caching-server/master/pdnsd.conf && mv -f pdnsd.conf %s'%conf_dir)
	cmd('wget https://raw.githubusercontent.com/zyqf/hosts/master/hosts && mv hosts /etc/hosts')
	cmd('service pdnsd start && chkconfig pdnsd on')

def add_cron():
	with open('./cron','w') as f:
		f.write('''0 1 * * * wget https://raw.githubusercontent.com/zyqf/hosts/master/hosts && mv -f hosts /etc/hosts
0 3 * * * service pdnsd restart
''')

	cmd('crontab ./cron')
	cmd('/sbin/service crond reload')
	cmd('/sbin/service crond restart')

if __name__ == '__main__':
	if sys.argv[1] == 'install':
		install_pdnsd()
		get_conf()
		add_cron()
	elif sys.argv[1] == 'set_dir':
		 conf_dir = sys.argv[2]
	elif sys.argv[1] == 'uninstall':
		cmd('yum remove pdnsd -y')
		cmd('rm -rf /etc/pdns.conf')
	else:
		print "Forget enter mode or your system isn't supported"

