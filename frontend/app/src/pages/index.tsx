import Search from '@/components/Search'
import Navbar from '@/components/Navbar'
import Image from 'next/image'
import { FormEvent, useState } from 'react'
import { Breach } from '@/models/Breach';
import { getBreachesByEmail } from '@/api/api';

export default function Home() {
  const [search, setSearch] = useState("");

  async function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    // const emailQuery = (event.target as HTMLElement).search.value;
    if (search) {
      const emailQuery = search;
      console.log("SearchingEQ: ", emailQuery);
      console.log("Searching: ", search);
      const breachesList: Breach[] = await getBreachesByEmail(emailQuery);
      console.log("Response: ", breachesList);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <Navbar />
      <div className="z-10 max-w-5xl w-full items-start justify-between font-mono text-sm lg:flex flex-col">
        <div className='self-start w-[60%]'>
          <h3 className='font-bold'>Verificación de correo electrónico</h3>
          <p>Ingrese el correo electrónico que desea consultar. Se revisará si dicho correo fue encontrado en alguna filtración de datos que tengamos conocimiento.</p>
        </div>
      </div>
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <form onSubmit={handleSearch} className='w-full'>
          <Search
            placeholder={'Consulte un email...'}
            searchTerm={search}
            setSearchTerm={setSearch}
          />
        </form>
      </div>

      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]">
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
      </div>
    </main>
  )
}
