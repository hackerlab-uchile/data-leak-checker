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
import { FormEvent, Suspense, useEffect, useState } from "react";
import { Breach, DataLeak } from "@/models/Breach";
import { getDataLeaksByValueAndType, QueryType } from "@/api/api";
import { FaCheckCircle } from "react-icons/fa";
import { MdOutlineSecurity } from "react-icons/md";
import { AiOutlineSafety } from "react-icons/ai";
import { useRouter } from "next/router";
import { IconContext } from "react-icons";
import { PiShieldWarningFill } from "react-icons/pi";
import { LeaksTable } from "@/components/breaches/leaks-table";
import { ColumnDef } from "@tanstack/react-table";
import {
  TypesLeak,
  getLeakTableColumns,
  getLeakTableRows,
} from "@/components/breaches/columns";

const redColor = "#ED342F";

export default function Home2() {
  const router = useRouter();
  const [searchEmail, setSearchEmail] = useState("");
  const [responseReceived, setResponseReceived] = useState(false);
  const [searchRut, setSearchRut] = useState("");
  const [searchPhone, setSearchPhone] = useState("");
  const [dataLeaks, setDataLeaks] = useState<Array<DataLeak>>([]);
  const [columns, setColumns] = useState<ColumnDef<TypesLeak>[]>([]);
  const [tableData, setTableData] = useState<TypesLeak[]>([]);

  async function handleEmailSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const emailQuery = searchEmail.trim();
    if (emailQuery) {
      const dataLeaksList: DataLeak[] = await getDataLeaksByValueAndType(
        emailQuery,
        QueryType.Email
      );
      setDataLeaks(dataLeaksList);
      setResponseReceived(true);
    }
  }

  async function handleRutSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const rutQuery = searchRut
      .trim()
      .replace(" ", "")
      .replace(".", "")
      .replace("-", "");
    if (rutQuery) {
      // TODO: Remove '.' and '-' symbols
      const dataLeaksList: DataLeak[] = await getDataLeaksByValueAndType(
        rutQuery,
        QueryType.Rut
      );
      setDataLeaks(dataLeaksList);
      setResponseReceived(true);
    } else {
      console.log("Not valid rut!");
    }
  }

  async function handlePhoneSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const phoneQuery = searchPhone.trim();
    if (phoneQuery) {
      const dataLeaksList: DataLeak[] = await getDataLeaksByValueAndType(
        phoneQuery,
        QueryType.Phone
      );
      setDataLeaks(dataLeaksList);
      setResponseReceived(true);
    }
  }

  useEffect(() => {
    if (dataLeaks.length > 0) {
      setColumns(getLeakTableColumns(dataLeaks));
      setTableData(getLeakTableRows(dataLeaks));
    }
  }, [dataLeaks]);

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
    setSearchEmail("");
    setSearchPhone("");
    setSearchRut("");
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
              {responseReceived ? (
                <div className="flex flex-col mt-5 w-full items-center justify-start">
                  <div className="flex flex-col w-full self-start justifiy-start items-center">
                    {dataLeaks.length > 0 ? (
                      <>
                        <IconContext.Provider value={{ color: `${redColor}` }}>
                          <PiShieldWarningFill
                            fontSize="3.5em"
                            className="self-center"
                          />
                          <AlertMessage
                            boxColor="bg-red-hackerlab"
                            message={`¡Este ${item.name} ha sido visto en ${dataLeaks.length} filtraciones de nuestro conocimiento!`}
                          />
                        </IconContext.Provider>
                        {/* <div className="container mx-auto py-10"> */}
                        <div className="w-full mx-auto py-5">
                          <LeaksTable
                            columns={columns}
                            data={tableData}
                            queried_type={item.name}
                          />
                        </div>
                      </>
                    ) : (
                      <IconContext.Provider value={{ color: "green" }}>
                        <FaCheckCircle
                          color="green"
                          fontSize="3.5em"
                          className="self-center"
                        />
                        <AlertMessage
                          boxColor="bg-green-hackerlab"
                          message={`¡Este ${item.name} no ha sido encontrado en filtraciones de nuestro conocimiento!`}
                        />
                      </IconContext.Provider>
                    )}
                  </div>
                  {dataLeaks.map((dLeak, index) => (
                    <BreachCard
                      key={index}
                      breach={dLeak.breach}
                      index={index}
                    />
                  ))}
                </div>
              ) : (
                <Suspense fallback={<p>Buscando...</p>}></Suspense>
              )}
            </TabsContent>
          ))}
        </Tabs>
        {/* </div> */}
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left"></div>
    </main>
  );
}

function BreachCard({ breach, index }: { breach: Breach; index: number }) {
  return (
    <div
      id={`${index}`}
      className="flex flex-col items-start my-1 p-4 border rounded-lg w-full"
    >
      <h3 className="font-bold text-xl">
        {`${breach.name} (${breach.breach_date.slice(0, 4)})`}
      </h3>
      <p>{breach.description}</p>
      <p>
        <b>Tipos de datos encontrados: </b>
        {breach.breached_data.join(", ")}
      </p>
      <p className="font-bold self-center pt-2 underline">
        Consejos de seguridad
      </p>
      <div className="flex flex-col">
        {breach.security_tips.map((tip, index) => (
          <div className="ml-3 flex flex-row items-center gap-1" key={index}>
            {/* <MdOutlineSecurity color="green"></MdOutlineSecurity> */}
            <AiOutlineSafety color="green"></AiOutlineSafety>
            <>{tip}</>
          </div>
        ))}
        {/* <div className="flex flex-row items-center">
          <p>Contraseña</p>
          <MdError color="red"></MdError>
        </div>
        <div className="flex flex-row items-center">
          <p>Contraseña</p>
          <MdError style={{ fill: `${redColor}` }}></MdError>
        </div> */}
      </div>
    </div>
  );
}

function AlertMessage({
  message,
  boxColor,
}: {
  message: string;
  boxColor: string;
}) {
  return (
    <div
      className={`flex px-3 rounded-md justify-center text-white ${boxColor} w-[90%]`}
    >
      <p className="text-xl text-center">{message}</p>
    </div>
  );
}
