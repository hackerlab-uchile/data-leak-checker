import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import Search from "@/components/Search";
import Navbar from "@/components/Navbar";
import CryptoJS from "crypto-js";
import { FormEvent, useState } from "react";
import { Breach } from "@/models/Breach";
import { MdError } from "react-icons/md";
import { FaCheckCircle } from "react-icons/fa";
import Link from "next/link";
import { useRouter } from "next/router";
import { QueryType } from "@/api/api";

export default function Home2() {
  const router = useRouter();
  const [searchEmail, setSearchEmail] = useState("");
  const [responseReceived, setResponseReceived] = useState(false);
  const [searchRut, setSearchRut] = useState("");
  const [searchPhone, setSearchPhone] = useState("");
  const [breaches, setBreaches] = useState<Array<Breach>>([]);

  async function handleEmailSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (searchEmail) {
      router.push(
        `/search?search=${searchEmail}&type=${QueryType.Email}`,
        "/search"
      );
    }
  }

  async function handleRutSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (searchRut) {
      router.push(
        `/search?search=${searchRut}&type=${QueryType.Rut}`,
        "/search"
      );
    }
  }

  async function handlePhoneSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (searchPhone) {
      router.push(
        `/search?search=${searchPhone}&type=${QueryType.Phone}`,
        "/search"
      );
    }
  }

  const searchKeys = [
    {
      title: "Email",
      value: "email",
      description:
        "Ingrese el correo electrónico que desea consultar. Se revisará si dicho correo fue encontrado en alguna filtración de datos que tengamos conocimiento.",
      submitFunc: handleEmailSearch,
      search: searchEmail,
      setSearch: setSearchEmail,
      inputHint: "Consulte un email...",
      name: "correo",
    },
    {
      title: "RUT",
      value: "rut",
      description:
        "Ingrese el RUT que desea consultar. Se revisará si dicho RUT fue encontrado en alguna filtración de datos que tengamos conocimiento.",
      submitFunc: handleRutSearch,
      search: searchRut,
      setSearch: setSearchRut,
      inputHint: "Consulte un RUT...",
      name: "RUT",
    },
    {
      title: "Número telefónico",
      value: "phone",
      description:
        "Ingrese el número telefónico que desea consultar. Se revisará si dicho número fue encontrado en alguna filtración de datos que tengamos conocimiento." +
        "\nRecuerde que un número celular tiene el siguiente format 9 XXXX XXXX, mientras que uno particular 22 XXXX XXX.",
      submitFunc: handlePhoneSearch,
      search: searchPhone,
      setSearch: setSearchPhone,
      inputHint: "Consulte un número telefónico...",
      name: "número telefónico",
    },
  ];

  function clearSearchIput() {
    // setSearchEmail("");
    setResponseReceived(false);
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-start p-24 pt-5">
      <Navbar />
      <div className="flex flex-col mt-5 w-full items-center justify-start">
        {/* </div> */}

        {/* <div className="z-10 max-w-5xl w-full font-mono text-sm lg:flex flex-col"> */}
        {/* <div className='flex-col w-[80%]'> */}
        <h3 className="font-bold">Consultar por:</h3>
        <Tabs defaultValue="email" className="w-[80%]">
          <TabsList className="grid w-full grid-cols-3">
            {searchKeys.map((item) => (
              <TabsTrigger
                onClick={clearSearchIput}
                key={item.value}
                value={item.value}
              >
                {item.title}
              </TabsTrigger>
            ))}
          </TabsList>
          {searchKeys.map((item) => (
            <TabsContent key={item.value} value={item.value}>
              <Card>
                <CardHeader>
                  <CardTitle>{item.title}</CardTitle>
                  <CardDescription>{item.description}</CardDescription>
                </CardHeader>
                <form
                  onSubmit={item.submitFunc}
                  autoComplete="off"
                  className="w-full"
                >
                  <CardContent className="space-y-2">
                    <div className="z-10 max-w-5xl w-full items-center self-center justify-self-center justify-between font-mono text-sm lg:flex">
                      <Search
                        placeholder={item.inputHint}
                        searchTerm={item.search}
                        setSearchTerm={item.setSearch}
                      />
                    </div>
                  </CardContent>
                  <CardFooter className="flex flex-row items-center justify-center">
                    {/* <Link
                      href={{
                        pathname: "/search",
                        query: { search: `${searchEmail}` },
                      }}
                    > */}
                    <Button type="submit">Buscar</Button>
                    {/* </Link> */}
                  </CardFooter>
                </form>
              </Card>
            </TabsContent>
          ))}
        </Tabs>
        {/* </div> */}
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}
