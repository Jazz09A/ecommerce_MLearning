'use client'

import Image from 'next/image'
import Link from 'next/link'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import React from 'react'
import { useRouter } from 'next/navigation'

interface ProductCardProps {
  productId: number
  title: string
  price: number
  description: string
  href: string
}

export function ProductCard({ title, price, description, href, productId }: ProductCardProps) {
  const formattedPrice = price?.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' }) || 'N/A';
  const router = useRouter()

  const handleViewProduct = async () => {
    const token = localStorage.getItem('token')
    
    if (!token) {
      // Guardamos la URL actual antes de redirigir
      localStorage.setItem('redirectAfterLogin', window.location.href)
      // Redirigimos al login
      router.push(`/login`)
      return
    }

    try {
      // Hacemos la solicitud para registrar la interacción
      const response = await fetch(`http://localhost:8000/api/v1/interactions/interactions/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          product_id: productId,
          event_type: 'view', 
          rating: 1, 
        })
      })

      if (response.status === 401) {
        // Si la respuesta es Unauthorized, redirigimos al login para obtener un nuevo token
        console.log('Token expirado o inválido, redirigiendo al login...')
        localStorage.setItem('redirectAfterLogin', window.location.href)  // Guardamos la URL
        router.push('/login')
      } else if (response.ok) {
        console.log('Interacción registrada exitosamente')
        // Redirigir al producto si la interacción se registró exitosamente
        window.location.href = href
      } else {
        console.error('Error al registrar la interacción')
      }
    } catch (error) {
      console.error('Error al realizar la solicitud:', error)
    }
  }


  return (
    <Card className="group overflow-hidden" onClick={handleViewProduct}>
      <div className="cursor-pointer">
        <Link href={href} className="block">
          <CardContent className="p-0">
            <Image
              src="/placeholder.svg"
              alt={title}
              width={400}
              height={300}
              className="aspect-[4/3] object-cover w-full"
            />
          </CardContent>
        </Link>
        <CardFooter className="flex flex-col items-start gap-2 p-4">
          <Link href={href} className="block">
            <h3 className="font-semibold">{title}</h3>
          </Link>
          <p className="text-sm text-muted-foreground">{description}</p>
          <p className="font-bold">
            {formattedPrice}
          </p>
        </CardFooter>
      </div>
    </Card>
  )
}
