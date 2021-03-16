## Pi in Birthday

简略版，如有问题，请提Issue

利用[y-cruncher](http://www.numberworld.org/y-cruncher/)生成的txt文件，在`read_large_pi.py`中进行改名`fname = "pi_str.txt"`

### pi_str.txt

根据y-cruncher生成的小数据测试文件

### flask_server.py

微信后台服务

### create_pi_d.py

生成

- `pi_date.txt`: 易读易查
- `pi.json`：直接查表，空间换时间

### read_large_pi.py

查询（10位数1s以内，测试机器腾讯云1核2G机器），目前是存在一个小bug的，尚未修复

### pi_date.txt

根据create_pi_d.py生成的表

### pi.json

根据create_pi_d.py生成的json
