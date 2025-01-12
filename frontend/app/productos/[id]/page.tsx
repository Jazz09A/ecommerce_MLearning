import { ProductDetail } from '@/components/product-detail'
import React from 'react'

// This would typically come from a database
const products = [
  {
    id: 1,
    title: 'Producto 1',
    price: 19.99,
    description: 'Descripción detallada del Producto 1. Este producto es ideal para aquellos que buscan calidad y rendimiento. Fabricado con los mejores materiales y diseñado para durar.',
    stock: 10
  },
  {
    id: 2,
    title: 'Producto 2',
    price: 29.99,
    description: 'Descripción detallada del Producto 2. Una excelente opción para quienes valoran la calidad y el diseño. Perfecto para uso diario.',
    stock: 15
  },
  // Add more products as needed
]

interface ProductPageProps {
  params: {
    id: string
  }
}

export default function ProductPage({ params }: ProductPageProps) {
  const product = products.find(p => p.id === parseInt(params.id))

  if (!product) {
    return <div className="container mx-auto px-4 py-8">Producto no encontrado</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <ProductDetail product={product} />
    </div>
  )
}

