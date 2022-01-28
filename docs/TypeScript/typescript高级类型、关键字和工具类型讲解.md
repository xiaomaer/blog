- [typescript高级类型、关键字和工具类型讲解](#typescript高级类型关键字和工具类型讲解)
  - [1、高级类型](#1高级类型)
    - [交叉类型（&）](#交叉类型)
    - [联合类型（|）](#联合类型)
  - [2、关键字](#2关键字)
    - [keyof](#keyof)
    - [typeof](#typeof)
    - [instanceof](#instanceof)
    - [in](#in)
    - [extends](#extends)
    - [is](#is)
    - [infer](#infer)
    - [索引访问操作符](#索引访问操作符)
  - [3、工具类型](#3工具类型)
    - [Partial<T>](#partialt)
    - [Required<T>](#requiredt)
    - [Readonly<T>](#readonlyt)
    - [ReadonlyArray<T>](#readonlyarrayt)
    - [Pick<T,K>](#picktk)
    - [Omit<T, K>](#omitt-k)
    - [Extract<T, U>](#extractt-u)
    - [Exclude<T, U>](#excludet-u)
    - [Record<K, T>](#recordk-t)
    - [NonNullable<T>](#nonnullablet)
    - [ConstructorParameters<typeof T>](#constructorparameterstypeof-t)
    - [InstanceType<T>](#instancetypet)
    - [ReturnType<T>](#returntypet)
    - [Parameters<T>](#parameterst)

# typescript高级类型、关键字和工具类型讲解
## 1、高级类型

### 交叉类型（&）
* 定义：将多种类型合并成一种类型，该类型包含了所有类型的所需属性
* 语法：`A&B`
* 用法:
  ```
  interface A{
    id:string;
    name:string;
    }

    interface B{
        sex:string;
        age:number;
    }

    // 等价于
    // type IntersectionType={
    //     id:string;
    //     name:string;
    //     sex:string;
    //     age:number;
    // }
    type IntersectionType = A & B;

    //缺少任何一个必须属性，编译都会报错 
    const result:IntersectionType={
        id:'1',
        name:'xiaoma',
        sex:'female',
        age:20
    }


    // error：
    // Type '{ id: string; name: string; sex: string; }' is not assignable to type 'IntersectionType'.
    //   Property 'age' is missing in type '{ id: string; name: string; sex: string; }' but required in type 'B'.
    const result2:IntersectionType={
        id:'1',
        name:'xiaoma',
        sex:'female',
    }
  ```
### 联合类型（|）
* 定义：可以赋值同一个变量不同的类型
* 语法：`A|B`
* 使用
  ```
  interface A{
    id:string;
    name:string;
    }

    interface B{
        sex:string;
        age:number;
    }

    // 等价于
    // type UnionType={
    //     id:string;
    //     name:string;
    //     sex?:string;
    //     age?:number;
    // }|{
    //     id?:string;
    //     name?:string;
    //     sex:string;
    //     age:number;
    // }
    type UnionType = A|B;


    let result:UnionType;

    result={
        id:'1',
        name:'xiaoma',
    }

    result={
        sex:'female',
        age:20
    }

    result={
        id:'1',
        name:'xiaoma',
        sex:'female',
        age:20
    }

    // error :
    // Type '{ id: string; name: string; sex: string; age: number; other: number; }' is not assignable to type 'UnionType'.
    //   Object literal may only specify known properties, and 'other' does not exist in type 'UnionType'.
    result={
        id:'1',
        name:'xiaoma',
        sex:'female',
        age:20,
        other:111
    }

  ```
## 2、关键字
### keyof
* 定义：获取该类型所有公共属性名构成的联合类型
* 语法：`keyof T`
* 使用：
  ```
  interface A{
    id:string;
    name:string;
    }

    // 等价于
    // type AProps='id'|'name'
    type AProps=keyof A

    let result:AProps;
    result='id';
    result='name';
    // error:Type '"ddd"' is not assignable to type 'keyof A'.
    result='ddd'
  ```
### typeof
* 定义：返回数据的类型定义
* 语法：`typeof T`
* 使用：
  ```
    const result1 = 1;
    const result2 = () => ({ id: '1', name: 'xiaoma' })
    const result3 = {
        id: '1',
        name: 'xiaoma',
        sex: 'female',
        age: 20
    }

    // true
    const isNumber = typeof result1 === 'number';
    // type Props1=1
    type Props1 = typeof result1;
    // type Props2=()=>{id:string,name:string}
    type Props2 = typeof result2;
    // type Props3={
    //     id:string;
    //     name:string;
    //     sex:string;
    //     age:number;
    // }
    type Props3 = typeof result3;

  ```

### instanceof 
* 定义：用于检测构造函数的 prototype 属性是否出现在某个实例对象的原型链上。
* 语法： `instance instanceof ClassType`
* 使用：
  ```
    class A {
        getName() {
            return 'xiaoma'
        }
    }

    class B {
        getSex() {
            return 'female'
        }
    }

    function getInfo(arg:A|B){
        // 判断实例所属原型
        if(arg instanceof A){
            console.log(arg.getName());
        }
        if(arg instanceof B){
            console.log(arg.getSex());
        }
    }

    // 输出xiaoma
    getInfo(new A());
    // 输出female
    getInfo(new B());
  ```
### in
* 定义：遍历指定接口的key或遍历联合类型
* 使用：
  ```
    interface A {
        id: string;
        name: string;
    }

    type MyReadonly<T> = {
        readonly [K in keyof T]: T[K]
    }

    // 等价于
    // type ReadonlyA = {
    //     readonly id: string;
    //     readonly name: string;
    // }
    type ReadonlyA = MyReadonly<A>
  ``` 
### extends
* 定义：不是类/接口的继承，是类型约束，用于判断一个类型(T)是否可以赋值给另一个类型(K)
* 语法：`T extends K`
* 使用
  ```
  interface A{
    id:string;
    name:string;
    }
  
    // T必须包含id和name属性
    function test<T extends A>(arg:T){
        console.log(arg.id);
    }

    const arg1={id:'1',name:'xiaoma'}
    test(arg1)

    const arg2={id:'1',name:'xiaoma',sex:'female'}
    test(arg2)

    const arg3={id:'1'}
    // error
    // Argument of type '{ id: string; }' is not assignable to parameter of type 'A'.
    //   Property 'name' is missing in type '{ id: string; }' but required in type 'A'.
    test(arg3)
  ```

### is
* 定义：判断函数参数是否为指定类型
* 语法：param is someType
* 使用
  ```
    function isString(test: any): test is string{
        return typeof test === "string";
    }

    function example(foo: any){
        if(isString(foo)){
            console.log("it is a string" + foo);
            console.log(foo.length); // string function
            // 编译时会报错：Property 'toExponential' does not exist on type 'string'.
            // 运行时会报错：foo.toExponential is not a function 
            // 因为 foo 是 string 不存在toExponential方法
            console.log(foo.toExponential(2));
        }
        // 编译不会出错，但是运行时出错
        console.log(foo.toExponential(2));
    }
    example("hello world");
  ```
* 与直接定义为`boolean`区别
    ```
        function isString(test: any): boolean{
            return typeof test === "string";
        }

        function example(foo: any){
            if(isString(foo)){
                console.log("it is a string" + foo);
                console.log(foo.length); // string function
                // foo 为 any，编译正常
                // 但是运行时会出错： foo.toExponential is not a function；因为 foo 是 string 不存在toExponential方法
                console.log(foo.toExponential(2));
            }
        }
        example("hello world");
    ```
### infer
* 定义：待推断类型，用于类型推断
* 语法：`infer P`
* 使用
  ```
    type FunctionType = (value: number) => boolean

    // 判断 T 是否能赋值给 (param: infer P) => any，并且将参数推断为泛型 P，如果可以赋值，则返回参数类型 P，否则返回传入的类型
    type ParamType<T> = T extends (param: infer P) => any ? P : T;

    type Param = ParamType<FunctionType>;   // type Param = number
    type OtherParam = ParamType<symbol>;   // type Param = symbol


    // 判断 T 是否能赋值给 (param: any) => infer U，并且将返回值类型推断为泛型 U，如果可以赋值，则返回返回值类型 U，否则返回传入的类型
    type ReturnValueType<T> = T extends (param: any) => infer U ? U : T;

    type Return = ReturnValueType<FunctionType>;   // type Return = boolean
    type OtherReturn = ReturnValueType<number>;   // type OtherReturn = number

  ```

### 索引访问操作符
* 定义：类似于js中获取对象属性值，而在ts中返回的是`T`对应属性`P`的类型
* 语法：`T[P]`
* 使用
  ```
  interface User {
    name: string
    age: number
    sex: 'male' | 'female';
    }

    type NameType = User['name']  // string
    type AgeType = User['age']  //  number
    type SexType = User['sex']  // 'male'|'female' 

  ```

## 3、工具类型
### Partial<T>
* 定义：将`T`类型的所有属性设置为可选
* 实现
  ```
  type Partial<T> = {
    [P in keyof T]?: T[P];
    }
  ```
* 使用
  ```
    interface User {
        name: string
        age: number
        sex: 'male' | 'female';
    }
    // 等价于
    // type PartialUser={
    //     name?: string
    //     age?: number
    //     sex?: 'male' | 'female';
    // }
    type PartialUser = Partial<User>
  ```

### Required<T>
* 定义：将`T`类型的所有属性设置为必选
* 实现：
  ```
  type Required<T> = {
    [P in keyof T]-?: T[P];
    }   
  ```
* 使用
  ```
  interface User {
    name: string
    age?: number
    sex?: 'male' | 'female';
    }
    // 等价于
    // type RequiredUser={
    //     name: string
    //     age: number
    //     sex: 'male' | 'female';
    // }
    type RequiredUser = Required<User>

  ```
### Readonly<T>
* 定义：将`T`类型的所有属性设置为可读状态
* 实现：
  ```
  type Readonly<T> = {
    readonly [P in keyof T]: T[P];
    }
  ```
* 使用：
  ```
  interface User {
    name: string
    age?: number
    sex?: 'male' | 'female';
    }
    // 等价于
    // type ReadonlyUser={
    //    readonly  name: string
    //    readonly age?: number
    //    readonly sex?: 'male' | 'female';
    // }
    type ReadonlyUser = Readonly<User>
  ```  
### ReadonlyArray<T>
* 定义：将`T`类型转换为只读状态`T[]`类型，只能在数组初始化时为变量赋值，之后数组无法修改
* 实现：
  ```
    interface ReadonlyArray<T> {
    /** Iterator of values in the array. */
    [Symbol.iterator](): IterableIterator<T>;

    /**
     * Returns an iterable of key, value pairs for every entry in the array
     */
    entries(): IterableIterator<[number, T]>;

    /**
     * Returns an iterable of keys in the array
     */
    keys(): IterableIterator<number>;

    /**
     * Returns an iterable of values in the array
     */
    values(): IterableIterator<T>;
    }
  ```
* 使用：
  ```
  interface User {
    name: string
    age?: number
    sex?: 'male' | 'female';
    }
    // 等价于
    // type ReadonlyUserArray= readonly User[]
    type ReadonlyUserArray = ReadonlyArray<User>

    // eg
    const personList: ReadonlyArray<User> = [{ name: 'Jack' }, { name: 'Rose' }]

    // 会报错：Property 'push' does not exist on type 'readonly Person[]'
    personList.push({ name: 'Lucy' })
  ```
### Pick<T,K>
* 定义：从`T`类型中提取部分属性`K`
* 实现：
  ```
  type Pick<T, K extends keyof T> = {
    [P in K]: T[P];
  }
  ```
* 使用
  ```
  interface User {
    name: string
    age?: number
    sex?: 'male' | 'female';
    }
    // 等价于
    // type PickUser= {
    //     name: string
    //     age?: number
    // }
    type PickUser = Pick<User,'name'|'age'>
  ```
### Omit<T, K>
* 定义：从`T`类型中排除部分属性`K`
* 实现：
  ```
  type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>
  
  or

  type Omit<T, K> = {
    [P in Exclude<keyof T, K>]: T[P];
  };

  ```
* 使用
  ```
  interface User {
    name: string
    age?: number
    sex?: 'male' | 'female';
    }
    // 等价于
    // type OmitUser= {
    //    sex?: 'male' | 'female';
    // }
    type OmitUser = Omit<User,'name'|'age'>

  ```
### Extract<T, U>
* 定义：取交集，提取`T`中可以赋值给`U`的类型
* 实现：
  ```
  type Extract<T, U> = T extends U ? T : never;
  ```
* 使用
  ```
  interface UserA {
    id:string;
    name: string
    age?: number
    sex?: 'male' | 'female';
  }

  interface UserB {
      id:string;
      name: string;
      address?:string;
  }


  //等价于 type ExtractUser= 'id'|'name'
  type ExtractUser = Extract<keyof UserA,keyof UserB>

  // 等价于 type ExtractProps1= "a" | "c"
  type ExtractProps1 = Extract<"a" | "b" | "c" | "d", "a" | "c" | "f">;  

  // 等价于 type ExtractProps2= () => void
  type ExtractProps2 = Extract<string | number | (() => void), Function>;  

  ```
### Exclude<T, U>
* 定义：提取`T`中剔除可以赋值给`U`的类型，即剔除共有属性
* 实现：
  ```
  type Exclude<T, U> = T extends U ? never : T
  ```
* 使用
  ```
  interface UserA {
    id:string;
    name: string
    age?: number
    sex?: 'male' | 'female';
  }

  interface UserB {
      id:string;
      name: string;
      address?:string;
  }


  // 等价于 type ExcludeUser= 'age'|'sex'
  type ExcludeUser = Exclude<keyof UserA,keyof UserB>

  // 等价于 type ExcludeProps1= 'b'|'d'
  type ExcludeProps1 = Exclude<"a" | "b" | "c" | "d", "a" | "c" | "f">; 


  // 等价于 type ExcludeProps2= 'string'|'number'
  type ExcludeProps2 = Exclude<string | number | (() => void), Function>;  
  ```
### Record<K, T>
* 定义：属性映射，即将一个类型`K`的属性映射到另一个类型`T`
* 实现
   ```
   type Record<K extends string | number | symbol, T> = {
    [P in K]: T;
  }
   ```
* 使用
  ```
  interface UserA {
    id: string;
    name: string;
    age?: number;
    sex?: 'male' | 'female';
  }

  interface UserB {
      id: string;
      name: string;
      address?: string;
  }


  // 等价于 
  // type RecordUser= {
  //     id: UserB;
  //     name: UserB;
  //     age: UserB;
  //     sex: UserB
  // }
  type RecordUser = Record<keyof UserA, UserB>
  ```

### NonNullable<T>
* 定义：不可为空类型，从 `T` 中剔除 `null` 和 `undefined`
* 实现：
  ```
  type NonNullable<T> = T extends null | undefined ? never : T
  ```
* 使用
  ```
  // 等价于 type NonNullable1= string | number
  type NonNullable1 = NonNullable<string | number | undefined>;

  //等价于 type NonNullable2= (() => string) | string[]
  type NonNullable2 = NonNullable<(() => string) | string[] | null | undefined>;

  // 等价于 type NonNullable3={name?: string, age: number} | string[]
  type NonNullable3 = NonNullable<{ name?: string, age: number } | string[] | null | undefined>;  
  ```
### ConstructorParameters<typeof T>
* 定义：构造函数参数类型，返回 class 中构造函数参数类型组成的`元组类型`
* 实现
  ```
  /**
  * Obtain the parameters of a constructor function type in a tuple
  */
  type ConstructorParameters<T extends new (...args: any) => any> = T extends new (...args: infer P) => any ? P : never;

  ```
* 使用
  ```
  class Person {
    name: string
    age: number
    gender: 'man' | 'women'

    constructor(name: string, age: number, gender: 'man' | 'women') {
        this.name = name
        this.age = age;
        this.gender = gender
    }
  }

  // 等价于 
  // type ConstructorType= [name: string, age: number, gender: "man" | "women"]
  type ConstructorType = ConstructorParameters<typeof Person>  

  const params: ConstructorType = ['Jack', 20, 'man']

  ```
### InstanceType<T>
* 定义：实例类型，获取 class 构造函数的返回类型
* 实现：
  ```
  /**
  * Obtain the return type of a constructor function type
  */
  type InstanceType<T extends new (...args: any) => any> = T extends new (...args: any) => infer R ? R : any;

  ```
* 使用：
  ```
  class Person {
    name: string
    age: number
    gender: 'man' | 'women'

    constructor(name: string, age: number, gender: 'man' | 'women') {
        this.name = name
        this.age = age;
        this.gender = gender
    }
  }

  // 等价于 type Instance=Person
  type Instance = InstanceType<typeof Person>

  const params: Instance = {
      name: 'Jack',
      age: 20,
      gender: 'man'
  }
  ```
### ReturnType<T>
* 定义：函数返回值类型，获取函数的返回值类型
* 实现：
  ```
  /**
  * Obtain the return type of a function type
  */
  type ReturnType<T extends (...args: any) => any> = T extends (...args: any) => infer R ? R : any;
  ```
* 使用：
  ```
  type FunctionType = (name: string, age: number) => boolean | string
  // 等价于 type FunctionReturnType =boolean | string
  type FunctionReturnType = ReturnType<FunctionType>
  ```
### Parameters<T>
* 定义：函数参数类型，获取函数的参数类型组成的`元组类型`
* 实现：
  ```
  /**
  * Obtain the parameters of a function type in a tuple
  */
  type Parameters<T extends (...args: any) => any> = T extends (...args: infer P) => any ? P : never;

  ```
* 使用：
  ```
    type FunctionType = (name: string, age: number) => boolean
    // 等价于 type FunctionParamsType=[name: string, age: number]
    type FunctionParamsType = Parameters<FunctionType>
  ```