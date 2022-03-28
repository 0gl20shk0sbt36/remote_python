# remote_python
### 中文名： 远程python

在电脑1运行server\SERVER.py将生成一个password.txt文件，将其储存至u盘，然后再其电脑2插入u盘并运行client\client.py即可在电脑2远程操控电脑1进行python交互式操作，或者将server\SERVER.py运行后输出的数据在client\client.py上输入即可。

目前可以实现：

1. python交互式的所有功能
2. 在电脑2可以让电脑1执行代码，也可以让电脑2执行代码
3. 电脑1和电脑2的变量可以互传
4. 错误用红字突出
5. 在电脑1调用print函数时输出到电脑2
6. 在电脑1调用input函数时由电脑2输入
