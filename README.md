git学习笔记

* git init 初始化
* git add 文件名 添加文件
* git add -A 添加所有
* git commit -m "提交说明"
* git push -u origin master
* git status 查看状态
* git diff
* git log
* git log --pretty==oneline

>在Git中，用HEAD表示当前版本，也就是最新的提交3628164...882e1e0（注意我的提交ID和你的肯定不一样），上一个版本就是HEAD^，上上一个版本就是HEAD^^，当然往上100个版本写100个^比较容易数不过来，所以写成HEAD~100。

假设提交了四次，想回退到第三次提交
 git reset --hard HEAD^ 回退到
 
 接上一步操作想要再次从第三次提交回退到第四次提交

git reflog 查看第四次提交的 commit id然后

git reset --hard commit_id

* git checkout -- file 丢弃工作区的操作

* git reset HEAD file可以把暂存区的修改撤销掉（unstage），重新放回工作区：

* git clone 
* git clone 
