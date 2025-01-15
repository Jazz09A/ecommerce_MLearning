'use client'

import { Button } from '@/components/ui/button'
import { ProductCard } from '@/components/product-card'
import Link from 'next/link'
import React, { useState, useEffect } from 'react'
import AboutPage from './sobre-nosotros/page'
import { useRouter } from 'next/navigation'

const featuredProducts = [
  { id: 1, title: 'Producto Destacado 1', price: 19.99, description: 'Descripción corta del Producto 1' },
  { id: 2, title: 'Producto Destacado 2', price: 29.99, description: 'Descripción corta del Producto 2' },
  { id: 3, title: 'Producto Destacado 3', price: 39.99, description: 'Descripción corta del Producto 3' },
]

export default function Home() {
  const [recommendedProducts, setRecommendedProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [token, setToken] = useState<string | null>(null); // Estado para almacenar el token
  const router = useRouter();

  useEffect(() => {
    // Verificar si estamos en el cliente antes de acceder a localStorage
    if (typeof window !== "undefined") {
      const tokenFromStorage = localStorage.getItem('token');
      setToken(tokenFromStorage);
    }
  }, []);

  useEffect(() => {
    if (token) {
      // Hacer la petición al backend para obtener los productos recomendados
      const fetchRecommendedProducts = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/v1/recommendations/recommended-products', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`, // Asegúrate de pasar el token de autenticación
            },
          });
          if (response.status === 401) {
            console.log('No autorizado');
            router.push('/login');
            return;
          }
          const data = await response.json();
          console.log("data", data)
          // Si la respuesta tiene productos recomendados, actualiza el estado
          if (data && data.recommended_products && data.recommended_products.length > 0) {
            setRecommendedProducts(data.recommended_products);
          } else {
            setRecommendedProducts([]);
          }
        } catch (error) {
          console.error('Error fetching recommended products:', error);
          setRecommendedProducts([]);
        } finally {
          setLoading(false);
        }
      };

      fetchRecommendedProducts();
    }
  }, [token]);

  console.log("recommendedProducts",recommendedProducts)

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

      {/* Sección de productos recomendados si están disponibles */}
      {recommendedProducts.length > 0 ? (
        <section className="container mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-8">Productos recomendados para ti</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {recommendedProducts.map((product) => (
              <ProductCard
                key={product.product_id} // Aquí se cambia a product.product_id
                title={product.name}
                price={product.price}
                description={product.description}
                href={`/productos/${product.product_id}`} // Aquí también se cambia a product.product_id
                productId={product.product_id} // Aquí se cambia a product.product_id
              />
            ))}
          </div>
        </section>
      ) : (
        // Si no hay productos recomendados, mostrar productos destacados
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
                productId={product.id}
              />
            ))}
          </div>
        </section>
      )}

      <section>
        <AboutPage />
      </section>
    </div>
  );
}
