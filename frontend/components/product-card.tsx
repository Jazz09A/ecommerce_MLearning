import Image from 'next/image'
import Link from 'next/link'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import React from 'react'

interface ProductCardProps {
  title: string
  price: number
  description: string
  href: string
}

export function ProductCard({ title, price, description, href }: ProductCardProps) {
  return (
    <Card className="group overflow-hidden">
      <div className="cursor-pointer">
        <Link href={href} className="block">
          <CardContent className="p-0">
            <Image
              src="/placeholder.svg"
              alt={title}
              width={400}
              height={300}
              className="aspect-[4/3] object-cover w-full"
            />
          </CardContent>
        </Link>
        <CardFooter className="flex flex-col items-start gap-2 p-4">
          <Link href={href} className="block">
            <h3 className="font-semibold">{title}</h3>
          </Link>
          <p className="text-sm text-muted-foreground">{description}</p>
          <p className="font-bold">
            ${price.toFixed(2)}
          </p>
        </CardFooter>
      </div>
    </Card>
  )
}

