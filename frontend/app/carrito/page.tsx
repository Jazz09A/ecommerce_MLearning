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
import { loadStripe } from '@stripe/stripe-js'
import { Elements, useStripe, useElements, CardElement } from '@stripe/react-stripe-js'

// Load your Stripe public key
// const stripePromise = loadStripe('your-public-key-here'); // Use your public Stripe key here

export default function ShoppingCart() {
  const [items, setItems] = useState<any[]>([])  // State to store cart items
  const [total, setTotal] = useState(0)  // State to store cart total
  const [paymentMethod, setPaymentMethod] = useState('credit-card')  // State for payment method
  const [shipping] = useState(5.99)  // Shipping cost
  const router = useRouter()
  // const stripe = useStripe();
  // const elements = useElements();

  const isCartEmpty = items.length === 0;
  const grandTotal = total + shipping;  // Total including shipping

  // Handle payment method change
  const handlePaymentMethodChange = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // const { error, paymentMethod } = await stripe.createPaymentMethod({
    //   type: 'card',
    //   card: elements.getElement(CardElement),
    // });

    // if (error) {
    //   console.error(error);
    //   return;
    // }

    // const paymentMethodId = paymentMethod.id;

    try {
      const response = await fetch('http://localhost:8000/api/v1/update-payment-method', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ payment_method: paymentMethod }),  // Send payment method id
      });

      const data = await response.json();
      if (!response.ok) {
        console.error('Error updating payment method:', data.message);
      } else {
        console.log('Payment method updated');
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  useEffect(() => {
    handlePaymentMethodChange();
  }, [paymentMethod]);

  // Fetch cart data from backend
  const fetchCart = async () => {
    const token = localStorage.getItem('token');

    if (!token) {
      localStorage.setItem('redirectAfterLogin', window.location.href);
      router.push('/login');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/cart/cart_by_user_id', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.status === 401) {
        console.log('Token expired or invalid, redirecting to login...');
        localStorage.setItem('redirectAfterLogin', window.location.href);
        router.push('/login');
      } else if (response.ok) {
        setItems(data.items);  // Only take cart items
        const cartTotal = data.items.reduce((acc: number, item: any) => acc + (item.price_at_time * item.quantity), 0);
        setTotal(cartTotal);
      } else {
        setItems([]);
        console.error('Error fetching cart:', data.message);
      }
    } catch (error) {
      console.error('Error making request:', error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const handleQuantityChange = async (cartItemId: number, newQuantity: number) => {
    const token = localStorage.getItem('token');

    if (!token) {
      console.log('No token found, redirecting to login.');
      router.push('/login');
      return;
    }

    try {
      if (newQuantity > 0) {
        const response = await fetch(`http://localhost:8000/api/v1/cart/items/${cartItemId}/update`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ quantity: newQuantity }),
        });

        if (response.ok) {
          fetchCart(); // Refresh the cart after updating
        } else {
          console.error('Error updating quantity:', await response.text());
        }
      } else {
        const response = await fetch(`http://localhost:8000/api/v1/cart/items/${cartItemId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          fetchCart(); // Refresh the cart after removing the item
        } else {
          console.error('Error removing item:', await response.text());
        }
      }
    } catch (error) {
      console.error('Error updating cart:', error);
    }
  };

  const handleCheckout = async () => {
    const token = localStorage.getItem('token');

    if (!token) {
      router.push('/login');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/cart/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();
      console.log(data);
      if (response.status === 401) {
        console.log('Token expired or invalid, redirecting to login...');
        localStorage.setItem('redirectAfterLogin', window.location.href);
        router.push('/login');
      } else if (response.ok) {
        router.push(`/checkout`);
      } else {
        console.error('Error in checkout:', data.message);
      }
    } catch (error) {
      console.error('Error processing checkout:', error);
    }
  };

  return (
    // <Elements stripe={stripePromise}>
      <div className="max-w-4xl mx-auto p-4 space-y-6">
        <h1 className="text-2xl font-bold">Shopping Cart</h1>

        {/* Display message if the cart is empty */}
        {isCartEmpty ?   (
          <p className="text-lg text-center font-semibold">Your cart is empty. Add items!</p>
        ) : (
          <div className="grid gap-6 md:grid-cols-2">
            {/* Cart items */}
            <div className="space-y-4">
              {items.map(item => (
                <Card key={item.product_id}>
                  <CardContent className="p-4">
                    <div className="flex gap-4">
                      <Image
                        src={item.image || '/placeholder.svg'}  // Placeholder image if not available
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
                          onClick={() => handleQuantityChange(item.product_id, 0)}  // Remove item
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Payment Method */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Payment Method</CardTitle>
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
                        Credit Card
                      </Label>
                    </div>
                    <div className="flex items-center space-x-3">
                      <RadioGroupItem value="debit-card" id="debit-card" />
                      <Label htmlFor="debit-card" className="flex items-center gap-2">
                        <CreditCard className="h-4 w-4" />
                        Debit Card
                      </Label>
                    </div>
                  </RadioGroup>
                </CardContent>
              </Card>

              {/* Cost Summary */}
              <Card>
                <CardHeader>
                  <CardTitle>Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span>Subtotal</span>
                    <span>${total.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="flex items-center gap-2">
                      <Truck className="h-4 w-4" />
                      Shipping
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
                    Proceed to Payment
                  </Button>
                </CardFooter>
              </Card>
            </div>
          </div>
        )}
      </div>
    // </Elements>
  );
}
