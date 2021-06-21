
- [h5 问题总结-HTML 篇](#h5-问题总结-html-篇)
    - [刘海屏适配](#刘海屏适配)
    - [禁止页面缩放](#禁止页面缩放)
    - [禁止自动识别电话/邮箱](#禁止自动识别电话邮箱)
    - [禁止页面缓存](#禁止页面缓存)
    - [禁止字母大写](#禁止字母大写)
    - [弹出数字键盘](#弹出数字键盘)
    - [调用系统功能（电话/短信/邮件/相册/文件）](#调用系统功能电话短信邮件相册文件)
    - [唤起原生应用 - 通过自定义 scheme（约定的一种 URL 格式）](#唤起原生应用---通过自定义-scheme约定的一种-url-格式)
    - [Safari 特有配置](#safari-特有配置)
    - [其他浏览器特有配置 - qq/uc/360 浏览器](#其他浏览器特有配置---qquc360-浏览器)

# h5 问题总结-HTML 篇

### 刘海屏适配

- ios 适配

```html
<!-- 设置网页在可视窗口的布局方式 -->
<meta name="viewport" content="width=device-width, viewport-fit=cover" />
```

```css
/* 页面主体内容限制在安全区域内 */
@supports (bottom: constant(safe-area-inset-bottom)) or
  (bottom: env(safe-area-inset-bottom)) {
  .page {
    /* ios < 11.2 */
    padding-left: constant(safe-area-inset-left);
    padding-top: constant(safe-area-inset-top);
    padding-right: constant(safe-area-inset-right);
    padding-bottom: constant(safe-area-inset-bottom);
    /* ios >= 11.2 */
    padding-left: env(safe-area-inset-left);
    padding-top: env(safe-area-inset-top);
    padding-right: env(safe-area-inset-right);
    padding-bottom: env(safe-area-inset-bottom);
  }
}
```

- android 适配

没有统一的适配方案，`建议客户端暴露方法获取刘海的高度`，如果客户端不支持，则可设置为 28px，此高度可适配大多数安卓刘海屏。

```
.page.android {
  padding-top: 28px;
}

```

### 禁止页面缩放

```
<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1, minimum-scale=1, maximum-scale=1">

```

### 禁止自动识别电话/邮箱

```
<!-- 忽略自动识别电话 -->
<meta name="format-detection" content="telephone=no">

<!-- 忽略自动识别邮箱 -->
<meta name="format-detection" content="email=no">

<!-- 忽略自动识别电话和邮箱 -->
<meta name="format-detection" content="telephone=no, email=no">

```

### 禁止页面缓存

```
<meta http-equiv="Cache-Control" content="no-cache">

```

### 禁止字母大写

```
<input autocapitalize="off" autocorrect="off">

```

### 弹出数字键盘

```
<!-- 纯数字带#和* -->
<input type="tel">

<!-- 纯数字 -->
<input type="number" pattern="\d*">
```

### 调用系统功能（电话/短信/邮件/相册/文件）

```
<!-- 拨打电话 -->
<a href="tel:10086">拨打电话给10086</a>

<!-- 发送短信 -->
<a href="sms:10086">发送短信给10086</a>

<!-- 发送邮件 -->
<a href="mailto:test@test.com">发送邮件给test</a>

<!-- 选择照片或拍摄照片 -->
<input type="file" accept="image/*">

<!-- 选择视频或拍摄视频 -->
<input type="file" accept="video/*">

<!-- 多选文件 -->
<input type="file" multiple>

```

### 唤起原生应用 - 通过自定义 scheme（约定的一种 URL 格式）

```
<!-- 打开微信 -->
<a href="weixin://">打开微信</a>

<!-- 打开支付宝 -->
<a href="alipays://">打开支付宝</a>

<!-- 打开支付宝的扫一扫 -->
<a href="alipays://platformapi/startapp?saId=10000007">打开支付宝的扫一扫</a>

<!-- 打开支付宝的蚂蚁森林 -->
<a href="alipays://platformapi/startapp?appId=60000002">打开支付宝的蚂蚁森林</a>

```

### Safari 特有配置

```
<!-- 设置Safari全屏，在iOS7+无效 -->
<meta name="apple-mobile-web-app-capable" content="yes">

<!-- 改变Safari状态栏样式，可选default/black/black-translucent，需在上述全屏模式下才有效 -->
<meta name="apple-mobile-web-app-status-bar-style" content="black">

<!-- 添加页面启动占位图 -->
<link rel="apple-touch-startup-image" href="pig.jpg" media="(device-width: 375px)">

<!-- 保存网站到桌面时添加图标 -->
<link rel="apple-touch-icon" sizes="76x76" href="pig.jpg">

<!-- 保存网站到桌面时添加图标且清除默认光泽 -->
<link rel="apple-touch-icon-precomposed" href="pig.jpg">

```

### 其他浏览器特有配置 - qq/uc/360 浏览器

```
<!-- 强制QQ浏览器竖屏 -->
<meta name="x5-orientation" content="portrait">

<!-- 强制QQ浏览器全屏 -->
<meta name="x5-fullscreen" content="true">

<!-- 开启QQ浏览器应用模式 -->
<meta name="x5-page-mode" content="app">

<!-- 强制UC浏览器竖屏 -->
<meta name="screen-orientation" content="portrait">

<!-- 强制UC浏览器全屏 -->
<meta name="full-screen" content="yes">

<!-- 开启UC浏览器应用模式 -->
<meta name="browsermode" content="application">

<!-- 开启360浏览器极速模式 -->
<meta name="renderer" content="webkit">

```