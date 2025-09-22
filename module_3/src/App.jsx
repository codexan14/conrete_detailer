import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const PRODUCTS = [
  { category: "Fruits", price: "$1", stocked: true, name: "Apple" },
  { category: "Fruits", price: "$1", stocked: true, name: "Dragonfruit" },
  { category: "Fruits", price: "$2", stocked: false, name: "Passionfruit" },
  { category: "Vegetables", price: "$2", stocked: true, name: "Spinach" },
  { category: "Vegetables", price: "$4", stocked: false, name: "Pumpkin" },
  { category: "Vegetables", price: "$1", stocked: true, name: "Peas" }
]

function ProductCategoryRow({ category }) {
  return (
    <tr>
      <th colSpan="2">
        {category}
      </th>
    </tr>
  );
}

function ProductRow({ product }) {
  const name = product.stocked ? product.name :
    <span style={{ color: 'red' }}>
      {product.name}
    </span>;

  return (
    <tr>
      <td>{name}</td>
      <td>{product.price}</td>
    </tr>
  );
}

function ProductTable({ products }) {
  const rows = [];
  let lastCategory = null;

  products.forEach((product) => {
    if (product.category !== lastCategory) {
      rows.push(
        <ProductCategoryRow
          category={product.category}
          key={product.key} />
      );
    }

    rows.push(
      <ProductRow
        product={product}
        key={product.key}
      />
    ); 

    lastCategory = product.category;
  });

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  );
}

function SearchBar({
  filterText, 
  inStockOnly,
  onFilterTextChange,
  onInStockOnlyChange
}) {
  return (
    <form>
      <input 
        type='text' 
        placeholder='Search ... '
        value={filterText}
        onChange={(e) => onFilterTextChange(e.target.value)}></input>
      <label>
        <input 
        type='checkbox' 
        checked={inStockOnly}
        onChange={(e) => onInStockOnlyChange(e.target.checked)}/>
        Only show products in stock
      </label>
    </form>
  );
}

function FilterableProductTable({ products }) {
  const [filterText, SetFilterText] = useState('');
  const [inStockOnly, SetInStockOnly] = useState('false')

  return (
    <div>
      <SearchBar 
        filterText={filterText} 
        inStockOnly={inStockOnly}
        onFilterTextChange={SetFilterText}
        onInStockOnlyChange={SetInStockOnly} />
      <ProductTable 
        products={products} 
        filterText={filterText} 
        inStockOnly={inStockOnly}/>
    </div>
  );
}


export default function App() {
  return (
    <div>
      <FilterableProductTable products={PRODUCTS} />;
    </div>
  );
}