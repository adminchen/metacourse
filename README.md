## 项目背景

这是一个收集批量下载优质课程方法的项目。目前已经添加了批量下载它们的方法：

* courera
* railscast
* TED

未来将补充完善其它优质课程的网站。当然，你也有更简单的应用办法，就是使用我已经解析之后的下载列表文件。放在`download`目录中。

## 用法

将本项目git clone到本地。

	git clone https://github.com/ouyangzhiping/metacourse.git
	cd metacourse

## courera课程

### 安装courera

### 准备python环境

	brew install python
	sudo easy_install pip
	pip install -r requirements.txt

### 下载courera课程

用法：

	cd courera
	python coursera-dl -u username -p password 课程编号 
	
如何查找课程编号？以网址为例： 

	https://class.coursera.org/sna-002/class/index 

这里面的sna-002就是课程编号。 username与password填入courera的登录邮箱与密码。

例子：

	python coursera-dl.py -u username -p pasword socialpsychology-001

### 注意事项

如果下载网速较慢，建议使用翻墙vpn。

## railscast课程

### 准备clojure环境

	brew install clojure


### 下载railscast课程

#### 免费课程

    cd railscast-downloader
	clj railscast-download.clj -rss your-rss-link -type media-format	


`media-format`一般填写mp4。例子：

	clj railscast-download.clj -rss http://feeds.feedburner.com/railscasts -type mp4
	
该免费网址需要翻墙。

### 收费课程

将`your-rss-link`改为订阅后的rss网址。

## 下载TED课程

### 每日更新的metalink文件

* [Download TED talks with Chinese, Simplified subtitles](http://metated.petarmaric.com/download.zh-cn.html)

### 解析后的下载列表

已经解析之后的下载地址列表文件：[TED_download.list](https://raw.github.com/ouyangzhiping/metacourse/master/download/TED_download.list)

将该文件下载下来，然后使用迅雷打开即可。

### 注意事项

* 有150g以上的硬盘闲置空间。
* 请务必使用离线与加速功能。这样，你可以享受到我已经加速过的部分视频，其它网友也可以享受到你带来的好处。
* 将这一千多个视频都保存在一个文件夹里面。

## 更新

批量更新下载脚本：

	git submodule foreach git pull && git pull

## 感谢

* [jplehmann/coursera](https://github.com/jplehmann/coursera)
* [bayan/railscast-downloader](https://github.com/bayan/railscast-downloader)
* [petar / metaTED — Bitbucket](https://bitbucket.org/petar/metated/)


## Author

* zhiping (<http://yangzhiping.com>)