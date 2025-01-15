'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { loadStripe } from '@stripe/stripe-js'
import { Elements } from '@stripe/react-stripe-js'
import { PaymentForm } from './payment-form'

// Cargar la clave pública de Stripe
const stripePromise = loadStripe('pk_test_51QgsBCCQYCslB2bN9YptptgmFPNaMELFAQvf3klyw7qqWlloOXwYPYv5lLgnFinUU6qAwt5TE9AhlhVUtjOWPIau002gdxReYm')

export default function CheckoutPage() {
  const [clientSecret, setClientSecret] = useState<string | null>(null)
  const [subtotal, setSubtotal] = useState<number | null>(null)
  const [shipping, setShipping] = useState<number | null>(null)
  const [total, setTotal] = useState<number | null>(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      localStorage.setItem('redirectAfterLogin', '/checkout')
      router.push('/login')
      return
    }

    // Llamar al backend para crear el PaymentIntent y obtener el client_secret
    fetch('http://localhost:8000/api/v1/cart/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => {
        setClientSecret(data.client_secret)
        setSubtotal(data.subtotal)
        setShipping(data.shipping)
        setTotal(data.total)
      })
      .catch(error => console.error('Error:', error))
  }, [router])

  if (!clientSecret || !subtotal || !shipping || !total) {
    return <div>Loading...</div>
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Complete su pago</h1>
      <Elements stripe={stripePromise}>
        <PaymentForm 
          clientSecret={clientSecret}
          subtotal={subtotal}
          shipping={shipping}
          total={total}
        />
      </Elements>
    </div>
  )
}