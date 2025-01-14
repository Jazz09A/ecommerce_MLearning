"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button'; // O cualquier otro componente de UI que uses
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import { PaymentForm } from './payment-form';


const stripePromise = loadStripe('pk_test_51QgsBCCQYCslB2bN9YptptgmFPNaMELFAQvf3klyw7qqWlloOXwYPYv5lLgnFinUU6qAwt5TE9AhlhVUtjOWPIau002gdxReYm'); // Usa tu clave pública de prueba

export default function CheckoutPage() {
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const router = useRouter(); 

  useEffect(() => {
    // Verificar si el usuario está autenticado
    const token = localStorage.getItem('token');
    if (!token) {
      localStorage.setItem('redirectAfterLogin', '/checkout');
      router.push('/login');
      return;
    }


    // Llamar a tu backend para crear un PaymentIntent y obtener el client_secret
    fetch('http://localhost:8000/api/v1/checkout', { method: 'POST' })
      .then(res => res.json())
      .then(data => setClientSecret(data.client_secret))
      .catch(error => console.error('Error:', error));
  }, [router]);

  if (!clientSecret) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Pago</h1>
      <Elements stripe={stripePromise}>
        <PaymentForm clientSecret={clientSecret} />
      </Elements>
    </div>
  );
}
