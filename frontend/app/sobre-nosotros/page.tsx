import { Shield, Truck, Headphones } from 'lucide-react';
import React from 'react';

export default function AboutPage() {
  return (
    <div className="container mx-auto px-6 py-12 md:py-16 space-y-20">
      {/* Why Choose Us Section */}
      <section className="grid gap-16 md:grid-cols-3">
        <div className="text-center space-y-6">
          <div className="mx-auto w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center">
            <Shield className="w-7 h-7 text-primary" />
          </div>
          <h3 className="text-lg font-semibold">Calidad Garantizada</h3>
          <p className="text-base text-muted-foreground">
            Todos nuestros productos son cuidadosamente seleccionados para asegurar la mejor calidad.
          </p>
        </div>
        <div className="text-center space-y-6">
          <div className="mx-auto w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center">
            <Truck className="w-7 h-7 text-primary" />
          </div>
          <h3 className="text-lg font-semibold">Envío Rápido</h3>
          <p className="text-base text-muted-foreground">
            Entregamos tus pedidos en el menor tiempo posible para que disfrutes de tus compras cuanto antes.
          </p>
        </div>
        <div className="text-center space-y-6">
          <div className="mx-auto w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center">
            <Headphones className="w-7 h-7 text-primary" />
          </div>
          <h3 className="text-lg font-semibold">Atención al Cliente</h3>
          <p className="text-base text-muted-foreground">
            Nuestro equipo está siempre disponible para ayudarte con cualquier duda o problema.
          </p>
        </div>
      </section>

      {/* About Us Section */}
      <section className="max-w-6xl mx-auto flex flex-col md:flex-row items-center md:space-x-12">
        {/* Text Content */}
        <div className="prose prose-lg prose-gray text-center md:text-left flex-1">
          <h2 className="text-4xl font-bold mb-6">Nuestra Historia</h2>
          <p>
            En Nuestra Tienda Online, nos apasiona ofrecer productos de alta calidad que mejoren la vida de nuestros clientes. Fundada en 2023, nuestra misión es proporcionar una experiencia de compra excepcional combinada con un servicio al cliente inigualable.
          </p>
          <p>
            Nuestro equipo está formado por expertos en diversas áreas, todos comprometidos con la excelencia y la satisfacción del cliente. Trabajamos incansablemente para mantenernos a la vanguardia de las últimas tendencias y tecnologías, asegurando que nuestros productos cumplan con los más altos estándares de calidad.
          </p>
        </div>
        {/* Placeholder for Image */}
        <div className="flex-1">
          <div className="w-full h-64 bg-gray-200 rounded-lg flex items-center justify-center text-gray-500">
            Placeholder Imagen
          </div>
        </div>
      </section>
    </div>
  );
}
