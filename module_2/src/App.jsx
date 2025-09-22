import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function MyButtonHooked({handleClick, count}) {
  return (
  <button onClick={handleClick}>{count}</button>
);
}

function MyButton() {
  const [count, setCount] = useState(0);
  
  function handleClick() {
    setCount(count + 1)
    alert('You Clicked Me!')
  }
  return (
    <button onClick={handleClick}> I'm a button and the count is {count} </button>
  )
}
const products = [
  { title: 'Cabbage', isFruit: false, id: 1 },
  { title: 'Garlic', isFruit: false, id: 2 },
  { title: 'Apple', isFruit: true, id: 3 },
];

function ShoppingList() {
  const listItmes = products.map(product =>
    <li
      key={product.id}
      style={{
        color: product.isFruit ? 'magenta' : 'green'
      }}>
      {product.title}
    </li>
  )

  return <ul>{listItmes}</ul>;
}

export default function MyApp() {
  const [counter2, setCounter2] = useState(0)

  function funcHandleClick() {
    setCounter2(counter2 + 1)
  }
  
  return (
    <div>
      <h1>Welcome to my App</h1>
      <MyButton />
      <MyButton />
      <ShoppingList />
      <MyButtonHooked handleClick={funcHandleClick} count={counter2} />
      <MyButtonHooked handleClick={funcHandleClick} count={counter2} />
    </div>
  )
}