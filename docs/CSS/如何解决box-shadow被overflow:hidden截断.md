# 如何解决box-shadow被overflow:hidden截断

## 场景
父容器设置了`overflow:hidden`，子元素设置了`box-shadow`，阴影显示效果不正常，被截断了。代码如下：
```
.container{
    position: fixed;
    top: 20px; 
    right: 0;
    left: 0;
    z-index: 2800;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
}
.content{
    align-items: flex-start;
    padding: 20px 0;
    background-color: #000;
    border-radius: 8px;
    box-shadow: 0px 10px 15px 0px rgba(0,0,0,0.1);
}

<div class="container">
    <div class="content"></div>
</div>
```

## 解决方案
给父容器增加`padding`，同时增加负 `margin`来消耗掉`padding`增加的空间，代码如下：
```
.container{
    // ...
    // 解决box-shadow阴影被overflow:hidden截断问题
     margin: 0 -50px -50px;
     padding: 0 50px 50px; 
}
```
