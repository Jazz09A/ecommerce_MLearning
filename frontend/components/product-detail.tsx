'use client'

import { Button } from '@/components/ui/button'
import { useCart } from '@/contexts/cart-context'
import Image from 'next/image'
import { useState } from 'react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useRouter } from 'next/navigation'

interface ProductDetailProps {
  product: {
    id: number
    title: string
    price: number
    description: string
    stock: number
  }
}

export function ProductDetail({ product }: ProductDetailProps) {
  const [quantity, setQuantity] = useState('1')
  // const { addToCart } = useCart()
  const router = useRouter()

    const handleAddToCart = async () => {
    const token = localStorage.getItem('token')

    if (!token) {
      router.push('/login')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/cart/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          product_id: product.id,
          quantity: quantity,
        }), // Se envía el product_id y la quantity
      })

      const data = await response.json()

      if (response.ok) {
        console.log('Producto agregado al carrito:', data)
      } else {
        console.error('Error al agregar al carrito:', data.error)
      }
    } catch (error) {
      console.error('Error al hacer la solicitud:', error)
    }
  };

  return (
    <div className="grid gap-8 md:grid-cols-2">
      <div className="relative aspect-square">
        <Image
          src="/placeholder.svg"
          alt={product.title}
          fill
          className="object-cover rounded-lg"
          priority
        />
      </div>
      <div className="flex flex-col gap-4">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold">{product.title}</h1>
          <p className="text-3xl font-bold">${product.price.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}</p>
        </div>
        
        <p className="text-gray-600">{product.description}</p>

        <div className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="quantity" className="text-sm font-medium">
              Cantidad
            </label>
            <Select value={quantity} onValueChange={setQuantity}>
              <SelectTrigger className="w-24">
                <SelectValue placeholder="Cantidad" />
              </SelectTrigger>
              <SelectContent>
                {[...Array(Math.min(10, product.stock))].map((_, i) => (
                  <SelectItem key={i + 1} value={(i + 1).toString()}>
                    {i + 1}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button 
            onClick={handleAddToCart}
            className="w-full md:w-auto"
          >
            Añadir al carrito
          </Button>

          <p className="text-sm text-gray-500">
            {product.stock} unidades disponibles
          </p>
        </div>
      </div>
    </div>
  )
}

