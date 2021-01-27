# 创建 ref 的几种方式

- useRef：适用于函数组件
- React.createRef()：适用于类组件
- 回调函数：适用于函数/类组件

## useRef 方式

```
function TextInputWithFocusButton() {
  const inputEl = useRef(null);
  const onButtonClick = () => {
    // `current` 指向已挂载到 DOM 上的文本输入元素
    inputEl.current.focus();
  };
  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  );
}
```

## React.createRef()方式

```
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef();
  }
  render() {
    return <div ref={this.myRef} />;
  }
}
```

## 回调函数

```
class MyComponent extends React.Component {
  constructor(props) {
    super(props);
  }
  refCb(instance){
      console.log('实例',instance)
  }
  render() {
    return <div ref={refCb} />;
  }
}


function TextInputWithFocusButton() {

  const refCb = useCallback((instance) => {
     console.log('实例',instance)
  }, []);

  return <div ref={refCb} />;
}
```
