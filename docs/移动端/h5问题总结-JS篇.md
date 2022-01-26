
- [h5 问题总结-JavaScript 篇](#h5-问题总结-javascript-篇)
  - [左右滑动时，禁止上下滚动](#左右滑动时禁止上下滚动)
  - [禁止滚动穿透](#禁止滚动穿透)
      - [问题描述](#问题描述)
      - [方案](#方案)
  - [禁止点击穿透](#禁止点击穿透)
  - [日期解析](#日期解析)
  - [简化回到顶部](#简化回到顶部)
  - [简化上拉加载更多](#简化上拉加载更多)
  - [修复输入监听](#修复输入监听)
  - [修复输入框失焦后页面未回弹](#修复输入框失焦后页面未回弹)
  - [如何监听键盘弹起呢？](#如何监听键盘弹起呢)
  - [ios中fixed为什么会失效呢？](#ios中fixed为什么会失效呢)

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

#### 问题描述
页面内容可滚动且有弹窗时，当在弹窗上滚动时，会导致页面内容也跟着滚动

#### 方案
- 方案 1：当打开弹窗时，设置body为`overflow:hidden;width:calc(100vw-0px);`，当关闭弹层时，移除样式（一定要通过内联样式上设置）
  ```
  // 解决弹层内容滚动穿透和滚动跳动问题（显示和隐藏输入URL地址栏）
    const body = document.body;
    if (visible) {
      // ! 必须是内联样式，如果使用添加类设置样式，会导致滚动位置丢失
      body.style.cssText += `width: calc(100vw - 0px); overflow: hidden;`;
    } else {
      body.style.width = '';
      body.style.overflow = '';
    }
  ```
- 方案 2：当打开弹窗时，获取 scrollTop，并给 body 设置`position:fixed;`和动态 top 为`-${scrollTop}px`；当关闭弹窗时，移除设置的样式，恢复scrollTop
  - 问题：关闭弹层时，页面会抖动（页面dom节点很多时）
  - 相关代码
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

- 方案 3:阻止 touchmove 事件默认行为（其默认行为为滚动事件）

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

## 如何监听键盘弹起呢？
* ios中，输入框（input、textarea 或 富文本）获取焦点，键盘弹起，但页面高度不会发生变化，只是页面整体往上滚了，且最大滚动高度（scrollTop）为软键盘高度；失去焦点，键盘收起。所以监听是否获取或失去焦点，代码如下：
  ```
  // IOS 键盘弹起：当输入框被聚焦时IOS键盘会被弹起
    inputRef?.current?.addEventListener('focus', function () {
      // IOS 键盘弹起后操作
    }, false)

    // IOS 键盘收起：当点击输入框以外区域或点击收起按钮，IOS输入框都会失去焦点，键盘会收起，
    inputRef?.current?.addEventListener('blur', () => {
      // IOS 键盘收起后操作
    })
  ```
* 在android上，输入框获取焦点，键盘弹起，但是页面高度会发生改变，一般来说，高度为可视区高度（原高度减去软键盘高度）；输入框失去焦点，软键盘收起。但是，触发键盘上的收起按钮键盘时，输入框并不会失去焦点，同样软键盘收起。所以监听高度的变化，代码如下：
  ```
  useEffect(() => {
      const { isAndroid } = Util.getOS('');
      let originHeight = document.documentElement.clientHeight || document.body.clientHeight;
      const handelAndroidResize = throttle(() => {
          const resizeHeight =
              document.documentElement.clientHeight || document.body.clientHeight;
          if (originHeight < resizeHeight) {
              // Android 键盘收起后操作
          } else {
              // Android 键盘弹起后操作
          }
          originHeight = resizeHeight;
      }, 300);

      if (isAndroid) {
          window.addEventListener('resize', handelAndroidResize, false);
      }

      return () => {
          if (isAndroid) {
              window.removeEventListener('resize', handelAndroidResize, false);
          }
      };
    }, []);
  ```


## ios中fixed为什么会失效呢？
* 现象：ios中，移动端页面顶部和底部元素fixed时，中间显示内容和输入框，当输入框获取焦点时，顶部被推到可视区域之外（即fixed定位的顶部显示异常）
* 原因：当时ios设计者考虑到一个问题：**当键盘弹起时，页面无法感知到键盘的存在。那么，如果将要输入的目标（即「输入框」，例如 input、textarea 或一般的 contenteditable 元素）正好被弹起的键盘遮住，体验不会很糟糕吗**？为了解决这个问题，**ios设计者们让webview上滚**，但滚动的结果有些出乎意料：输入框本身可以理解地滚动到了实际可视区域的正中间，但 fixed 元素不会发生重新计算，而是保持原来的相对位置，跟着输入框一起被上推；在滚动过程中，还会允许屏幕底部超出页面底部（「滚动过头」），以便让输入框尽可能露出来。收起键盘后，「滚动过头」的部分会被弹回，fixed 元素发生重新计算，但页面并不会回到与打开键盘前相同的位置。所以fixed定位失效了。
* 解决方案：暂时没有很好的解决方案（可以使用native提供的header）
* 相关参考文章：
  * [iOS 键盘难题与可见视口（VisualViewport）API](https://segmentfault.com/a/1190000021874101)
  * [移动端那些戳中你痛点的软键盘问题](https://mp.weixin.qq.com/s/X9vR9b_WJ409TAtT65Mwig)