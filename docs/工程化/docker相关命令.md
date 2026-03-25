## docker构建镜像
docker build --build-arg APP_NAME=console -t console-app .

* 不使用缓存
docker build --no-cache --build-arg APP_NAME=console -t console-app .

## 查看生成的镜像
docker images | grep console-app

## 进入镜像内部查看文件
* 运行容器并进入 shell
docker run --rm -it console-app sh

* 或者如果镜像里没有 sh，尝试 bash
docker run --rm -it console-app /bin/bash

进入容器后，你可以使用 ls -a 查看文件结构。通常 Next.js 项目在 Dockerfile 中会被移动到 /app 或 /usr/src/app 目录下。

## 验证镜像是否能正常运行
* 启动容器
docker run -p 3000:3000 --name test-console console-app
参数解释：
    * -p 3000:3000：将你电脑（宿主机）的 3000 端口映射到容器内部的 3000 端口。
    * --name test-console：给这个运行中的容器起个名字，方便后续管理。
    * console-app：你刚才构建的镜像名称。
打开浏览器，输入 http://localhost:3000。如果能看到你的应用界面，说明构建产物完全没问题。

* 停止容器
docker stop test-console
* 启动已停止的容器
docker start test-console
* 删除容器	
docker rm -f test-console
* 查看正在运行的容器	
docker ps

## 删除生成的镜像
docker rmi console-app