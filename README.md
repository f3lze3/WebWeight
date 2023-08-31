# 免责声明

此工具仅供交流使用，请各位遵守《中华人民共和国网络安全法》以及相应地方的法律，禁止使用此工具进行违法操作，使用此工具造成的任何**直接**或**间接**的***后果***及***损失***，均由**使用者本人负责**。

## WebWeight

### 介绍

一个查询域名权重的便捷工具

### 使用

#### 安装依赖

> <span style="color:red">pip install -r requirements.txt</span>

#### 帮助

```python
Usage: python WebWeight.py -u <url/domain>

Options:
<<<<<<< HEAD
-h, --help 				show this help message and exit
=======
-h, --help 					show this help message and exit
>>>>>>> 9910aa8c92dea822e153bf89731cd927cd00654f
-u URL, --url=URL     				specify a url
-f FILE, --file=FILE  				specify a filename
-o OUTPUT, --output=OUTPUT			specify a csv filename to output (default csv)
```

#### 例子

1. 查询单域名权重

```python
python WebWeight.py -u example.com
```

```python
python WebWeight.py -u https://www.example.com
```

2. 批量查询域名权重

```python
python WebWeight.py -f urls.txt
```

```python
python WebWeight.py -f domains.txt -o result.csv
```
