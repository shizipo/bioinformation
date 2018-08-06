#上传本地代码及更新代码到GitHub教程
##上传本地代码
第一步：去github上创建自己的Repository，获得创建仓库的https地址。

第二步：
	echo "# Test" >> README.md
第三步：建立git仓库
	git init
第四步：将项目的所有文件添加到仓库中
	git add .
第五步：
	git add README.md
第六步：提交到仓库
	git commit -m "注释语句"
第七步：将本地的仓库关联到GitHub，后面的https改成刚刚自己的地址，上面的红框处
	git remote add origin https://github.com/zlxzlxzlx/Test.git
第八步：上传github之前pull一下
	git pull origin master
第九步：上传代码到GitHub远程仓库
	git push -u origin master
中间可能会让你输入Username和Password，你只要输入github的账号和密码就行了。执行完后，如果没有异常，等待执行完就上传成功了。
##更新代码
第一步：查看当前的git仓库状态，可以使用git status
	git status
第二步：更新全部
	git add *
第三步：接着输入git commit -m "更新说明"
	git commit -m "更新说明"
第四步：先git pull,拉取当前分支最新代码
	git pull
第五步：push到远程master分支上
	git push origin master
不出意外，打开GitHub已经同步了

[原文链接] https://www.cnblogs.com/zlxbky/p/7727895.html 