"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import { PaymentForm } from './payment-form';

const stripePromise = loadStripe('pk_test_51QgsBCCQYCslB2bN9YptptgmFPNaMELFAQvf3klyw7qqWlloOXwYPYv5lLgnFinUU6qAwt5TE9AhlhVUtjOWPIau002gdxReYm');


export default function CheckoutPage() {
  const [clientSecret, setClientSecret] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      localStorage.setItem('redirectAfterLogin', '/checkout')
      router.push('/login')
      return
    }

    // Fetch the client secret for Stripe
    fetch('http://localhost:8000/api/v1/cart/checkout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    })
      .then(res => res.json())
      .then(data => setClientSecret(data.client_secret))
      .catch(error => console.error('Error:', error))
  }, [router])

  if (!clientSecret) {
    return <div>Loading...</div> // You can show a loading spinner here
  }

  return (
    <div>
      <h1>Checkout</h1>
      <Elements stripe={stripePromise} options={{ clientSecret }}>
        <PaymentForm clientSecret={clientSecret} />
      </Elements>
    </div>
  )
}
