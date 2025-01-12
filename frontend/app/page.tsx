import { Button } from '@/components/ui/button'
import { ProductCard } from '@/components/product-card'
import Link from 'next/link'
import  React  from 'react'
import AboutPage from './sobre-nosotros/page'
const featuredProducts = [
  { id: 1, title: 'Producto Destacado 1', price: 19.99, description: 'Descripción corta del Producto 1' },
  { id: 2, title: 'Producto Destacado 2', price: 29.99, description: 'Descripción corta del Producto 2' },
  { id: 3, title: 'Producto Destacado 3', price: 39.99, description: 'Descripción corta del Producto 3' },
]

export default function Home() {
  return (
    <div className="flex flex-col gap-16 py-8 md:py-12">
      <section className="container mx-auto px-4 text-center space-y-4">
        <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
          Bienvenido a Nuestra Tienda Online
        </h1>
        <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl">
          Descubre nuestra amplia selección de productos de alta calidad.
        </p>
        <Button asChild className="mt-4">
          <Link href="/productos">
            Ver Todos los Productos
          </Link>
        </Button>
      </section>

      <section className="container mx-auto px-4">
        <h2 className="text-2xl font-bold text-center mb-8">Productos Destacados</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featuredProducts.map((product) => (
            <ProductCard
              key={product.id}
              title={product.title}
              price={product.price}
              description={product.description}
              href={`/productos/${product.id}`}
            />
          ))}
        </div>
        <section>
          <AboutPage />
        </section>
      </section>
    </div>
  )
}

