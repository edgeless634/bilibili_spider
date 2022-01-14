# BilibiliSpider 一个简单的B站弹幕爬虫

```
 _____ _ _ _ _   _ _ _ _____     _   _         
| __  |_| |_| |_|_| |_|   __|___|_|_| |___ ___ 
| __ -| | | | . | | | |__   | . | | . | -_|  _|
|_____|_|_|_|___|_|_|_|_____|  _|_|___|___|_|  
                            |_|                
```

## BilibiliSpider

大学生做出来练手的B站弹幕爬虫，可以用来收集B站的弹幕作为语料

- 文档：没有（暂时）

- 支持版本：Python 3.6+

## 特点

- 可以从输入up的关注中自动提取出新的up作为抓取的目标

- 可以配合proxy_pool使用


## 运行

### 安装依赖

```
pip install -r requirement.txt
```

### 修改配置

配置在`setting/setting.yml`中，您看着改就行

### 启动

```
python biliSpider.py run
```

之后获取到的弹幕会放在`datafield/video_danmaku`中

## 项目结构

- biliSpider.py # 程序入口
- test.py # 测试脚本
- version.py # 版本信息
- datafield
  - up_mid # 需要抓取的up，本文件夹会根据输入自动扩充
    - xxx.txt 
  - video_danmaku # 抓取到的弹幕，文件命名格式为"{av号}.txt"
  - aid_done # 已经获取到的弹幕
  - mid_done # 已经获取到的up
- fetcher # 和网络交互的API
  - biliApi.py # B站的API
  - proxyFetcher.py # proxy_pool的API
- helper
  - fetch.py # 爬取B站的worker
  - launch # 启动worker
- setting
  - setting.yml # 配置文件
  - settingReader.py # 读取配置文件
- utils
  - bid.py # BV号和AV号互转
  - datafield.py # 处理datafield文件夹中的数据
  - randomsleep.py # 随机秒数的time.sleep
  - userAgent.py # 提供随机的userAgent






