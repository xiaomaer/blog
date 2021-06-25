# iphone设置css  :active伪类失效

## 问题
最近开发组件，需要处理组件点击态样式，该样式通过CSS的`:active`伪类设置，但是在iPhone部分浏览器却没有效果。代码如下：
```
.mobile-button:active {
      .mobile-button__highlight-overlay {
        display: block;
      }
}
```

## 原因
`By default, Safari Mobile does not use the :active state unless there is a touchstart event handler on the relevant element or on the <body>`(默认情况下，除非在该元素或body上绑定一个touchstart事件，否则浏览器不会展示:active样式)


## 解决方案
* 在iOS系统的移动设备中，需要在按钮元素或body/html上绑定一个touchstart事件才能激活:active状态。
```
document.body.addEventListener('touchstart', function (){});
```
* 要让css的:active伪类生效，只需要给这个元素的touchstart/touchend绑定一个空的匿名方法即可成功。
```
button {
     -webkit-tap-highlight-color: rgba(0,0,0,0);
}

<button onTouchStart={()=>{}}></button>
````