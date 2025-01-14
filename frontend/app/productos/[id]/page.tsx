"use client";

import { useEffect, useState } from 'react';
import { ProductDetail } from '@/components/product-detail';

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

interface ProductPageProps {
  params: {
    id: string;
  };
}

export default function ProductPage({ params }: ProductPageProps) {
  const [product, setProduct] = useState<Product | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/products/${params.id}`);
        if (!response.ok) {
          throw new Error('Product not found');
        }
        const data: Product = await response.json();
        setProduct(data);
      } catch (err) {
        setError('Error fetching product');
      }
    };

    fetchProduct();
  }, [params.id]);

  if (error) {
    return <div className="container mx-auto px-4 py-8">{error}</div>;
  }

  if (!product) {
    return <div className="container mx-auto px-4 py-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <ProductDetail product={{...product, id: product.product_id, title: product.name}} />
    </div>
  );
}

