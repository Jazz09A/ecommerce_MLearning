"use client";
import { useEffect, useState } from 'react';
import { ProductCard } from '@/components/product-card';

interface Product {
  product_id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
  image: string;
  description: string;
  created_at: string;
}

export default function ProductosPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/products/');
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
        const data: Product[] = await response.json();
        setProducts(data);
      } catch (err) {
        setError('Error fetching products');
      }
    };

    fetchProducts();
  }, []);

  if (error) {
    return <div className="container mx-auto px-4 py-8">{error}</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Nuestros Productos</h1>
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {products.map((product) => (
          <ProductCard
            key={product.product_id}
            title={product.name}
            price={product.price}
            description={product.description}
            href={`/productos/${product.product_id}`}
            productId={product.product_id}
          />
        ))}
      </div>
    </div>
  );
}

