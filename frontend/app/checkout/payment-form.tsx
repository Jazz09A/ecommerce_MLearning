import { Button } from '@/components/ui/button'
import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js'
import { useState } from 'react'

interface PaymentFormProps {
  clientSecret: string
  subtotal: number
  shipping: number
  total: number
}

export function PaymentForm({ clientSecret, subtotal, shipping, total }: PaymentFormProps) {
  const stripe = useStripe()
  const elements = useElements()
  const [error, setError] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()

    if (!stripe || !elements) {
      return
    }

    setIsProcessing(true)

    const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: elements.getElement(CardElement)!,
      },
    })

    setIsProcessing(false)

    if (error) {
      setError(error.message || 'Pago fallido')
    } else if (paymentIntent?.status === 'succeeded') {
      const token = localStorage.getItem('token')
      try {
        // Hacemos la solicitud para registrar la interacción
        const response = await fetch(`http://localhost:8000/api/v1/interactions/interactions/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            event_type: 'purchase', 
            rating: 5, 
          })
        })
        if (response.ok) {
          console.log('Interacción registrada exitosamente')
        } else {
          console.error('Error al registrar la interacción:', response.statusText)
        }
      } catch (error) {
        console.error('Error al registrar la interacción:', error)
      }

      fetch('http://localhost:8000/api/v1/checkout/confirm-payment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          id: paymentIntent.id,
          token: token,
        }),
      })
        .then(response => response.json())
        .then(async data => {
          if (data.message === 'Pago y orden confirmados exitosamente') {
            window.location.href = 'success'
          }
        })
        .catch(error => {
          setError('Error al procesar el pago: ' + error.message)
        })
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <CardElement className="p-2 border rounded-md" />
      <div className="space-y-2">
        <div className="flex justify-between">
          <span>Subtotal:</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span>Envío:</span>
          <span>${shipping.toFixed(2)}</span>
        </div>
        <div className="flex justify-between font-bold">
          <span>Total a pagar:</span>
          <span>${total.toFixed(2)}</span>
        </div>
      </div>
      {error && <div className="text-red-500">{error}</div>}
      <Button type="submit" disabled={isProcessing} className="w-full bg-blue-500 text-white py-2 rounded-md">
        {isProcessing ? 'Procesando...' : 'Pagar'}
      </Button>
    </form>
  )
}
