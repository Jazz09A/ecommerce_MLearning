'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { Minus, Plus, Trash2, CreditCard, Truck } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'
import { useRouter } from 'next/navigation'

export default function ShoppingCart() {
  const [items, setItems] = useState<any[]>([])  // Estado para almacenar los productos del carrito
  const [total, setTotal] = useState(0)  // Estado para el total del carrito
  const [paymentMethod, setPaymentMethod] = useState('credit-card')  // Estado para el método de pago
  const [shipping] = useState(5.99)  // Costo de envío
  const router = useRouter()

  // Verificamos si el carrito está vacío
  const isCartEmpty = items.length === 0
  const grandTotal = total + shipping  // Total incluyendo envío

  // Función para obtener el carrito desde el backend
  const fetchCart = async () => {
    const token = localStorage.getItem('token')

    if (!token) {
      // Guardamos la URL actual antes de redirigir
      localStorage.setItem('redirectAfterLogin', window.location.href)
      // Redirigimos al login
      router.push(`/login`)
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/cart/cart_by_user_id', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      })

      const data = await response.json()
      
      if (response.status === 401) {
        console.log('Token expirado o inválido, redirigiendo al login...')
        localStorage.setItem('redirectAfterLogin', window.location.href)  // Guardamos la URL
        router.push('/login')
      } else if (response.ok) {
        setItems(data.items)  // Solo tomamos los items del carrito
        const cartTotal = data.items.reduce((acc: number, item: any) => acc + (item.price_at_time * item.quantity), 0)
        setTotal(cartTotal)
      } else {
        console.error('Error al obtener el carrito:', data.error)
      }
    } catch (error) {
      console.error('Error al hacer la solicitud:', error)
    }
  }

  // Función para manejar el cambio de cantidad en el carrito
  const handleQuantityChange = async (cartItemId: number, newQuantity: number) => {
    const token = localStorage.getItem('token');

    if (!token) {
      console.log('No token found, redirecting to login.');
      router.push('/login');
      return;
    }

    try {
      if (newQuantity > 0) {
        console.log(`Updating quantity for cart item ID ${cartItemId} to ${newQuantity}.`);

        const response = await fetch(`http://localhost:8000/api/v1/cart/items/${cartItemId}/update`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ quantity: newQuantity }),
        });

        if (response.ok) {
          console.log('Quantity updated successfully.');
          fetchCart(); // Refresh the cart after updating
        } else {
          console.error('Error updating quantity:', await response.text());
        }
      } else {
        console.log(`Removing cart item ID ${cartItemId} as quantity is set to 0.`);

        const response = await fetch(`http://localhost:8000/api/v1/cart/items/${cartItemId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          console.log('Item removed successfully.');
          fetchCart(); // Refresh the cart after removing the item
        } else {
          console.error('Error removing item:', await response.text());
        }
      }
    } catch (error) {
      console.error('Error updating the cart:', error);
    }
  };

  // Llamar a fetchCart() cuando el componente se monta
  useEffect(() => {
    fetchCart()
  }, [])

  // Función para proceder al pago
  const handleCheckout = async () => {
    const token = localStorage.getItem('token')

    if (!token) {
      router.push('/login')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/cart/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      })

      const data = await response.json()
      console.log(data)
      if (response.ok) {
        // Redirigir a la página de pago
        router.push(`/checkout/payment/${data.order_id}`)
      } else {
        console.error('Error en el checkout:', data.error)
      }
    } catch (error) {
      console.error('Error al proceder con el checkout:', error)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold">Carrito de Compras</h1>

      {/* Mostrar mensaje si el carrito está vacío */}
      {isCartEmpty ? (
        <p className="text-lg text-center font-semibold">El carrito está vacío. ¡Agrega productos!</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {/* Productos del carrito */}
          <div className="space-y-4">
            {items.map(item => (
              <Card key={item.product_id}>
                <CardContent className="p-4">
                  <div className="flex gap-4">
                    <Image
                      src={item.image || '/placeholder.svg'}  // Si no tiene imagen, usar placeholder
                      alt={item.title}
                      width={80}
                      height={80}
                      className="rounded-lg object-cover"
                    />
                    <div className="flex-1 space-y-2">
                      <h3 className="font-medium">{item.title}</h3>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => handleQuantityChange(item.product_id, item.quantity - 1)}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <span className="w-12 text-center">{item.quantity}</span>
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => handleQuantityChange(item.product_id, item.quantity + 1)}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    <div className="space-y-2 text-right">
                      <p className="font-medium">${(item.price_at_time * item.quantity).toFixed(2)}</p>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-red-500"
                        onClick={() => handleQuantityChange(item.product_id, 0)}  // Eliminar el producto
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Resumen del pedido y métodos de pago */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Método de Pago</CardTitle>
              </CardHeader>
              <CardContent>
                <RadioGroup
                  value={paymentMethod}
                  onValueChange={setPaymentMethod}
                  className="space-y-3"
                >
                  <div className="flex items-center space-x-3">
                    <RadioGroupItem value="credit-card" id="credit-card" />
                    <Label htmlFor="credit-card" className="flex items-center gap-2">
                      <CreditCard className="h-4 w-4" />
                      Tarjeta de Crédito
                    </Label>
                  </div>
                  <div className="flex items-center space-x-3">
                    <RadioGroupItem value="debit-card" id="debit-card" />
                    <Label htmlFor="debit-card" className="flex items-center gap-2">
                      <CreditCard className="h-4 w-4" />
                      Tarjeta de Débito
                    </Label>
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>

            {/* Resumen de los costos */}
            <Card>
              <CardHeader>
                <CardTitle>Resumen del Pedido</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span>${total.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="flex items-center gap-2">
                    <Truck className="h-4 w-4" />
                    Envío
                  </span>
                  <span>${shipping.toFixed(2)}</span>
                </div>
                <Separator />
                <div className="flex justify-between font-medium">
                  <span>Total</span>
                  <span>${grandTotal.toFixed(2)}</span>
                </div>
              </CardContent>
              <CardFooter>
                <Button className="w-full" onClick={handleCheckout}>
                  Proceder al pago
                </Button>
              </CardFooter>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
