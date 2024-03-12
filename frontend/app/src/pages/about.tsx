import Navbar from '@/components/Navbar'
import { FormEvent, useState } from 'react'
import { Breach } from '@/models/Breach';

export default function Home() {

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24 pt-5">
      <Navbar/>
    <h2 className='text-2xl font-bold self-start'>Acerca de este proyecto</h2>
      <div className="flex flex-col mt-5 w-full items-center justify-start">
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
      </div>
    </main>
  )
}
