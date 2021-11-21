# position:sticky为什么失效了呢？
使用position:sticky很容易实现滚动吸顶的效果，但是我们在使用时发现经常会失效，为什么呢？

## 失效场景1：sticky元素的父级（或祖先级）元素设置了overflow:visible以外的属性值
* 原因：父级（或祖先级）元素设置了overflow:visible以外的属性值，滚动容器发生了变化
* 代码示例
  ```
      /* 会导致sticky效果失效 */
     .parentcontainer {
       overflow: auto; 
      }
       // or
      .container {
        overflow: auto;
      }
  ```

  ```
  <div class="parentcontainer">
        <div class="container">
          <div class="header">header1</div>
          <div class="content">
            content1我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
        </div>
      </div>

  ```

## 失效场景2：sticky元素的高度跟其父元素的高度一致
* 原因：如果父元素的高度和粘性定位元素一样，将会导致粘性约束矩形的高度也是和粘性定位元素一样高，粘性定位元素的已经完全没有了实现粘性效果的空间。[点击这里](https://www.zhangxinxu.com/wordpress/2020/03/position-sticky-rules/)学习更多
* 代码示例
  ```
    body{
        height: 1000px;
      }
      .testheight {
        height: 100px;
        background-color: gainsboro;
      }
      .testcontent {
        position: sticky;
        top: 0px;
        background: lightskyblue;
      }
  ```
  ```
    <body>
      <div style="height: 50px"></div>
      <div class="testheight">
         <!-- 去掉testheight类，可以看看与父元素高度不同的效果 -->
        <div class="testheight testcontent">内容</div>
      </div>
    </body>

  ```

## 其他特点：
* 同一个父容器中的sticky元素，如果定位值相等，则会重叠。示例代码如下：
  ```
   .header {
        position: sticky;
        top: 0px;
        padding: 10px 0;
        text-align: center;
        background-color: red;
      }
      .content {
        padding: 5px;
        height: 350px;
        background: gainsboro;
      }

  <body>
    <div class="container">
          <div class="header">header1</div>
          <div class="content">
            content1我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
          <div class="header">header2</div>
          <div class="content">
            content2我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
          <div class="header">header3</div>
          <div class="content">
            content3我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
          <div class="header">header4</div>
          <div class="content">
            content4我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
          <div class="header">header5</div>
          <div class="content">
            content5我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
      </div>
   </body>   
  ```
* 如果不同sticky元素属于不同父元素（即加上了`section`标签后），且这些父元素正好紧密相连，则会挤开原来的元素，形成依次占位的效果。示例代码如下：
  ```
   .header {
        position: sticky;
        top: 0px;
        padding: 10px 0;
        text-align: center;
        background-color: red;
      }
      .content {
        padding: 5px;
        height: 350px;
        background: gainsboro;
      }

  <body>
    <div class="container">
        <section>
          <div class="header">header1</div>
          <div class="content">
            content1我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
        </section>
        <section>
          <div class="header">header2</div>
          <div class="content">
            content2我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
        </section>
        <section>
          <div class="header">header3</div>
          <div class="content">
            content3我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
        </section>
        <section>
          <div class="header">header4</div>
          <div class="content">
            content4我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
        </section>
        <section>
          <div class="header">header5</div>
          <div class="content">
            content5我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容我是内容
          </div>
        </section>
      </div>
   </body>   
  ```