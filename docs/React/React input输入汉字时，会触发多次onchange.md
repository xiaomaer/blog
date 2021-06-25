# React input输入汉字时，会触发多次onchange

## 问题
在开发react组件时，input绑定onChange事件，当输入中文时，每输入一个拼音都会触发一次onChange事件，导致搜索不符合预期。

## 原因
* React 中，onChagne 事件是一个合成事件，由 ChangeEventPlugin 插件处理其监听。
* ChangeEventPlugin 插件会处理三类元素，select 和 file 监听 change 事件，input 和 textarea 监听 input 和 change 事件，checkbox 和 radio 监听 click 事件。
* 所以输入中文时，每输入一个拼音字母，就会触发onChange事件

## 解决方法
使用 `compositionEvent` 事件，即：
* 监听输入法开始输入（compositionstart）和结束输入（compositionend）事件，通过状态记录输入是否完成，如果输入完成，触发onChange事件，否则不触发onChange事件
* 由于在不同浏览器，事件执行顺序有所不同，所以针对先执行onChange后执行compositionend事件的浏览器，需要在compositionend事件中再次触发onChange事件。事件执行顺序如下：
  ```
    有的浏览器执行顺序（webkit内核浏览器）：compositionstart onChange compositionend
    有的浏览器执行顺序（火狐浏览器等）：compositionstart compositionend onChange
  ```

最终代码如下：

```
import React, { useCallback, useRef, useEffect } from 'react';

export const Input = ({ value, onChange }) => {
    const inputRef = useRef<HTMLInputElement | null>(null);
    const isOnCompositionRef = useRef(false);
    const onchangeRef = useRef(false);

    useEffect(() => {
        // 受控使用时，要这样赋值
        if (inputRef.current) {
            inputRef.current.value = value || '';
        }
    }, [value]);

    const handleChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            onchangeRef.current = true;
            if (!isOnCompositionRef.current) {
                const val = e.target.value as string;
                onChange && onChange(val);
                onchangeRef.current = false;
            }
        },
        [onChange],
    );

    const handleComposition = useCallback(
        (e) => {
            if (e.type === 'compositionend') {
                isOnCompositionRef.current = false;
                // 有的浏览器执行顺序（webkit内核浏览器）：compositionstart onChange compositionend
                // 有的浏览器执行顺序（火狐浏览器）：compositionstart compositionend onChange
                if (onchangeRef.current) {
                    handleChange(e);
                }
                return;
            }

            isOnCompositionRef.current = true;
        },
        [handleChange],
    );

    return (
        <input 
            // 这样赋值输入框将会不能输入内容
            // value={value}
            onChange={handleChange}
            ref={inputRef}
            onCompositionStart={handleComposition}
            onCompositionUpdate={handleComposition}
            onCompositionEnd={handleComposition}
        />
    )
}
```


## CompositionEvent 事件介绍
DOM 接口 CompositionEvent 表示用户间接输入文本（如使用输入法）时发生的事件。此接口的常用事件有compositionstart, compositionupdate 和 compositionend。[点击这里](https://developer.mozilla.org/zh-CN/docs/Web/API/CompositionEvent)查看详情。

* **compositionstart**：当用户使用输入法如拼音输入汉字时，这个事件就会被触发（即在用户开始非直接输入的时候触发，在非直接输入的时候结束，整个过程`只触发了一次`）。
* **compositionupdate**：事件触发于字符被输入到一段文字的时候（如在用户开始输入拼音到确定结束的过程都会触发该事件）。
* **compositionend**：当文本段落的组成完成或取消时, compositionend 事件将被触发（如用户点击拼音输入法选词确定后，则触发了该事件，此时是直接输入了，整个过程只触发了一次）。

可以知道这三个事件就把我们输入中文拼音的三个过程进行了拆分。
