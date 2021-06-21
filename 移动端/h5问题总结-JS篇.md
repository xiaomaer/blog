
- [h5 问题总结-JavaScript 篇](#h5-问题总结-javascript-篇)
  - [左右滑动时，禁止上下滚动](#左右滑动时禁止上下滚动)
  - [禁止滚动穿透](#禁止滚动穿透)
  - [禁止点击穿透](#禁止点击穿透)
  - [日期解析](#日期解析)
  - [简化回到顶部](#简化回到顶部)
  - [简化上拉加载更多](#简化上拉加载更多)
  - [修复输入监听](#修复输入监听)
  - [修复输入框失焦后页面未回弹](#修复输入框失焦后页面未回弹)

# h5 问题总结-JavaScript 篇

## 左右滑动时，禁止上下滚动

- 问题描述：页面出现滚动条，左右滑动切换卡片时，会出现上下滑动，导致页面乱跑
- 解决方案：阻止默认行为（touchmove 事件的默认行为是 scroll事件），即记录滑动方向，如果开始滑动方向为横向，阻止默认行为，代码如下：

```
  <div
        ref={contenRef}
        style={contentStyle}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}>
      内容区域
      </div>

const handleTouchMove = useCallback((e: TouchEvent) => {
    if (!dragRef.current) {
      return;
    }
    if (e.touches.length > 1) {
      return;
    }
    const touch = e.touches[0];
    const diffY = touch.pageY - pageY.current;
    let diffX = touch.pageX - pageX.current;
    if (!directionRef.current) {
      directionRef.current = Math.abs(diffX) > Math.abs(diffY) ? 'horizontal' : 'vertical';
    }
    if (directionRef.current === 'horizontal') {
      if (e.cancelable) {
        e.preventDefault();
      }
      // 阻止默认行为
      e.preventDefault();
    }
  }, []);

  const handleTouchStart = useCallback(
    (e: React.TouchEvent<HTMLDivElement>) => {
      contenRef.current!.addEventListener('touchmove', handleTouchMove, { passive: false });
      const touch = e.touches[0];
      pageX.current = touch.pageX;
      pageY.current = touch.pageY;
      directionRef.current = '';
      dragRef.current = true;
    },
    [handleTouchMove],
  );

  const handleTouchEnd = useCallback(
    (e: React.TouchEvent) => {
      dragRef.current = false;
      directionRef.current = '';
      contenRef.current!.removeEventListener('touchmove', handleTouchMove, false);
    },
    [handleTouchMove],
  );
```

## 禁止滚动穿透

- 问题描述：页面内容可滚动且有弹窗时，当在弹窗上滚动时，会导致页面内容也跟着滚动
- 方案 1：当打开弹窗时，获取 scrollTop，并给 body 设置`position:fixed;`和动态 top 为`-${scrollTop}px`；当关闭弹窗时，移除设置的样式

```
body.fixed {
    position: fixed;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

const clsName="fixed";
const body = document.body;
const openBtn = document.getElementById("open-btn"); // 打开弹窗
const closeBtn = document.getElementById("close-btn"); // 关闭弹窗
openBtn.addEventListener("click", e => {
    e.stopPropagation();
    const scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
    body.classList.add(clsName);
    body.style.top = `-${scrollTop}px`;
});
closeBtn.addEventListener("click", e => {
    e.stopPropagation();
    body.classList.remove(clsName);
    body.scrollTop = document.documentElement.scrollTop = -parseInt(body.style.top);
    body.style.top = '';
});


```

- 方案 2:阻止 touchmove 事件默认行为【待验证】

- 结果：除了弹窗内容能点击或滚动，其他内容都不能点击或滚动

## 禁止点击穿透

- 问题描述：移动端点击后，为了确认是否是双击事件，会有 300ms 延迟，该点击延迟被称为点击穿透。
- 解决方案：使用 touch 事件、使用 fastclick npm 包

## 日期解析

- 问题描述：在苹果系统上解析 YYYY-MM-DD HH:mm:ss 这种日期格式会报错 Invalid Date，但在安卓系统上解析这种日期格式完全无问题。
- 解决方案：Android 和 iOS 通用日期格式为：YYYY/MM/DD HH:mm:ss

```
const date = "2019-03-31 21:30:00";
new Date(date.replace(/\-/g, "/"));
```

## 简化回到顶部

使用 scrollIntoView API。

```
const toTop = document.getElementById("toTop");
toTop.addEventListener("click", () => document.body.scrollIntoView({ behavior: "smooth" }));

```

## 简化上拉加载更多

使用 IntersectionObserver 监听目标元素与祖先元素的关系，即监听目标元素是否进入或者离开了指定父元素的内部

```
let list = document.querySelectorAll("ul li");

let observer = new IntersectionObserver(entries => {
  entries.forEach(item => {
    if (item.isIntersecting) {
      item.target.classList.add("show"); // 增加show类名
      observer.unobserve(item.target); // 移除监听
    }
  });
});

list.forEach(item => observer.observe(item));
```

## 修复输入监听

在苹果系统上的输入框输入文本，keyup/keydown/keypress 事件可能会无效。当输入框监听 keyup 事件时，逐个输入英文和数字会有效，但逐个输入中文不会有效，需按回车键才会有效。

此时`可用 input 事件`代替输入框的 keyup/keydown/keypress 事件。

## 修复输入框失焦后页面未回弹

问题描述：当页面同时出现以下三个条件时，键盘占位会把页面高度压缩一部分。 当输入完成键盘占位消失后，页面高度有可能回不到原来高度，产生坍塌导致 Webview 底色露脸。包括：

- 页面高度过小
- 输入框在页面底部或视窗中下方
- 输入框聚焦输入文本

解决方案：获取焦点时，获取 scrollTop，失去焦点时，根据获取的 scrollTop，回复 scrollTop。

```
const input = document.getElementById("input");
let scrollTop = 0;
input.addEventListener("focus", () => {
    scrollTop = document.scrollingElement.scrollTop;
});
input.addEventListener("blur", () => {
    document.scrollingElement.scrollTo(0, this.scrollTop);
});

```
