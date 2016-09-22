# encoding=utf-8
import json
import base64
import requests

"""
输入你的微博账号和密码，可去淘宝买，一元七个。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
	# {'no': 'jiadieyuso3319@163.com', 'psw': 'a123456'},
	{'no': 'shudieful3618@163.com', 'psw': 'a123456'},
	{'no': 'lizhanyang0110', 'psw': '8698331'},
	{'no': 'lizetian567@sina.com', 'psw': 'cqmyg123'},
	{'no': 'lizh1236', 'psw': '1309853'},
	{'no': 'lizhiwang171', 'psw': '5618626'},
	{'no': 'lizhongpei123', 'psw': 'lzp42098481'},
	{'no': 'lizhi280483650', 'psw': 'pd2880'},
	{'no': 'lizhi280483650', 'psw': 'pd2880'},
	{'no': 'lizhongxlj', 'psw': 'lizhong'},
	{'no': 'lizhenlz@sina.com', 'psw': '33850132'},
	{'no': 'lizqchina235', 'psw': '235888'},
	{'no': 'lj050530', 'psw': '19851008'},
	{'no': 'ljb1098', 'psw': 'puzzle'}
]


def getCookies(weibo):
	""" 获取Cookies """
	cookies = []
	loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
	for elem in weibo:
		account = elem['no']
		password = elem['psw']
		username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
		postData = {
			"entry": "sso",
			"gateway": "1",
			"from": "null",
			"savestate": "30",
			"useticket": "0",
			"pagerefer": "",
			"vsnf": "1",
			"su": username,
			"service": "sso",
			"sp": password,
			"sr": "1440*900",
			"encoding": "UTF-8",
			"cdult": "3",
			"domain": "sina.com.cn",
			"prelt": "0",
			"returntype": "TEXT",
		}
		session = requests.Session()
		r = session.post(loginURL, data=postData)
		jsonStr = r.content.decode('gbk')
		info = json.loads(jsonStr)
		if info["retcode"] == "0":
			print "Get Cookie Success!( Account:%s )" % account
			cookie = session.cookies.get_dict()
			cookies.append(cookie)
		else:
			print "Failed!( Reason:%s )" % info['reason']
	return cookies


cookies = getCookies(myWeiBo)
print "Get Cookies Finish!( Num:%d)" % len(cookies)
