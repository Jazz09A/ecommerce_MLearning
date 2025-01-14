import { CardElement } from '@stripe/react-stripe-js';

export default function StripeCardElement() {
  return (
    <div className="stripe-card-element">
      <CardElement />
    </div>
  );
}
