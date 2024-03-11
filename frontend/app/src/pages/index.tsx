
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

import Search from '@/components/Search'
import Navbar from '@/components/Navbar'
import Image from 'next/image'
import { FormEvent, useState } from 'react'
import { Breach } from '@/models/Breach';
import { getBreachesByEmail } from '@/api/api';
import { MdError } from "react-icons/md";
import { FaCheckCircle } from "react-icons/fa";
import Link from "next/link"

export default function Home() {
  const [search, setSearch] = useState("");
  const [breaches, setBreaches] = useState<Array<Breach>>([]);
  const [responseReceived, setResponseReceived] = useState(false);

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (search) {
      const emailQuery = search;
      console.log("SearchingEQ: ", emailQuery);
      console.log("Searching: ", search);
      const breachesList: Breach[] = await getBreachesByEmail(emailQuery);
      console.log("Response: ", breachesList);
      setBreaches(breachesList);
      setResponseReceived(true);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24">
      <Navbar />
      <div className="flex flex-col w-full items-center justify-start">
      {/* </div> */}

      {/* <div className="z-10 max-w-5xl w-full font-mono text-sm lg:flex flex-col"> */}
        {/* <div className='flex-col w-[80%]'> */}
          <h3 className='font-bold'>Búsqueda por:</h3>
          <Tabs defaultValue="email" className="w-[80%]">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="email">Email</TabsTrigger>
              <TabsTrigger value="rut">RUT</TabsTrigger>
              <TabsTrigger value="phone">Phone</TabsTrigger>
            </TabsList>
            <TabsContent value="email">
              <Card>
                <CardHeader>
                  <CardTitle>Email</CardTitle>
                  <CardDescription>
                    Ingrese el correo electrónico que desea consultar. Se revisará si dicho correo fue encontrado en alguna filtración de datos que tengamos conocimiento.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="z-10 max-w-5xl w-full items-center self-center justify-self-center justify-between font-mono text-sm lg:flex">
                    <form onSubmit={handleSearch} className='w-full'>
                      <Search
                        placeholder={'Consulte un email...'}
                        searchTerm={search}
                        setSearchTerm={setSearch}
                      />
                    </form>
                  </div>
                </CardContent>
                <CardFooter className="flex flex-row items-center justify-center">
                  <Button>Buscar</Button>
                </CardFooter>
              </Card>
            </TabsContent>
            <TabsContent value="rut">
              <Card>
                <CardHeader>
                  <CardTitle>RUT</CardTitle>
                  <CardDescription>
                    holi
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="z-10 max-w-5xl w-full items-center self-center justify-self-center justify-between font-mono text-sm lg:flex">
                    <form onSubmit={handleSearch} className='w-full'>
                      <Search
                        placeholder={'Consulte un RUT...'}
                        searchTerm={search}
                        setSearchTerm={setSearch}
                      />
                    </form>
                  </div>
                </CardContent>
                <CardFooter className="flex flex-row items-center justify-center">
                  <Button>Buscar</Button>
                </CardFooter>
              </Card>
            </TabsContent>
          </Tabs>
        {/* </div> */}
      </div>

      {responseReceived && (
        // <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]">
        <div className="flex place-items-center">
          <label>
            {breaches.length > 0 ? (
              <div className='flex flex-col'>
                <div className='pb-2 flex flex-row'>
                  <MdError color="red" fontSize="4.5em" className="self-center" />
                  <p className='pl-3 self-center'>
                    Su correo ha sido encontrado en las siguiente filtraciones:
                  </p>
                </div>
                <div className='flex flex-col w-full'>
                  <div className='flex flex-col w-full'>
                    {breaches.map((breach) => (
                      <div key={breach.id} className='my-1 p-4 border rounded-lg w-full'>
                        <h4 className='text-lg font-bold'>{breach.name}</h4>
                        <p>{breach.description}</p>
                        <p>{`Fecha de subida: ${breach.created_at.slice(0, 10)}`}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className='pb-2 flex flex-row'>
                <FaCheckCircle color="green" fontSize="4.5em" className="self-center" />
                <p className='pl-3 self-center'>
                  Su correo <strong>NO</strong> ha sido encontrado en filtraciones de nuestro conocimiento.
                </p>
              </div>
            )}
          </label>
        </div>
      )}

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
      </div>
    </main>
  )
}
