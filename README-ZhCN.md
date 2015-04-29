# Docker registry ufile driver

这是基于[UFile](http://www.ucloud.cn/product/ufile_main/)的[docker-registry](https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core)的存储适配.


[![License][license-image]][license-url]
[![PyPI version][pypi-image]][pypi-url]

[![Build Status][travis-image]][travis-url]
[![Coverage Status][coverage-image]][coverage-url]

## 目录

- [部署](#部署)
- [详细配置](#详细配置)
- [开发](#开发)


## 部署
### 准备
- 一台服务器, 以ubuntu14.04为例
- python2, 以ubuntu自带的python2为例 (docker-registry因为使用了gevent, 目前仅支持py2)

### 安装
#### virtualenv
virtualenv将不同的python环境隔离. 你可以在[这里](virtualenv-site)了解更多
```bash
sudo apt-get install python-virtualenv
virtualenv docker-registry
cd docker-registry
source ./bin/active
```
#### 安装docker-registry及ufile-driver
```
pip install docker-registry
pip install docker-registry-driver-ufile
```
#### 配置和运行
修改下方配置并存为`conf.yml`
> 具体配置请看[详细配置](#详细配置). **如果可能, 请使用内网url**
```yaml
ufile:
      <<: *common
      storage: ufile
      ufile_baseurl: http://your-bucket.ufile.ucloud.cn
      ufile_public_key: your-ucloud-public-key
      ufile_private_key: your-ucloud-private-key
      ufile_retries: 3
      ufile_retry_interval: 1
      ufile_timeout: 60
```

#### 运行docker-registry并指定运行环境和配置文件
```bash
export DOCKER_REGISTRY_CONFIG=`pwd`/config.yml
export SETTINGS_FLAVOR=ufile

docker-registry
```

#### 试着玩一下

> 默认的docker-registry监听localhost:5000
> 你只需要把某个image tag 成 localhost:5000/image-name:tag-name
> 然后push localhost:5000/image-name:tag-name 即可


## 详细配置

Driver目前有如下选项可供配置.

### ufile_baseurl
> ufile bucket地址(含有 `http://`), 例如:

> `http://your-bucket.ufile.ucloud.cn`

> 如果可能, 你应该总是使用内网url, 例如  `http://your-bucket.ufile.cn-north-03.ucloud.cn`


### ufile_public_key
> ucloud public key, 你可以从[控制台](app-key-url)获取


### ufile_private_key
> ucloud private key, 你可以从[控制台](app-key-url)获取


### ufile_retries
> 如果遇上网络错误, 在失败前重试的次数 (默认3次)


### ufile_retry_interval
> 如果遇上网络错误, 在重试前应等待多少秒 (默认1秒)


### ufile_timeout
> 网络超时 (默认60秒, 如果你只能使用外网的话, 请把这个值改大)


## 开发
#### fork后将代码clone到本地
#### 安装tox
```
pip install tox
```
#### 开始测试
```
tox
```

> tox将会安装测试依赖并运行单元测试及pep8测试.

> **在pull request前, 请确保你本地的tox运行结果都是正确的.**


## 开源许可证

本项目及[docker-registry][docker-registry-url]均采用 [Apache License][license-url].


[pypi-url]: https://pypi.python.org/pypi/docker-registry-driver-ufile
[pypi-image]:  https://img.shields.io/pypi/v/docker-registry-driver-ufile.svg?style=flat-square
[travis-url]: https://travis-ci.org/SkyLothar/docker-registry-driver-ufile
[travis-image]:https://img.shields.io/travis/SkyLothar/docker-registry-driver-ufile.svg?style=flat-square
[coverage-url]: https://coveralls.io/r/SkyLothar/docker-registry-driver-ufile
[coverage-image]: https://img.shields.io/coveralls/SkyLothar/docker-registry-driver-ufile.svg?style=flat-square
[license-url]: http://www.apache.org/licenses/LICENSE-2.0.html
[license-image]: https://img.shields.io/github/license/skylothar/docker-registry-driver-ufile.svg?style=flat-square
[app-key-url]: https://consolev3.ucloud.cn/apikey
[virtualenv-site]: https://virtualenv.pypa.io/en/latest/
[docker-registry-url]: https://github.com/docker/docker-registry
