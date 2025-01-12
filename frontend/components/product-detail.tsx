'use client'

import { Button } from '@/components/ui/button'
import { useCart } from '@/contexts/cart-context'
import Image from 'next/image'
import { useState } from 'react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

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
  const { addToCart } = useCart()

  const handleAddToCart = () => {
    addToCart(product, parseInt(quantity))
    console.log(`Adding ${quantity} of product ${product.id} to cart`)
  }

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
          <p className="text-3xl font-bold">${product.price.toFixed(2)}</p>
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

