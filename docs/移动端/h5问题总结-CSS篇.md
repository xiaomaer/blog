
- [h5 问题总结-CSS篇](#h5-问题总结-css篇)
  - [自适应布局](#自适应布局)
  - [1px 问题](#1px-问题)
  - [超过一行打点](#超过一行打点)
  - [超过多行打点](#超过多行打点)
  - [开启 GPU 渲染](#开启-gpu-渲染)
  - [使用滚动回弹](#使用滚动回弹)
  - [禁止滚动传播](#禁止滚动传播)
  - [禁止长按操作](#禁止长按操作)
  - [禁止文本高亮显示](#禁止文本高亮显示)
  - [禁止动画闪屏](#禁止动画闪屏)
  - [美化表单外观](#美化表单外观)
  - [自定义滚动条 - `::-webkit-scrollbar-*`](#自定义滚动条----webkit-scrollbar-)
  - [自定义输入占位 - `::-webkit-input-placeholder`](#自定义输入占位----webkit-input-placeholder)
  - [对齐输入占位](#对齐输入占位)
  - [对齐下拉选项](#对齐下拉选项)
  - [10px 字体](#10px-字体)
  - [不垂直居中问题](#不垂直居中问题)
  - [flex 布局最后子元素 margin-right 失效](#flex-布局最后子元素-margin-right-失效)
  - [滚动元素，在顶部下拉时，背景色断层问题](#滚动元素在顶部下拉时背景色断层问题)
  - [禁止页面上下拉动，露出背景](#禁止页面上下拉动露出背景)
  - [CSS改变input光标颜色](#css改变input光标颜色)
  - [ios click事件偶发失效](#ios-click事件偶发失效)

# h5 问题总结-CSS篇

## 自适应布局

- rem
- vh/vm
- 百分比

## 1px 问题

```
 .elem{
    position: relative;
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: #f0f0f0;
      transform: scaleY(0.5);
    }
  }
```

## 超过一行打点

```
@mixin overflow-ellipsis {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

```

## 超过多行打点

```
@mixin multiple-overflow-ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3; // 设置多行
    -webkit-box-orient: vertical;
}

```

## 开启 GPU 渲染

```
.elem {
    transform: translate3d(0, 0, 0);
    /* transform: translateZ(0); */
}
```

## 使用滚动回弹

解决 ios 上滚动卡顿的问题

```
.elem{
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
}
```
[了解-webkit-overflow-scrolling属性的坑](https://www.cnblogs.com/xiahj/p/8036419.html)

## 禁止滚动传播

当页面包含多个滚动区域时，滚完一个区域后若还存在滚动动量则会将这些剩余动量传播到下一个滚动区域，造成该区域也滚动起来。这种行为称为滚动传播。

```
.elem {
    overscroll-behavior: contain;
}

```

## 禁止长按操作

```
* {
    /* pointer-events: none; */ /* 微信浏览器还需附加该属性才有效 */
    user-select: none; /* 禁止长按选择文字 */
    -webkit-touch-callout: none;
}


```

## 禁止文本高亮显示

```
* {
    -webkit-tap-highlight-color: transparent;
}

```

## 禁止动画闪屏

```
.elem {
    perspective: 1000;
    backface-visibility: hidden;
    transform-style: preserve-3d; // 创建3D环境
}

```

## 美化表单外观

```
button,
input,
select,
textarea {
    appearance: none;
    /* 自定义样式 */
}
```

## 自定义滚动条 - `::-webkit-scrollbar-*`

- ::-webkit-scrollbar：滚动条整体部分
- ::-webkit-scrollbar-track：滚动条轨道部分
- ::-webkit-scrollbar-thumb：滚动条滑块部分

```
::-webkit-scrollbar {
    display:none
}
::-webkit-scrollbar-track {
    background-color: transparent;
}
::-webkit-scrollbar-thumb {
    border-radius: 3px;
    background-image: linear-gradient(135deg, #09f, #3c9);
}

```

## 自定义输入占位 - `::-webkit-input-placeholder`

```
input::-webkit-input-placeholder {
    color: #13c2c2;
}

```

## 对齐输入占位

```
input {
    line-height: normal;
}

```

## 对齐下拉选项

```
select option {
    direction: rtl; //下拉框选项默认向左对齐，修改为向右对齐
}

```

## 10px 字体

- 问题描述：默认情况下，浏览器是不支持 12px 以下字体的，如果设置 font-size 小于 12px，会显示为 12px 字体。
- 解决方案：先放大，然后再缩放，代码如下：

```
 .tag-text {
    font-size: 12px; // 放大
    transform: scale(0.83); // 缩小
  }
```

## 不垂直居中问题

- 问题描述：在有些 android 手机，指定高度或字体时，设置了 align-items:center 时，仍然不垂直居中。
- 解决方案：外面加一层元素包裹，设置为实际的高度，里面元素扩大一倍，然后再缩放，代码如下：

```
.button {
      width: 24px;
      height: 24px;
      overflow: hidden;
}
.button .today {
      display: flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
      width: 48px; // 重要
      height: 48px; // 重要
      color: #13c2c2;
      font-weight: bold;
      font-size: 28px;
      font-family: Montserrat-Medium, Montserrat;
      background: rgba(19, 194, 194, 0.1);
      background: themeColorAlpha('S6', 0.1);
      border: 2px solid rgba(19, 194, 194, 0.5); // 重要
      border-radius: 50%;
      transform: scale(0.5); // 重要
      transform-origin: left top; // 重要
    }

```

## flex 布局最后子元素 margin-right 失效

- 参考：[flex 布局最后子元素 margin-right 失效](../CSS/flex布局最后子元素margin-right失效.md)

## 滚动元素，在顶部下拉时，背景色断层问题

- 参考：[如何设置 div 背景色一半为蓝色一半为白色](../CSS/如何设置div背景色一半为蓝色一半为白色.md)

## 禁止页面上下拉动，露出背景
解决方案：给html设置`overflow: hidden;`

## CSS改变input光标颜色
* 使用color来实现
  
光标的颜色是继承自当前输入框字体的颜色，所以用 color 属性即可改变：
```
  input{
      color:red;
  }
```

* 使用caret-color来实现

上一种方式已经修改了光标的颜色但是字体的颜色也改变了，如果只想改变光标的颜色而不改变字体的颜色那就使用 caret-color 属性:
```
input{
    caret-color:red;
}
```
## ios click事件偶发失效
* 场景：通过增加绝对定位的div，实现按钮点按效果，代码如下：
    ```
    <button class="mobile-button" onclick="handleclick">
        <!-- 实现点按效果的标签 --> 
        <div class="mobile-button__highlight-overlay"></div>
        <!-- icon -->
        <div class="mobile-button__icon-container">icon</div>
        <!-- text -->
        <div class="mobile-button__children-container">text</div>
    </button>
    .mobile-button {
        // ...
        position:relative;
    }
    .mobile-button__highlight-overlay {
        position: absolute;
        z-index: 1;
        display: none;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.05);
        border-radius: 5px;
    }
    ```
* 操作：在ios上点击按钮，偶尔不触发click逻辑
* 问题：`.mobile-button__highlight-overlay`那层div阻碍了事件执行
* 解决：给`.mobile-button__highlight-overlay`增加以下属性，禁止该元素的鼠标事件
  ```
  .mobile-button__highlight-overlay {
    pointer-events: none !important;
    }
  ```