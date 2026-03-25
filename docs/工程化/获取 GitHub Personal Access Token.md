获取 GitHub Personal Access Token (PAT) 的过程其实非常直观，就像是在 GitHub 为你的第三方工具或代码仓库申请一张“通行证”。

目前 GitHub 主要推荐两种 Token：**Fine-grained tokens**（精细权限令牌，安全性更高，推荐使用）和 **Tokens (classic)**（经典令牌）。

以下是具体的操作步骤：

---

### 第一步：进入设置页面
1. 登录你的 [GitHub](https://github.com/) 账号。
2. 点击页面右上角的个人头像，选择 **Settings**（设置）。
3. 在左侧菜单栏拉到最底部，点击 **Developer settings**（开发者设置）。

### 第二步：选择 Token 类型
在左侧菜单中你会看到 **Personal access tokens**，点击展开后有两个选择：

#### 1. Fine-grained tokens (推荐)
这是目前最安全的做法，你可以限制 Token 只能访问特定的仓库。
* 点击 **Generate new token**。
* **Token name**: 给它起个名字（比如 "VSCode-Sync"）。
* **Expiration**: 设置有效期（建议不要选 "No expiration" 以保证安全）。
* **Repository access**: 选择它是能访问“所有仓库”还是“仅选中的仓库”。
* **Permissions**: 根据你的需求勾选权限（例如：读取代码权限选 `Contents`）。

#### 2. Tokens (classic)
如果你使用的某些旧插件或工具不支持精细权限，请选择这个。
* 点击 **Generate new token** -> **Generate new token (classic)**。
* **Note**: 备注用途。
* **Select scopes**: 勾选需要的权限。如果你是要在本地推送代码，通常勾选 `repo` 即可。



### 第三步：生成并保存
1. 点击底部的 **Generate token** 按钮。
2. **重要：** 页面会显示一串以 `github_pat_` 或 `ghp_` 开头的字符串。**请立即复制并保存到你的备忘录或密码管理器中。**
3. **注意：** 一旦你刷新或离开这个页面，你就再也看不到这串 Token 了！如果丢了，只能删掉重新生成一个。

---

### 如何使用这个 Token？
当你在终端（Terminal）执行 `git push` 或 `git clone` 被要求输入密码时，**不要输入你的 GitHub 登录密码**，而是粘贴这个 **Token**。

> **小贴士：** 为了安全，请永远不要把你的 Token 直接写在公共代码库的文件里，否则别人就能以此身份操作你的 GitHub。