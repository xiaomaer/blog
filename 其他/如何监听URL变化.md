# 如何监听URL变化

## 形式
URL变化有两种形式：hash和html5 history api。如果通过改变hash值来实现，可以监听hashchange事件；如果通过html5 history API来改变URL，分成两种情况：
    * history.forward() 和 history.back()实现前进和后退时，可以监听popstate事件
    * history.pushState() 和 history.replaceState() 改变URL时，没有可以监听的原生事件，需要自定义实现

## 监听代码
```
const getFunc = function (type) {
  var historyFunc = history[type];
  return function () {
    const func = historyFunc.apply(this, arguments);
    // 自定义事件
    const e = new Event(type);
    e.arguments = arguments;
    window.dispatchEvent(e);
    return func;
  };
};

// 重新定义pushstate和replacestate方法
history.pushState = getFunc('pushState');
history.replaceState = getFunc('replaceState');

// 监听hash变化
window.addEventListener('hashchange', handleHashChange, false);
// 监听 history.forward() 和 history.back()改变URL
window.addEventListener('popstate', handlePopState, false);
// 监听 history.pushState()改变URL
window.addEventListener('pushState', handleStateChange, false);
// 监听 history.replaceState()改变URL
window.addEventListener('replaceState', handleStateChange, false);
    

```