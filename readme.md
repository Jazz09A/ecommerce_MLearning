# Proyecto de E-commerce

Este proyecto es una aplicación de comercio electrónico construida con un frontend en React (Next.js) y un backend en FastAPI. Se integra con Stripe para procesar los pagos.

## Requisitos Previos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu máquina:

- [Node.js](https://nodejs.org/) (versión 14 o superior)
- [Python](https://www.python.org/) (versión 3.8 o superior)
- [Git](https://git-scm.com/)
- [Cuenta de Stripe](https://stripe.com/) (para el procesamiento de pagos)

## Empezando

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Clona el Repositorio

Primero, clona el repositorio desde GitHub a tu máquina local:

```bash
git clone https://github.com/usuario/ecommerce.git
```

### 2. Configurar el Backend

Navega al directorio `backend` y configura el entorno de Python:

#### Instalar Dependencias del Backend

Instala los paquetes necesarios de Python utilizando `pip`:

```bash
cd backend
pip install -r requirements.txt
```

#### Configurar la Base de Datos

Asegúrate de que la base de datos SQLite esté configurada correctamente. Si es necesario, ejecuta migraciones iniciales o configura el esquema de la base de datos:

```bash
python -m app.db.init_db
```

Esto creará la base de datos `database.db` en el directorio adecuado si no existe. Si tienes alguna base de datos existente, asegúrate de que el esquema esté alineado con los modelos de datos.

#### Ejecutar el Servidor Backend

Inicia el servidor FastAPI ejecutando el siguiente comando:

```bash
uvicorn app.main:app --reload
```

El servidor backend ahora estará corriendo en `http://localhost:8000`.

### 3. Configurar el Frontend

Navega al directorio `frontend`:

```bash
cd frontend
```

#### Instalar Dependencias del Frontend

Instala los paquetes necesarios de Node.js utilizando `npm`:

```bash
npm install
```

#### Configurar las Variables de Entorno

Crea un archivo `.env.local` en el directorio `frontend` y agrega tu clave pública de Stripe:

```env
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_test_tu_clave_publica_de_stripe
```

Este paso es esencial para poder integrar Stripe correctamente.

#### Ejecutar el Servidor Frontend

Inicia el servidor de desarrollo de Next.js con el siguiente comando:

```bash
npm run dev
```

El servidor frontend ahora estará corriendo en `http://localhost:3000`.

### 4. Acceder a la Aplicación

Abre tu navegador web y dirígete a `http://localhost:3000` para acceder a la aplicación de comercio electrónico.

### 5. Configuración Adicional

- Asegúrate de que el backend esté correctamente configurado para manejar la autenticación y autorización. El sistema de autenticación debe estar configurado correctamente en FastAPI, y el frontend debe obtener y almacenar un token JWT para realizar las solicitudes de manera segura.
- Actualiza cualquier endpoint de la API o variables de entorno según sea necesario para tu configuración específica.

### 6. Flujo Principal del Proyecto

El flujo de este proyecto se basa en un proceso de compras típico de comercio electrónico. Los usuarios pueden navegar por los productos, añadirlos al carrito, proceder al pago y completar la compra. El sistema gestiona la autenticación de usuarios, el procesamiento de pagos a través de Stripe y el registro de interacciones de los usuarios con los productos.

#### Componentes principales:
1. **Frontend**: Consta de la interfaz de usuario construida en Next.js con React. El frontend interactúa con el backend para obtener los productos, realizar pagos, gestionar el carrito, entre otros.
2. **Backend**: El backend está basado en FastAPI y gestiona las operaciones de la base de datos, como la creación de carritos, el procesamiento de pagos y la autenticación de usuarios.
3. **Base de Datos**: Utiliza SQLite para almacenar información sobre productos, carritos, órdenes y usuarios.
4. **Stripe**: Se usa para procesar pagos, generando un PaymentIntent y utilizando la clave pública de Stripe para la verificación de tarjetas de crédito.

### 7. Generación de Datos para el Modelo de Machine Learning

#### Datos en los que nos estamos enfocando:
- Interacciones de los usuarios con los productos, como visualizaciones, adiciones al carrito y compras.
- Calificaciones de los productos por parte de los usuarios.

El modelo de machine learning se entrena utilizando estas interacciones para recomendar productos a los usuarios en función de sus intereses previos.

### 8. Funcionamiento del Modelo de Machine Learning

#### Algoritmo utilizado:
Utilizamos el algoritmo de **K-Nearest Neighbors (KNN)** para la recomendación de productos. Este algoritmo se basa en encontrar los productos más cercanos en el espacio de características de los usuarios (basado en sus interacciones previas).

#### Por qué KNN:
KNN es un algoritmo simple y efectivo para sistemas de recomendación cuando no se tiene mucha información estructurada. Al calcular la similitud entre los usuarios en función de sus interacciones, podemos recomendar productos similares a los que el usuario ha mostrado interés.

#### Finalidad del modelo:
El objetivo es recomendar productos que sean de interés para el usuario basándose en las interacciones previas con el sistema.

### 9. Contribución

Si deseas contribuir a este proyecto, por favor, realiza un **fork** del repositorio y envía un **pull request** con tus cambios. Asegúrate de seguir las mejores prácticas de codificación y agregar pruebas unitarias si es necesario.

### 10. Licencia

Este proyecto está bajo la Licencia MIT.

---

Este `README` explica de forma detallada cómo configurar el proyecto y cómo funciona el flujo completo, desde el frontend hasta el modelo de recomendación de productos utilizando machine learning.
```

Este README está diseñado para guiar a los desarrolladores a través de la configuración del proyecto y proporcionar detalles sobre cómo funciona el sistema, desde la base de datos hasta el modelo de recomendaciones de productos, y cómo contribuir al proyecto.