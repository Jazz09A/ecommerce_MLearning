import { Button } from '@/components/ui/button';
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
import { useState } from 'react';

interface PaymentFormProps {
  clientSecret: string;
}


export function PaymentForm({ clientSecret }: PaymentFormProps) {
  const stripe = useStripe();

  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setIsProcessing(true);

    const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: elements.getElement(CardElement)!,
      },
    });

    setIsProcessing(false);

    if (error) {
      setError(error.message || 'Pago fallido');
    } else if (paymentIntent?.status === 'succeeded') {
      // Obtener el token de autenticación
      const token = localStorage.getItem('token'); // Asegúrate de que el token sea correcto

      console.log("paymentIntent", paymentIntent)
      console.log("token", token)

      fetch('http://localhost:8000/api/v1/checkout/confirm-payment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // Incluye el token de autenticación
        },
        body: JSON.stringify({
          id: paymentIntent.id,  // Enviar paymentIntent.id en lugar de clientSecret
          token: token, // Enviar el token de autenticación
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('No autorizado');
          }
          return response.json();
        })
        .then((data) => {
          if (data.message === "Pago y orden confirmados exitosamente") {
            // Redirigir al usuario a la página de éxito
            window.location.href = '/checkout/success';
          }
        })


        .catch((error) => {
          setError('Error al procesar el pago: ' + error.message);
        });
    }
  };


  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <CardElement className="p-2 border rounded-md" />
      {error && <div className="text-red-500">{error}</div>}
      <Button type="submit" disabled={isProcessing} className="w-full bg-blue-500 text-white py-2 rounded-md">
        {isProcessing ? 'Procesando...' : 'Pagar'}
      </Button>
    </form>
  );
}
