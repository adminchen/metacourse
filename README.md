
## courera课程

### 安装courera

### 准备python环境

	brew install python
	sudo easy_install pip
	pip install -r requirements.txt

### 下载courera课程

例子：

	python coursera-dl.py -u username -p pasword socialpsychology-001


## railscast课程

### 准备clojure环境

	brew install clojure


### 下载railscast课程

#### 免费课程

	clj railscast-download.clj -rss your-rss-link -type media-format


`media-format`一般填写mp4

### 收费课程

将`your-rss-link`改为订阅后的rss网址。

## 下载TED课程

### 下载网址

* [Download TED talks with Chinese, Simplified subtitles](http://metated.petarmaric.com/download.zh-cn.html)

## 更新

批量更新下载脚本：

	git submodule foreach git pull && git pull

## 感谢

* [jplehmann/coursera](https://github.com/jplehmann/coursera)
* [bayan/railscast-downloader](https://github.com/bayan/railscast-downloader)


## Author

* zhiping (<http://yangzhiping.com>)