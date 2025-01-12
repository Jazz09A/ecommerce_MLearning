import { ProductCard } from '@/components/product-card'
import  React  from 'react'
const products = [
  { id: 1, title: 'Producto 1', price: 19.99, description: 'Descripción corta del Producto 1' },
  { id: 2, title: 'Producto 2', price: 29.99, description: 'Descripción corta del Producto 2' },
  { id: 3, title: 'Producto 3', price: 39.99, description: 'Descripción corta del Producto 3' },
  { id: 4, title: 'Producto 4', price: 49.99, description: 'Descripción corta del Producto 4' },
  { id: 5, title: 'Producto 5', price: 59.99, description: 'Descripción corta del Producto 5' },
  { id: 6, title: 'Producto 6', price: 69.99, description: 'Descripción corta del Producto 6' },
]

export default function ProductosPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Nuestros Productos</h1>
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            title={product.title}
            price={product.price}
            description={product.description}
            href={`/productos/${product.id}`}
          />
        ))}
      </div>
    </div>
  )
}

