
# textarea高度根据内容自适应

## 问题
textarea可以通过rows或height设置高度，当内容超过rows或高度时，会出现滚动条，那么怎么实现高度根据内容自适应呢？

## 解决方案

### 方案1：纯css
* 实现原理：给textarea包裹一层父容器，并在该容器中放入一个隐藏的div（visibility:hidden），并将textarea输入内容实时显示在div中，这样div把父容器高度撑开了。textarea绝对定位，height设置为100%，textarea高度即会跟着内容而变化。（div和textarea字体、边距等样式要保持一致，不然高度会不同步）
* 实现代码：
   ```
    const [value, setValue] = useState('');
    const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      setValue(e.target.value);
      onChange && onChange(e.target.value, e);
    },
    [onChange],
    );
    // ...
    <div className="container">
        <div className="simulate">{value}</div>
        <textarea
          ref={textareaRef}
          disabled={disabled}
          className="content"
          onChange={handleChange}
          value={value}></textarea>
      </div>
    // ...  
    .container {
      position: relative;
      width: 100%;
      overflow: hidden;
      min-height: 131px;
      max-height: 194px;
    }
    .simulate,
    .content {
      width: 100%;
      padding: 0;
      color: #333;
      white-space: pre-wrap;
      word-wrap: break-word;
      word-break: break-word;
      background-color: transparent;
      border: none;
      outline: none;
      -webkit-appearance: none;
      -webkit-tap-highlight-color: transparent;
      font-size:18px;
      line-height:22px;
    }
    .simulate {
      position: relative;
      visibility: hidden;
    }
    .content {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      overflow-x: hidden;
      overflow-y: scroll;
      resize: none;
      caret-color: green;
    }

   ```
### 方案2：css+js
* 实现原理：通过js检测文本的高度，然后动态设置文本框的高度。
* 实现思路：当出现滚动条的时候，文本的实际高度就是**scrollHeight**，我们只需要设置文本框的高度为内容的**scrollHeight**即可。
* 实现代码：
  ```
    <textarea oninput="auto_grow(this)"></textarea>

    textarea {
        resize: none;
        overflow: hidden;
        min-height: 50px;
        max-height: 100px;
    }

    function auto_grow(element) {
        element.style.height = "auto";
        element.style.height = (element.scrollHeight)+"px";
        }

  ```
### 方案3: 纯css
  ```
  <label class="input-sizer stacked">
    <span>Text: </span>
    <textarea oninput="this.parentNode.dataset.value = this.value" rows="1" placeholder="hi"></textarea>
  </label>

  HTML SCSS JSResult Skip Results Iframe

    *,
    *::before,
    *::after { 
        box-sizing: border-box;
    }

    .input-sizer {
        display: inline-grid;
        vertical-align: top;
        align-items: center;
        position: relative;
        border: solid 1px;
        padding: .25em .5em;
        margin: 5px;
    
        &.stacked {
            padding: .5em;
            align-items: stretch;
            
            &::after,
            textarea {
                grid-area: 2 / 1;
            }
        }
    
        &::after,
        textarea {
            width: auto;
            min-width: 1em;
            grid-area: 1 / 2;
            font: inherit;
            padding: 0.25em;
            margin: 0;
            resize: none;
            background: none;
            appearance: none;
            border: none;
        }
    
        span {
            padding: 0.25em;
        }
    
        &::after {
            content: attr(data-value) ' ';
            visibility: hidden;
            white-space: pre-wrap;
        }
    
        &:focus-within {
            outline: solid 1px blue;
            box-shadow: 4px 4px 0px blue;
            
            > span { color: blue; }
            
            textarea:focus,
            input:focus {
            outline: none;
            }
        }
    }

    .input-sizer {
        box-shadow: 4px 4px 0px #000;
        > span {
            text-transform: uppercase;
            font-size: 0.8em;
            font-weight: bold;
            text-shadow: 2px 2px 0 rgba(0,0,0,.15);
        }
    }
  ```
### 方案4:通过给元素设置contenteditable模拟

  ```
    <span 
  class="input" 
  role="textbox" 
  contenteditable>
    99
</span>
  ``` 