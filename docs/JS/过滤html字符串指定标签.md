# 过滤html字符串指定标签

## 场景
* 从html字符串中，获取指定标签个数
* 从html字符串中，过滤掉指定标签
* 从html字符串中，过滤掉所有标签，只剩下内容

## 实现
### 从html字符串中，找到指定标签个数
```
function getLabelsCount(htmlStr, filterLabels = []) {
        let labelCountMap = {};
        filterLabels.forEach((item) => {
          const reg = new RegExp(`<${item}[^a-zA-Z]`, 'ig');
          const count = (htmlStr.match(reg) || []).length;
          labelCountMap[item.toLowerCase()] = count;
        });
        return labelCountMap;
      }
```
### 从html字符串中，过滤掉指定标签
```
 function filteSomeLabels(htmlStr, filterLabels = []) {
        let fitlerContent = htmlStr;
        // 找到指定标签个数，并从内容中过滤掉
        filterLabels.forEach((item) => {
          const filterReg = new RegExp(
            `<${item}\\s*[^>]*>(.*?)<\/${item}>`,
            'ig'
          );
          fitlerContent = fitlerContent.replace(filterReg, '$1');
        });
        return fitlerContent;
      }
```

### 从html字符串中，过滤掉所有标签，只剩下内容
```
function filterAllLabels(htmlStr) {
        return htmlStr.replace(/<\/?.+?>/g, '');
      }
```