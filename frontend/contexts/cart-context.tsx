'use client'

import React, { createContext, useContext, useState } from 'react'

interface CartItem {
  id: number
  title: string
  price: number
  quantity: number
  image: string
}


interface CartContextType {
  items: CartItem[]
  addToCart: (product: { id: number; title: string; price: number; image: string }, quantity: number) => void
  removeFromCart: (id: number) => void
  updateQuantity: (id: number, quantity: number) => void
  total: number
  uniqueItemsCount: number

}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([])

  const addToCart = (product: { id: number; title: string; price: number; image: string }, quantity: number) => {
    setItems(currentItems => {
      const existingItem = currentItems.find(item => item.id === product.id)
      

      if (existingItem) {
        return currentItems.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      }
      
      return [...currentItems, { ...product, quantity }]
    })
  }

  const removeFromCart = (id: number) => {
    setItems(currentItems => currentItems.filter(item => item.id !== id))
  }

  const updateQuantity = (id: number, quantity: number) => {
    setItems(currentItems => {
      return currentItems.map(item =>
        item.id === id ? { ...item, quantity } : item
      )
    })
  }

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const uniqueItemsCount = items.length // Cuenta productos únicos, no cantidades

  return (
    <CartContext.Provider value={{ items, addToCart, removeFromCart, updateQuantity, total, uniqueItemsCount }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
} 