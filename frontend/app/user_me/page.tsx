'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { CreditCard, Package, Settings, User, LogOut } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import Image from 'next/image'

type Order = {
  id: number
  date: string
  status: string
  total: number
  items: number
}

type UserProfile = {
  username: string
  email: string
  orders: Order[]
  recommendations: Array<{
    id: number
    name: string
    price: number
    image: string
  }>
}

export default function UserMePage() {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null)
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          throw new Error('Token is missing')
        }

        const response = await fetch('http://localhost:8000/api/v1/users/me', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          if (response.status === 401) {
            router.push('/login')
          }
          throw new Error('Failed to fetch user data')

        }

        const data: UserProfile = await response.json()
        setUserProfile(data)
      } catch (err: any) {
        setError(err.message || 'An unknown error occurred')
        console.error(err)
      }
    }

    fetchUserData()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token') // Elimina el token del localStorage
    router.push('/login') // Redirige al usuario al login
  }

  if (error) {
    return <div>{error}</div>
  }

  if (!userProfile) {
    return <div>Loading...</div>
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
              <User className="h-8 w-8" />
            </div>
            <div>
              <CardTitle>{userProfile.username}</CardTitle>
              <CardDescription>{userProfile.email}</CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      <Tabs defaultValue="orders">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="orders">Pedidos</TabsTrigger>
          <TabsTrigger value="payments">Métodos de Pago</TabsTrigger>
          <TabsTrigger value="recommendations">Recomendados</TabsTrigger>
        </TabsList>

        <TabsContent value="orders" className="space-y-4">
          {userProfile?.orders?.map(order => (
            <Card key={order.id}>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <div>
                    <CardTitle>Pedido #{order.id}</CardTitle>
                    <CardDescription>{order.date}</CardDescription>
                  </div>
                  <Button variant="outline">Ver Detalles</Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <Package className="h-4 w-4" />
                    <span>{order.items} productos</span>
                  </div>
                  <div className="space-x-4">
                    <span className="text-muted-foreground">{order.status}</span>
                    <span className="font-medium">${order.total.toFixed(2)}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="payments">
          <Card>
            <CardHeader>
              <CardTitle>Métodos de Pago Guardados</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <CreditCard className="h-5 w-5" />
                  <div>
                    <p className="font-medium">•••• •••• •••• 1234</p>
                    <p className="text-sm text-muted-foreground">Expira 12/25</p>
                  </div>
                </div>
                <Button variant="ghost" size="icon">
                  <Settings className="h-4 w-4" />
                </Button>
              </div>
              <Button variant="outline" className="w-full">
                Agregar nuevo método de pago
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="recommendations">
          <div className="grid gap-4 md:grid-cols-3">
            {userProfile?.recommendations?.map(product => (
              <Card key={product.id}>
                <CardContent className="p-4">
                  <Image
                    src={product.image}
                    alt={product.name}
                    width={200}
                    height={200}
                    className="w-full rounded-lg object-cover mb-4"
                  />
                  <h3 className="font-medium">{product.name}</h3>
                  <p className="text-muted-foreground">${product.price.toFixed(2)}</p>
                  <Button className="w-full mt-4">
                    Ver Producto
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Botón de logout */}
      <Button onClick={handleLogout} className="w-full mt-4">
        <LogOut className="mr-2 h-4 w-4" />
        Logout
      </Button>
    </div>
  )
}
