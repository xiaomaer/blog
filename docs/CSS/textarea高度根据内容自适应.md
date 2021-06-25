
# textarea高度根据内容自适应

## 问题
textarea可以通过rows或height设置高度，当内容超过rows或高度时，会出现滚动条，那么怎么实现高度根据内容自适应呢？

## 解决方案
* 方案1：css+js
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
* 方案2: 纯css
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
* 通过给元素设置contenteditable模拟
  ```
  <span 
  class="input" 
  role="textbox" 
  contenteditable>
    99
</span>
  ``` 