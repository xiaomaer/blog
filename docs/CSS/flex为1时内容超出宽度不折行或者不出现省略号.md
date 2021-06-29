# flex为1时内容超出宽度不折行或者不出现省略号
## 1、问题
使用flex进行左右布局，左边内容固定宽度，右边内容使用flex:1把宽度设置为剩余宽度。奇怪现象出现了，当右侧文字很长时，这时文字就会超出容器，而不是呆在设置好的动态剩余的空间中。代码如下：
```
<div class="main">
    <div class="left">左侧</div>
    <div class="right">右侧内容-很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长</div>
</div>

.main {
    display: flex;
}
.left {
    width: 100px;
    height: 100px;
    margin: 10px;
}
.right {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
```
## 2、原因
元素设置flex:1时，如果内容过长，其宽度会被内容撑开，并不会获取父容器剩余宽度（猜测flex:1优先级更高导致）

# 3、解决方法
* 给flex:1元素增加属性`width:0`
* 给flex:1元素增加属性`overflow:hidden`

以上解决方法原理，给元素设置了 flex 为 1 的时候，它会动态的获得父容器的剩余宽度，且不会被自己的子元素把内容撑开。
