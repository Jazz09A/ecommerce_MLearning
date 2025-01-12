'use client'

import Link from 'next/link'
import { ShoppingCart, User } from 'lucide-react'
import { Button } from '@/components/ui/button'
import React from 'react'
import { useCart } from '@/contexts/cart-context'

export function Header() {
  const { uniqueItemsCount } = useCart()

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="font-semibold text-xl">
          Mi Tienda
        </Link>
        <nav className="hidden md:flex items-center gap-6">
          <Link href="/" className="text-sm hover:text-primary">
            Inicio
          </Link>
          <Link href="/productos" className="text-sm hover:text-primary">
            Productos
          </Link>
          <Link href="/sobre-nosotros" className="text-sm hover:text-primary">
            Sobre Nosotros
          </Link>
        </nav>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Button variant="ghost" size="icon" asChild>
              <Link href="/carrito">
                <ShoppingCart className="h-5 w-5" />
                <span className="sr-only">Carrito</span>
              </Link>
            </Button>
            {uniqueItemsCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
                {uniqueItemsCount}
              </span>
            )}
          </div>
          <Button variant="ghost" size="icon" asChild>
            <Link href="/user_me">
              <User className="h-5 w-5" />
              <span className="sr-only">Cuenta</span>
            </Link>
          </Button>
        </div>
      </div>
    </header>
  )
}

